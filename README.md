# ❄️ FrostWrite — Magical Air Canvas

FrostWrite is a real-time **AI-powered Air Canvas** application that allows users to draw in the air using hand gestures — without touching a screen, mouse, or keyboard.

Built using **Python, OpenCV, and MediaPipe**, the project tracks hand movements through the webcam and converts them into a virtual drawing experience.

The project also includes a unique **Ice Energy Mode**, where two detected hands create a glowing animated energy connection with particles, sparkles, and ice-crystal effects.

---

## ✨ Features

### 🖐️ Touchless Air Drawing
Draw on a virtual canvas by simply moving your index finger in the air.

### 🎨 Multiple Brush Colors
Switch between different brush colors using keyboard shortcuts:

- 🔵 Ice Blue
- 🟣 Purple
- 🩷 Pink
- 🟢 Green

### ❄️ Ice Energy Mode
When two hands come close to each other, FrostWrite automatically activates **ICE LINK mode**.

It creates:

- ⚡ Animated energy strands
- ✨ Glowing particles
- 💫 Sparkles
- ❄️ Ice-crystal effects
- 🔵 Dynamic blue glow

### 🧹 Gesture-Based Eraser
Show all four fingers to activate the eraser and remove drawings without touching the screen.

### 🧼 Clear Canvas
Press `C` to instantly clear the entire virtual canvas.

### 🎥 Real-Time Hand Tracking
MediaPipe detects and tracks hand landmarks in real time through the webcam.

### 🖥️ Live Interface
The application displays:

- Current mode
- Selected brush color
- Gesture controls
- Hand distance
- Ice Energy status

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Core programming language |
| OpenCV | Webcam processing and drawing |
| MediaPipe | Real-time hand tracking |
| NumPy | Virtual canvas and image processing |
| Math | Distance and geometric calculations |
| Time | Animation and dynamic effects |

---

## 🧠 How It Works

FrostWrite uses the webcam to capture live video frames.

### Step 1 — Capture Video

OpenCV accesses the webcam and captures the user's hand movements.

### Step 2 — Hand Detection

MediaPipe Hands detects hand landmarks and identifies important finger positions.

### Step 3 — Gesture Recognition

The system checks which fingers are raised.

#### ☝️ Index Finger Only

Activates:

```text
DRAW MODE
