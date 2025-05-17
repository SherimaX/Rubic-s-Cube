# Rubik's Cube Solver Server

This project provides a simple Flask server and web page that allows you to
capture images of a Rubik's Cube with your phone camera and receive a solving
sequence. The cube state detection from images is currently a placeholder and
needs a real computer vision implementation.

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
   access and capture six faces of the cube in order. When all six faces are
   captured, click **Solve Cube** to send the images to the server. The server
   will attempt to compute a solution using the `kociemba` algorithm.

## Notes

- The current `detect_cube_state` function in `server/app.py` is a stub that
  always returns a solved cube state. You must implement color detection and
  mapping from captured images to the cube notation for a working solver.
- Make sure `opencv-python` is installed if you intend to process images.
