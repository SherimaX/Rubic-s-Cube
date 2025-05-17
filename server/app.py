from flask import Flask, render_template, request, jsonify
import base64
import cv2
import numpy as np
try:
    import kociemba
except ImportError:  # handle if not installed
    kociemba = None

app = Flask(__name__)

# Simple color-based cube state detection

def detect_cube_state(images):
    """Detect cube state from a list of six base64 encoded PNG images.

    Images must be provided in the order Up, Right, Front, Down, Left, Back.
    Each face is divided into a 3x3 grid. The mean color of each grid cell is
    classified using HSV ranges to one of the cube colors. This routine is very
    naive and works best in even lighting conditions.
    """

    # HSV ranges for cube sticker colors
    color_ranges = {
        'U': [(np.array([0, 0, 180]), np.array([180, 50, 255]))],            # white
        'R': [(np.array([0, 120, 70]), np.array([10, 255, 255])),            # red
              (np.array([160, 120, 70]), np.array([180, 255, 255]))],
        'F': [(np.array([50, 100, 100]), np.array([85, 255, 255]))],         # green
        'D': [(np.array([20, 100, 100]), np.array([35, 255, 255]))],         # yellow
        'L': [(np.array([10, 100, 100]), np.array([20, 255, 255]))],         # orange
        'B': [(np.array([90, 150, 50]), np.array([130, 255, 255]))],         # blue
    }

    def classify(hsv_pixel):
        for face, ranges in color_ranges.items():
            for lower, upper in ranges:
                if np.all(hsv_pixel >= lower) and np.all(hsv_pixel <= upper):
                    return face
        return 'U'  # default to white if uncertain

    cube = ''
    for img_str in images:
        # Remove possible data URI prefix
        if ',' in img_str:
            img_str = img_str.split(',', 1)[1]
        img_data = base64.b64decode(img_str)
        buf = np.frombuffer(img_data, dtype=np.uint8)
        img = cv2.imdecode(buf, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError('Invalid image data')

        h, w, _ = img.shape
        step_y, step_x = h // 3, w // 3
        for row in range(3):
            for col in range(3):
                y0, x0 = row * step_y, col * step_x
                roi = img[y0:y0 + step_y, x0:x0 + step_x]
                hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                mean = hsv.reshape(-1, 3).mean(axis=0)
                cube += classify(mean)

    return cube


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
