# Rubik's Cube Solver Server

This project provides a simple Flask server and web page that allows you to
capture images of a Rubik's Cube with your phone camera and receive a solving
sequence. A minimal color-based detection routine is included but is fairly
naïve and may not work in poor lighting conditions. Further computer vision
improvements are needed for reliable solving.

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

- The `detect_cube_state` function in `server/app.py` performs a simple color
  averaging approach to guess the cube colors. It expects faces to be captured
  in the order Up, Right, Front, Down, Left, Back. The algorithm works best in
  bright lighting and is only meant as a starting point.
- Make sure `opencv-python` is installed if you intend to process images.
