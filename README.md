# Rubik's Cube Solver Server

This project exposes a small Flask application and web interface for solving a Rubik's Cube. The page uses your device camera to capture six images of the cube and sends them to the server for solving.

The server contains a very basic color-based cube state detector implemented with OpenCV. It works best in good, even lighting and expects the six faces to be captured in the following order:

1. **Up**
2. **Right**
3. **Front**
4. **Down**
5. **Left**
6. **Back**

Once all images are captured the server will try to compute a solution using the `kociemba` algorithm.
=======
This project provides a simple Flask server and web page that allows you to
capture images of a Rubik's Cube with your phone camera and receive a solving
sequence. The cube state detection from images is currently a placeholder and
needs a real computer vision implementation.

3. Open `http://localhost:5000` on your phone or computer. Allow camera access and capture each face in the order listed above. After all faces are captured click **Solve Cube**.

## Notes

- The detection routine is a simple heuristic and may fail with poor lighting or unusual sticker shades.
- Ensure `opencv-python` and `numpy` are installed so the detection code can run.
=======
3. Visit `http://localhost:5000` from your phone or computer. Allow camera
   access and capture six faces of the cube in order. When all six faces are
   captured, click **Solve Cube** to send the images to the server. The server
   will attempt to compute a solution using the `kociemba` algorithm.

## Notes

- The current `detect_cube_state` function in `server/app.py` is a stub that
  always returns a solved cube state. You must implement color detection and
  mapping from captured images to the cube notation for a working solver.
- Make sure `opencv-python` is installed if you intend to process images.