# Welcome to Bomb Dodge  🎮💣

A fun and interactive computer vision-based game built using Python and Pygame, where you dodge obstacles and hit moving targets by detecting gestures from your webcam in real time. Uses computer vision to estimate angles and velocity from green-colored object movements and fires projectiles accordingly.

---

## 🧠 Features

- Real-time gesture recognition using OpenCV
- Projectile motion simulation with gravity
- Dynamic obstacles with movement
- Multi-threaded rendering and firing system for smooth gameplay
- Live angle and velocity feedback on screen

---

## 📦 Tech Stack

- **Python**
- **Pygame** (for graphics and game logic)
- **OpenCV** (for camera input and gesture detection)
- **NumPy** (for math operations)
- **Threading & Queues** (for concurrency)

---

## 🚀 Installation Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/AdarshM-07/Vision-CanonGame.git

2. **Create a Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv env
   source env/bin/activate      # macOS/Linux
   env\Scripts\activate.bat     # Windows

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt

4. **Run the Game**
   ```bash
   python main.py

## 🎮 How to Play
	-	Use a green object (like a stick or cap) in front of your webcam.
	-	The left side of the screen detects direction and speed (angle + velocity).
	-	Show green on the right side of the camera view to trigger a projectile.
	-	The projectile will fire in the detected direction to hit the moving green block.
	-	Hit the block to score!
## 📝 Notes
	-	Make sure your webcam is working and there’s enough lighting.
	-	You can replace the background image by modifying the path to your own image in the code:
   ```python
   pygame.image.load("/path/to/your/background.jpg")
