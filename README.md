<h1>air-writing-recognition-system</h1>
<p>Real-time touchless handwriting canvas and character recognition system powered by MediaPipe, OpenCV, and Deep Convolutional Neural Networks (CNN)</p>

<h2>Project description</h2>
<p>This project implements an interactive, real-time Computer Vision and Deep Learning pipeline that enables users to write in the air using fingertip trajectories and automatically transcribes gestures into text:</p>
<ol>
  <li>
    <dl>
      <dt><b>Hand Landmark Tracking (MediaPipe Hands):</b></dt>
      <dd>Detects 21 3D hand landmarks in real time with high confidence thresholds (&ge; 0.80) via webcam feed.</dd>
      <dd>Tracks the index fingertip (<code>INDEX_FINGER_TIP</code>) as an interactive virtual stylus.</dd>
    </dl>
  </li>
  <li>
    <dl>
      <dt><b>Gesture-Based State Machine:</b></dt>
      <dd><b>Writing Mode:</b> Extended index finger draws continuous strokes on the virtual canvas.</dd>
      <dd><b>Pen-Up / Idle:</b> Clenched fist detection (<code>fist_detect</code>) pauses stroke rendering to prevent unwanted travel lines.</dd>
      <dd><b>Thumbs-Up Confirmation:</b> Gesture recognition (<code>is_thumb_up</code>) for state confirmation and navigation.</dd>
    </dl>
  </li>
  <li>
    <dl>
      <dt><b>Computer Vision Preprocessing (OpenCV):</b></dt>
      <dd>Captures raw pixel paths, applies morphological erosion to eliminate artifacts, and detects character contours (<code>findContours</code>)[span_16](start_span)[span_16](end_span).</dd>
      <dd>Extracts bounding boxes, centers characters with aspect-ratio preservation, and normalizes them into 28&times;28 grayscale matrices.</dd>
    </dl>
  </li>
  <li>
    <dl>
      <dt><b>Deep Learning Character Classifier (TensorFlow / Keras):</b></dt>
      <dd>Custom 2D Convolutional Neural Network (Conv2D &rarr; MaxPool &rarr; Dropout &rarr; Dense).</dd>
      <dd>Trained on the extended EMNIST dataset across 62 alphanumeric classes (0–9, A–Z, a–z).</dd>
    </dl>
  </li>
  <li>
    <dl>
      <dt><b>Web Interface & Streaming (Flask):</b></dt>
      <dd>Streams live video with canvas overlays using multipart HTTP MJPEG.</dd>
      <dd>Asynchronously polls recognition predictions and binds keyboard shortcuts for full keyboardless writing.</dd>
    </dl>
  </li>
</ol>

<h2>Project files</h2>
<table>
  <tr>
    <th colspan="2">air-writing-recognition-system</th>
  </tr>
  <tr>
    <td>main.py</td>
    <td>Application root entry point initializing and launching the Flask web server</td>
  </tr>
  <tr>
    <td>pages/mainPage.py</td>
    <td>Flask routing engine managing REST endpoints, MJPEG video streaming, and canvas states</td>
  </tr>
  <tr>
    <td>logic/AirWritingApp.py</td>
    <td>Core orchestrator synchronizing video capture, hand tracking, and canvas rendering</td>
  </tr>
  <tr>
    <td>logic/workWithHand/HandTracker.py</td>
    <td>MediaPipe wrapper for 21-point hand tracking, fingertip extraction, and gesture detection</td>
  </tr>
  <tr>
    <td>logic/workWithHand/GestureWriter.py</td>
    <td>TensorFlow/Keras CNN classifier for offline training and real-time character inference</td>
  </tr>
  <tr>
    <td>logic/canva/DrawingCanvas.py</td>
    <td>Virtual 2D canvas, line interpolation, contour filtering, and 28&times;28 normalization</td>
  </tr>
  <tr>
    <td>data/config.py</td>
    <td>Path configuration and EMNIST 62-class alphanumeric character label mappings</td>
  </tr>
  <tr>
    <td>templates/index.html</td>
    <td>Web frontend displaying live stream, candidate predictions, and controls</td>
  </tr>
  <tr>
    <td>static/js/script.js</td>
    <td>Client-side script handling button events, key bindings, and async inference polling</td>
  </tr>
  <tr>
    <td>requirements.txt</td>
    <td>Python package dependencies (TensorFlow, OpenCV, MediaPipe, Flask, NumPy)</td>
  </tr>
</table>

<h2>Keyboard shortcuts</h2>
<table>
  <tr>
    <th>Key</th>
    <th>Action</th>
  </tr>
  <tr>
    <td><b>S</b></td>
    <td>Save / append current predicted letter to the accumulated text</td>
  </tr>
  <tr>
    <td><b>C</b></td>
    <td>Clear virtual drawing canvas</td>
  </tr>
  <tr>
    <td><b>Space</b></td>
    <td>Insert a space character</td>
  </tr>
  <tr>
    <td><b>D</b></td>
    <td>Delete / backspace last recorded letter</td>
  </tr>
</table>

<h2>Installation and launch</h2>
<ol>
  <b>
    <li>
      <dl>
        <dt>Clone the repository</dt>
        <dd>
          <code>git clone https://github.com/Kyoryuu-lab/air-writing-recognition-system.git</code>
        </dd>
        <dd>
          <code>cd air-writing-recognition-system</code>
        </dd>
      </dl>
    </li>
  </b>
  <b>
    <li>
      <dl>
        <dt>Create and activate virtual environment</dt>
        <dd>
          <code>python3 -m venv .venv</code>
        </dd>
        <dd>
          <code>source .venv/bin/activate</code> <i>(macOS/Linux)</i> or <code>.venv\Scripts\activate</code> <i>(Windows)</i>
        </dd>
      </dl>
    </li>
  </b>
  <b>
    <li>
      <dl>
        <dt>Install dependencies</dt>
        <dd>
          <code>pip install -r requirements.txt</code>
        </dd>
      </dl>
    </li>
  </b>
  <b>
    <li>
      <dl>
        <dt>Launch the application</dt>
        <dd>
          <code>python main.py</code>
        </dd>
        <dd>Open your browser and navigate to: <code>http://localhost:5000</code></dd>
      </dl>
    </li>
  </b>
</ol>

<h2>Example of console output</h2>
<samp>
  <p>
    ========================================================================<br />
    &nbsp;&nbsp;AIR WRITING SYSTEM | COMPUTER VISION &amp; DEEP LEARNING<br />
    ========================================================================<br />
    [*] Loading pre-trained EMNIST CNN model from storage...<br />
    [*] MediaPipe Hands tracking initialized (Confidence: 0.80)<br />
    [*] Starting Flask web server on http://0.0.0.0:5000<br />
    &nbsp;* Serving Flask app 'pages.mainPage'<br />
    &nbsp;* Debug mode: on<br />
    &nbsp;* Running on all addresses (0.0.0.0)<br />
    &nbsp;* Running on http://127.0.0.1:5000<br />
    ------------------------------------------------------------------------<br />
    [CV-FEED] Video stream active (Camera index: 0)<br />
    [INFERENCE] Detected character: 'A' | Confidence: 94.8%<br />
    [INFERENCE] Detected character: 'B' | Confidence: 91.2%<br />
    [GESTURE] Fist detected &rarr; Pausing stroke buffer<br />
    ========================================================================
  </p>
</samp>

