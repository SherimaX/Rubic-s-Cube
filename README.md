# Rubik's Cube Solver Server

This project provides a simple Flask server and web page that allows you to
capture images of a Rubik's Cube with your phone camera and receive a solving
sequence. The cube state detection uses a very basic color-based routine and
should only be considered a starting point.

## Setup

1. Install Python dependencies (preferably in a virtual environment):

```bash
pip install -r server/requirements.txt
```

2. Run the server:

```bash
python server/app.py
```

3. Visit `http://localhost:5000` from your phone or computer. Allow camera
   access and capture faces in the following order: **Up, Right, Front, Down,
   Left, Back**. When all six faces are captured, click **Solve Cube** to send
   the images to the server. The server will attempt to compute a solution
   using the `kociemba` algorithm.

## Notes

- The `detect_cube_state` function in `server/app.py` implements a naive
  HSV-based color classification. It works best with uniform lighting and
  clear cube stickers. More sophisticated vision logic is recommended for a
  production-ready solver.
- Make sure `opencv-python` is installed if you intend to process images.
