import json
import os
from datetime import datetime
from typing import Dict, Optional


class ActivityLogger:
    """Logs activity data to files for later analysis."""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        
        # Create logs directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            print(f"📁 Created logs directory: {log_dir}")
        
        # File paths
        self.sessions_file = os.path.join(log_dir, "sessions.jsonl")
        self.daily_file = os.path.join(log_dir, "daily_summary.jsonl")
        self.nudges_file = os.path.join(log_dir, "nudges.jsonl")
    
    def log_session(self, site: str, duration_minutes: float, start_time: datetime, end_time: datetime):
        """Log a completed browsing session."""
        session_data = {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().date().isoformat(),
            "site": site,
            "duration_minutes": round(duration_minutes, 2),
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "day_of_week": datetime.now().strftime("%A"),
            "hour": datetime.now().hour
        }
        
        self._append_jsonl(self.sessions_file, session_data)
        print(f"📝 Logged session: {site} - {duration_minutes:.1f} minutes")
    
    def log_nudge(self, nudge_data: Dict):
        """Log when a nudge was sent."""
        nudge_log = {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().date().isoformat(),
            "site": nudge_data.get("site"),
            "type": nudge_data.get("type"),
            "severity": nudge_data.get("severity"),
            "session_time": nudge_data.get("session_time"),
            "total_today": nudge_data.get("total_today"),
            "limit": nudge_data.get("limit")
        }
        
        self._append_jsonl(self.nudges_file, nudge_log)
        print(f"📝 Logged nudge: {nudge_data.get('type')} for {nudge_data.get('site')}")
    
    def log_daily_summary(self, summary: Dict):
        """Log end-of-day summary."""
        daily_log = {
            "timestamp": datetime.now().isoformat(),
            "date": summary.get("date"),
            "sites": summary.get("sites", {})
        }
        
        self._append_jsonl(self.daily_file, daily_log)
        print(f"📝 Logged daily summary for {summary.get('date')}")
    
    def _append_jsonl(self, filepath: str, data: Dict):
        """Append JSON line to file."""
        try:
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(json.dumps(data) + '\n')
        except Exception as e:
            print(f"❌ Error logging to {filepath}: {e}")
    
    def get_sessions_count(self) -> int:
        """Get total number of logged sessions."""
        if not os.path.exists(self.sessions_file):
            return 0
        
        try:
            with open(self.sessions_file, 'r', encoding='utf-8') as f:
                return sum(1 for _ in f)
        except:
            return 0
    
    def get_recent_sessions(self, limit: int = 10):
        """Get the most recent sessions."""
        if not os.path.exists(self.sessions_file):
            return []
        
        sessions = []
        try:
            with open(self.sessions_file, 'r', encoding='utf-8') as f:
                for line in f:
                    sessions.append(json.loads(line))
        except Exception as e:
            print(f"Error reading sessions: {e}")
        
        return sessions[-limit:] if sessions else []


# Test the logger
if __name__ == "__main__":
    print("Testing ActivityLogger...\n")
    
    logger = ActivityLogger()
    
    # Test logging a session
    from datetime import timedelta
    now = datetime.now()
    logger.log_session(
        site="youtube.com",
        duration_minutes=15.5,
        start_time=now - timedelta(minutes=15),
        end_time=now
    )
    
    # Test logging a nudge
    test_nudge = {
        "type": "NUDGE",
        "severity": "info",
        "site": "youtube.com",
        "session_time": 15.5,
        "total_today": 45.2,
        "limit": 60
    }
    logger.log_nudge(test_nudge)
    
    # Test logging daily summary
    test_summary = {
        "date": datetime.now().date().isoformat(),
        "sites": {
            "youtube.com": {
                "time_spent": 45.2,
                "limit": 60,
                "percentage": 75.3,
                "over_limit": False
            }
        }
    }
    logger.log_daily_summary(test_summary)
    
    print(f"\n✅ Logs created in 'logs/' directory")
    print(f"📊 Total sessions logged: {logger.get_sessions_count()}")
    
    print("\n📁 Recent sessions:")
    for session in logger.get_recent_sessions(5):
        print(f"   {session['site']}: {session['duration_minutes']} min on {session['date']}")