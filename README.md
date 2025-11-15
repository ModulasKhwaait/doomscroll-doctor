# 🩺 DoomScrollDoctor

A Python desktop app that helps you break free from doomscrolling by monitoring your screen time and sending friendly (or not-so-friendly) nudges when you've been on distracting sites too long.

## 😅 The Problem

Ever open YouTube "just for 5 minutes" and suddenly it's 2 hours later? Yeah, me too. That's why I built this.

## 💡 The Solution

DoomScrollDoctor runs quietly in the background, tracks how long you spend on time-wasting sites, and sends you desktop notifications to get you back on track.

## ✨ Features

- **Real-time monitoring** - Tracks active browser windows
- **Smart detection** - Recognizes YouTube, Reddit, Twitter, Facebook, and more
- **Configurable limits** - Set daily time limits per site
- **Friendly nudges** - Desktop notifications at customizable intervals
- **Daily summaries** - See how you spent your time
- **Privacy-first** - All data stays on YOUR machine (no external tracking)

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Windows (currently Windows-only due to window detection)

### Installation
```bash
# Clone the repository
git clone https://github.com/ModulasKhwaait/doomscroll-doctor.git
cd doomscroll-doctor

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Copy sample config
copy config.sample.json config.json  # Windows
# cp config.sample.json config.json  # Mac/Linux

# Edit config.json to set your preferences
```

### Usage

**Option 1: Command Line**
```bash
python src/monitor.py
```

**Option 2: Double-click launcher (Windows)**
```
Double-click run_doctor.bat
```

The app will run in the background and send notifications when needed.

Press `Ctrl+C` to stop and see your daily summary.

## ⚙️ Configuration

Edit `config.json` to customize:
```json
{
  "tracked_sites": {
    "youtube.com": {
      "daily_limit": 60,        // Max minutes per day
      "nudge_interval": 15,     // Remind every X minutes
      "hard_block": false       // Block after limit (not implemented yet)
    }
  }
}
```

### Add Your Own Sites

Just add entries to `tracked_sites`:
```json
"instagram.com": {
  "daily_limit": 30,
  "nudge_interval": 10,
  "hard_block": false
}
```

## 📊 Example Notifications

**Friendly Nudge:**
```
👋 Friendly reminder!

You've been on youtube.com for 15 minutes.
Time remaining today: 45 minutes
```

**Warning:**
```
⚠️  You've exceeded your daily limit on youtube.com!

Time today: 65 minutes
Limit: 60 minutes

Maybe it's time for a break? 🤔
```

## 🔒 Privacy & Ethics

**DoomScrollDoctor is for personal productivity, not surveillance.**

- ✅ All data stays on YOUR machine (no cloud, no servers)
- ✅ Tracks only window titles, not content or keystrokes
- ✅ You control when it runs and what it monitors
- ✅ Open source - verify exactly what it does
- ✅ Designed for self-improvement, not spying

**⚠️ Important:** Only install this on devices YOU own. Installing monitoring software on others' devices without consent may be illegal.

## 🛠️ Technical Stack

- **Python 3.9+**
- **psutil** - Process and system monitoring
- **pywin32** - Windows API for window detection
- **plyer** - Cross-platform desktop notifications

## 📁 Project Structure
```
doomscroll-doctor/
├── src/
│   ├── monitor.py       # Main monitoring logic
│   ├── notifier.py      # Desktop notifications
│   ├── blocker.py       # (Future) Hard blocking
│   └── ui.py            # (Future) GUI dashboard
├── config.json          # Your personal settings (not in git)
├── config.sample.json   # Template configuration
├── run_doctor.bat       # Windows launcher
└── requirements.txt
```

## 🎯 Real-World Use Case

This project was born out of a real problem: losing entire afternoons to YouTube shorts. Now I use it daily to:
- Stay aware of my screen time
- Build better browsing habits
- Actually finish my side projects (like this one!)

## 🔮 Future Enhancements

- [ ] Hard blocking (prevent access after limit)
- [ ] System tray GUI with live stats
- [ ] Weekly/monthly trend reports
- [ ] Pomodoro timer integration
- [ ] "Focus mode" that blocks all distractions
- [ ] Cross-platform support (Mac, Linux)
- [ ] Browser extension version

## 👨‍💻 About

Built by ModulasKhwaait as a practical solution to a real problem, and as a portfolio project demonstrating:
- Python desktop application development
- System monitoring and Windows API integration
- Real-time data processing
- User notification systems
- Ethical software design

## 🤝 Contributing

This is a personal project, but suggestions and improvements are welcome! Feel free to open issues or PRs.

## 📄 License

MIT License - Use it, modify it, just don't blame me if you still end up watching cat videos. 😺

---

**If this helped you reclaim your time, give it a ⭐!**