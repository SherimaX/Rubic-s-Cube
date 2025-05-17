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
COLOR_RANGES = {
    'U': [([0, 0, 200], [180, 50, 255])],               # white
    'R': [([0, 70, 50], [10, 255, 255]),
          ([170, 70, 50], [180, 255, 255])],            # red can wrap hue end
    'F': [([50, 70, 50], [85, 255, 255])],              # green
    'D': [([20, 70, 50], [40, 255, 255])],              # yellow
    'L': [([10, 70, 50], [20, 255, 255])],              # orange
    'B': [([90, 70, 50], [130, 255, 255])],             # blue
}


def _classify_color(hsv_pixel):
    h, s, v = hsv_pixel
    for face, ranges in COLOR_RANGES.items():
        for lower, upper in ranges:
            if lower[0] <= h <= upper[0] and \
               lower[1] <= s <= upper[1] and \
               lower[2] <= v <= upper[2]:
                return face
    return 'X'


def detect_cube_state(images):
    """Detect cube state from list of base64 image strings.

    This is a very naive implementation using predefined HSV color ranges.
    It expects the cube faces to be captured in the following order:
    Up, Right, Front, Down, Left, Back.
    """

    state = ''
    for img_str in images:
        img_data = base64.b64decode(img_str.split(',')[1])
        np_arr = np.frombuffer(img_data, np.uint8)
        bgr = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if bgr is None:
            return 'U' * 9 + 'R' * 9 + 'F' * 9 + 'D' * 9 + 'L' * 9 + 'B' * 9
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

        h_step = hsv.shape[0] // 3
        w_step = hsv.shape[1] // 3

        for r in range(3):
            for c in range(3):
                y = r * h_step + h_step // 2
                x = c * w_step + w_step // 2
                patch = hsv[max(0, y-10):y+10, max(0, x-10):x+10]
                mean_hsv = patch.mean(axis=(0, 1))
                state += _classify_color(mean_hsv)

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
