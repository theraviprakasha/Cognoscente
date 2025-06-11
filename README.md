# Cognoscente – Gamified Cognitive Retraining Platform

A web-based platform designed to **enhance cognitive skills in children with developmental disabilities** through gamification and virtual EEG neuro-feedback. Developed using Flask and SQLite, this platform provides engaging games and user/admin dashboards to monitor progress and collect feedback.

---

## Screenshots
<img width="1440" alt="TOH" src="https://github.com/user-attachments/assets/8ec697bd-d2a7-4b8a-baf8-777480b930e0" />
<img width="1440" alt="TicTacToe" src="https://github.com/user-attachments/assets/e489e279-d2dd-44e6-8e9b-abe323ba40ea" />
<img width="1440" alt="Tetris" src="https://github.com/user-attachments/assets/b66a06e1-295f-4c8f-8eca-1dd15786481f" />
<img width="1440" alt="Sudoku" src="https://github.com/user-attachments/assets/d7ae8934-2223-4002-8ca8-6bd9f3cc6e72" />
<img width="1440" alt="Report 4" src="https://github.com/user-attachments/assets/3f2668d9-ca4e-4ae4-892e-a1d84ef39303" />
<img width="1440" alt="Report 3" src="https://github.com/user-attachments/assets/20b920ae-8397-4f9d-b2d7-243a030c35bb" />
<img width="1440" alt="Report 2" src="https://github.com/user-attachments/assets/ab4be7e0-a5fa-4460-b805-426119a59483" />
<img width="1440" alt="Report 1" src="https://github.com/user-attachments/assets/02808af2-f8ed-4642-8548-38555dff1ae5" />
<img width="1440" alt="Player Registration" src="https://github.com/user-attachments/assets/4e307a3a-daa9-4669-8978-95bc7e868ba3" />
<img width="1440" alt="Player Login" src="https://github.com/user-attachments/assets/97594469-1b23-4676-b952-35021c65699a" />
<img width="1440" alt="Pattern Matching" src="https://github.com/user-attachments/assets/63fe7156-12b4-45f2-8671-4675619f8bcb" />
<img width="1440" alt="Home Page" src="https://github.com/user-attachments/assets/04f33478-f22e-48d4-a3fa-79eff68e0128" />
<img width="1440" alt="Games 2" src="https://github.com/user-attachments/assets/c5f3f0d8-c571-4946-9951-222f1c753496" />
<img width="1440" alt="Games 1" src="https://github.com/user-attachments/assets/d381ee42-4aaa-4152-8111-883d35d5fa1f" />
<img width="1440" alt="Feedback 2" src="https://github.com/user-attachments/assets/dd6a0d9a-8a48-4bc8-a968-f8205ef0ddad" />
<img width="1440" alt="Feedback 1" src="https://github.com/user-attachments/assets/000a8f8b-d256-438c-b650-c5ed175948cc" />
<img width="1440" alt="Expert Report 2" src="https://github.com/user-attachments/assets/ce483d6e-f390-40c9-8b37-59a641fd532f" />
<img width="1440" alt="Expert Report" src="https://github.com/user-attachments/assets/90f1fed6-cd85-4691-b4ce-f689354307c3" />
<img width="1440" alt="Expert Login" src="https://github.com/user-attachments/assets/54a68aea-d2c9-4cf4-8a46-a6e2580d6a52" />
<img width="1440" alt="About" src="https://github.com/user-attachments/assets/ba5bb9ef-b3f2-4cb3-a2b0-1795e92ae536" />



---

## 🧠 Project Summary

Cognoscente combines cognitive retraining therapy and modern web technology to help children improve:
- Attention
- Memory
- Reasoning
- Decision-making
- Problem-solving
- Reaction time

### Key Features:
- 🎮 Multiple cognitive training games (Tetris, Sudoku, Whack-a-Mole, Pattern Matching, etc.)
- 👨‍👩‍👧‍👦 Role-based login system (User/Admin)
- 🧾 User registration and feedback collection
- 📊 Admin interface for feedback viewing and monitoring
- 🧠 Simulated EEG-based tracking using game performance data
- 💽 SQLite databases for persistent user and gameplay data

---

## 🚀 Technologies Used

- **Frontend**: HTML, CSS, JavaScript, Jinja2 templates
- **Backend**: Python with Flask
- **Database**: SQLite
- **Other**: Adobe XD/Figma for UI design, GitHub for version control

---

## 🔧 Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/cognoscente.git
   cd cognoscente
   ```

2. **Create a Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   # or
   .\venv\Scripts\activate    # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install flask
   ```

4. **Run the App**
   ```bash
   python3 app.py
   ```

5. Open your browser and go to:
   ```
   http://127.0.0.1:5000/
   ```

---

## 🗃️ Project Structure

```
├── app.py                # Main Flask application
├── user_data.db          # Main SQLite database for users and feedback
├── templates/            # HTML templates for rendering UI
│   ├── index.html
│   ├── allgames.html
│   ├── patterngraph.html
│   └── ...
├── static/               # Static assets (CSS/JS/images)
├── venv/                 # Python virtual environment (optional)
└── README.md             # This file
```

---

## 👥 Roles & Functionalities

### 👤 User
- Register and log in
- Play cognitive training games
- Submit feedback
- Automatically generate and use a personal gameplay database (e.g., `username.db`)

### 🛠️ Admin
- Login with credentials (`admin@gmail.com` / `admin123`)
- View user feedback (categorized by type)
- Monitor gameplay statistics via graphs

---

## 🎮 List of Games Integrated

| Game         | Tracked Metrics |
|--------------|-----------------|
| Pattern Match | Score, Time, Level, Avg |
| Sudoku        | Score, Time, Mistakes |
| Tetris        | Score, Level, Lines Cleared |
| Tick Tack Toe | Timer, Wins, Losses, Ties |
| Tower of Hanoi| Moves, Timer |
| Whack-a-Mole  | Score, Accuracy, Reaction Time, Duration |

---

## 🧠 EEG Simulation

While actual EEG hardware is not integrated, **game performance is mapped to virtual EEG signals**, simulating neuro-feedback for real-time tracking and therapist insights.

---

## 📚 Academic Background

This project is part of the research titled:

**"Gamified Cognitive Retraining Platform for Children with Developmental Disabilities"**

Published in JETIR by:
- Ravi Prakasha
- Tejaswini B N
- Monika G
- Naveen K V
- Spoorthi M G

View paper for full methodology and impact details.
[ConferencePaper.pdf](https://github.com/user-attachments/files/20698719/ConferencePaper.pdf)


---

## 📄 License

This project is for academic and research purposes only. Contact authors before commercial use.

---

## 💬 Feedback

For issues, suggestions, or improvements, please open an issue or reach out to me on linked in: https://www.linkedin.com/in/raviprakasha/
