from flask import Flask, render_template, request, jsonify
import base64
import cv2
import numpy as np
try:
    import kociemba
except ImportError:  # handle if not installed
    kociemba = None

app = Flask(__name__)

# --- Cube detection helpers -------------------------------------------------

def _decode_image(data_url):
    """Convert a base64 data URL to a BGR OpenCV image."""
    if ',' in data_url:
        _, encoded = data_url.split(',', 1)
    else:
        encoded = data_url
    img_bytes = base64.b64decode(encoded)
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def _classify_color(hsv_value):
    """Map an HSV mean value to a cube color code."""
    h, s, v = hsv_value
    if v > 180 and s < 40:
        return 'U'  # white
    if h < 10 or h > 160:
        return 'R'  # red
    if 10 <= h < 25:
        return 'L'  # orange
    if 25 <= h < 40:
        return 'D'  # yellow
    if 40 <= h < 90:
        return 'F'  # green
    if 90 <= h < 150:
        return 'B'  # blue
    return 'U'  # fallback


def detect_cube_state(images):
    """Detect cube state from list of base64 image strings.

    The detection here is intentionally simple. Each face image is divided
    into a 3x3 grid and the mean HSV value of each cell is used to classify
    the color. The user must capture the faces in the following order:
    Up, Right, Front, Down, Left, Back.
    """

    state = ''

    for idx, data_url in enumerate(images):
        img = _decode_image(data_url)
        if img is None:
            raise ValueError(f'Invalid image for face {idx}')
        h, w, _ = img.shape
        cell_h, cell_w = h // 3, w // 3
        for row in range(3):
            for col in range(3):
                y1 = row * cell_h + cell_h // 4
                y2 = (row + 1) * cell_h - cell_h // 4
                x1 = col * cell_w + cell_w // 4
                x2 = (col + 1) * cell_w - cell_w // 4
                cell = img[y1:y2, x1:x2]
                hsv = cv2.cvtColor(cell, cv2.COLOR_BGR2HSV)
                mean = hsv.reshape(-1, 3).mean(axis=0)
                state += _classify_color(mean)

    return state

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json(force=True)
    images = data.get('images', [])
    if len(images) != 6:
        return jsonify({'error': 'Six images required'}), 400
    cube_state = detect_cube_state(images)
    if kociemba:
        try:
            solution = kociemba.solve(cube_state)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        solution = 'kociemba not installed'
    return jsonify({'solution': solution})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
