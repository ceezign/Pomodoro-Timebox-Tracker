
# ⏱️ Pomodoro Timebox Tracker  

A **GUI-based Pomodoro app** written in Python that helps users manage focus sessions and breaks effectively.  
It includes desktop notifications, task tracking, CSV logging, and customizable long breaks after a chosen number of sessions.  

---

## ✨ Features  

- 🖥️ **Simple GUI** with Tkinter for easy interaction  
- 🔔 **Desktop notifications** (via `plyer`) for session reminders  
- 📋 **Optional task name input** to track what you’re working on  
- 🗂️ **CSV logging** of all sessions (task, type, start time, duration)  
- ⏳ **Configurable focus/break durations**  
- 🌙 **Optional long break** after a set number of focus sessions  
- 💾 Fully commented source code for learning and customization  

---

## 📦 Requirements  

Make sure you have Python **3.8+** installed.  
Install dependencies with:  

```bash
pip install plyer
```

(Standard libraries like `tkinter`, `csv`, and `datetime` come with Python.)  

---

## ▶️ Usage  

1. Clone/download the project.  
2. Run the app:  

```bash
python pomodoro_app.py
```

3. Enter an optional **task name** (e.g., *"Finish report"*)  
4. Click **Start Timer** to begin a focus session.  
5. Receive desktop notifications for breaks and new sessions.  
6. All sessions are saved into `pomodoro_log.csv`.  

---

## 📊 CSV Logging Format  

Each session is logged with:  

| Task Name | Session Type | Start Time          | Duration (minutes) |  
|-----------|--------------|---------------------|--------------------|  
| Report    | Focus        | 2025-08-20 10:00 AM | 25                 |  
| Report    | Short Break  | 2025-08-20 10:25 AM | 5                  |  

---

## ⚙️ Customization  

Inside the code, you can change:  

- `FOCUS_TIME = 25` → Focus session length in minutes  
- `SHORT_BREAK = 5` → Short break length  
- `LONG_BREAK = 15` → Long break length  
- `SESSIONS_BEFORE_LONG_BREAK = 4` → Number of focus sessions before long break  

---

## 🖼️ Demo Screenshot  

![Pomodoro Demo](screenshot.png)  

---

## 🚀 Future Improvements  

- Add sound alerts 🎵  
- Graphical stats dashboard 📈  
- Dark/light mode themes 🌙☀️  

---

## 📜 License  

This project is open-source and free to use for learning and productivity purposes.  
