# Rubik's Cube Solver Server

This project provides a simple Flask server and web page that allows you to
capture images of a Rubik's Cube with your phone camera and receive a solving
sequence. Cube colors are detected using a basic HSV color classification
routine. Faces must be captured in the order **Up, Right, Front, Down, Left,
Back** for the solution to be correct.

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
   access and capture six faces in the order listed above. Good lighting is
   required for accurate color detection. When all six faces are captured,
   click **Solve Cube** to send them to the server. The server will attempt to
   compute a solution using the `kociemba` algorithm.

## Notes

- The color detector is very naive and may fail with poor lighting or unusual
  sticker shades. Adjust the HSV ranges in `server/app.py` if needed.
- Make sure `opencv-python` and `numpy` are installed for image processing.
