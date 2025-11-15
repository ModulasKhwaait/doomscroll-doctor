import psutil
import time
from datetime import datetime, timedelta
from typing import Dict, Optional
import json
import os
# Windows-specific import
try:
    import win32gui  # type: ignore
    WINDOWS_AVAILABLE = True
except ImportError:
    WINDOWS_AVAILABLE = False
    print("⚠️  win32gui not available. Window detection may not work.")

from notifier import Notifier


class ActivityMonitor:
    """Monitors browser activity and tracks time on specific sites."""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.load_config()
        
        # Track current session
        self.current_site: Optional[str] = None
        self.session_start: Optional[datetime] = None
        self.last_nudge_time: Optional[datetime] = None
        
        # Daily stats
        self.daily_stats: Dict[str, float] = {}  # site -> total minutes today
        self.last_reset = datetime.now().date()

        # Notifier
        self.notifier = Notifier()

    
    def load_config(self):
        """Load configuration or create default."""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                config = json.load(f)
        else:
            # Default config
            config = {
                "tracked_sites": {
                    "youtube.com": {
                        "daily_limit": 60,  # minutes
                        "nudge_interval": 15,  # remind every 15 min
                        "hard_block": False
                    },
                    "reddit.com": {
                        "daily_limit": 30,
                        "nudge_interval": 10,
                        "hard_block": False
                    },
                    "twitter.com": {
                        "daily_limit": 30,
                        "nudge_interval": 10,
                        "hard_block": False
                    },
                    "facebook.com": {
                        "daily_limit": 30,
                        "nudge_interval": 10,
                        "hard_block": False
                    }
                },
                "work_hours": {
                    "enabled": True,
                    "start": "09:00",
                    "end": "17:00",
                    "stricter_limits": True
                }
            }
            self.save_config(config)
        
        self.config = config
        self.tracked_sites = config["tracked_sites"]
    
    def save_config(self, config: dict):
        """Save configuration to file."""
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def get_active_window_title(self) -> str:
        """Get the title of the currently active window."""
        if not WINDOWS_AVAILABLE:
            return ""
        
        try:
            window = win32gui.GetForegroundWindow()
            title = win32gui.GetWindowText(window)
            # Uncomment for debugging:
            # print(f"🔍 Detected window: {title[:80]}")
            return title
        except Exception as e:
            # Only print errors occasionally to avoid spam
            return ""
    
    def detect_current_site(self) -> Optional[str]:
        """Detect which tracked site user is currently on."""
        window_title = self.get_active_window_title().lower()
        
        for site in self.tracked_sites.keys():
            if site.replace('.com', '') in window_title or site in window_title:
                return site
        
        return None
    
    def update_session(self):
        """Update current tracking session."""
        detected_site = self.detect_current_site()
        
        # Reset daily stats if it's a new day
        if datetime.now().date() != self.last_reset:
            self.daily_stats = {}
            self.last_reset = datetime.now().date()
        
        # If we just started viewing a tracked site
        if detected_site and not self.current_site:
            self.current_site = detected_site
            self.session_start = datetime.now()
            print(f"📱 Started viewing: {detected_site}")
        
        # If we switched sites or stopped viewing
        elif self.current_site and detected_site != self.current_site:
            self._end_session()
            if detected_site:
                self.current_site = detected_site
                self.session_start = datetime.now()
                print(f"📱 Switched to: {detected_site}")
        
        # If we're still on the same site, check if nudge needed
        elif self.current_site:
            return self.check_for_nudge()
        
        return None
    
    def _end_session(self):
        """End the current viewing session and update stats."""
        if self.current_site and self.session_start:
            duration = (datetime.now() - self.session_start).total_seconds() / 60
            
            if self.current_site not in self.daily_stats:
                self.daily_stats[self.current_site] = 0
            
            self.daily_stats[self.current_site] += duration
            
            print(f"⏱️  Ended session on {self.current_site}: {duration:.1f} minutes")
            print(f"📊 Total today: {self.daily_stats[self.current_site]:.1f} minutes")
            
            self.current_site = None
            self.session_start = None
    
    def check_for_nudge(self) -> Optional[Dict]:
        """Check if we need to send a nudge to the user."""
        if not self.current_site or not self.session_start:
            return None
        
        site_config = self.tracked_sites[self.current_site]
        current_session_minutes = (datetime.now() - self.session_start).total_seconds() / 60
        total_today = self.daily_stats.get(self.current_site, 0) + current_session_minutes
        
        daily_limit = site_config["daily_limit"]
        nudge_interval = site_config["nudge_interval"]
        
        # Check if we've hit daily limit
        if total_today >= daily_limit and site_config.get("hard_block", False):
            return {
                "type": "BLOCK",
                "site": self.current_site,
                "message": f"⛔ Daily limit reached for {self.current_site}!\n\nYou've spent {total_today:.0f}/{daily_limit} minutes today.\n\nTime to get back to work! 💪"
            }
        
        # Check if enough time has passed since last nudge
        minutes_since_last_nudge = 999  # Default to large number
        if self.last_nudge_time:
            minutes_since_last_nudge = (datetime.now() - self.last_nudge_time).total_seconds() / 60
        
        # Only nudge if we've been on the site for at least nudge_interval minutes
        # AND it's been at least nudge_interval minutes since the last nudge
        if current_session_minutes >= nudge_interval and minutes_since_last_nudge >= nudge_interval:
            self.last_nudge_time = datetime.now()
            
            time_remaining = daily_limit - total_today
            
            if time_remaining <= 0:
                severity = "warning"
                message = f"⚠️  You've exceeded your daily limit on {self.current_site}!\n\n" \
                        f"Time today: {total_today:.0f} minutes\n" \
                        f"Limit: {daily_limit} minutes\n\n" \
                        f"Maybe it's time for a break? 🤔"
            elif time_remaining <= 10:
                severity = "warning"
                message = f"⏰ Running low on time for {self.current_site}!\n\n" \
                        f"Time remaining: {time_remaining:.0f} minutes\n" \
                        f"Current session: {current_session_minutes:.0f} minutes"
            else:
                severity = "info"
                message = f"👋 Friendly reminder!\n\n" \
                        f"You've been on {self.current_site} for {current_session_minutes:.0f} minutes.\n" \
                        f"Time remaining today: {time_remaining:.0f} minutes"
            
            return {
                "type": "NUDGE",
                "severity": severity,
                "site": self.current_site,
                "message": message,
                "session_time": current_session_minutes,
                "total_today": total_today,
                "limit": daily_limit
            }
        
        return None
    
    def get_daily_summary(self) -> Dict:
        """Get summary of today's activity."""
        summary = {
            "date": str(datetime.now().date()),
            "sites": {}
        }
        
        for site, minutes in self.daily_stats.items():
            limit = self.tracked_sites[site]["daily_limit"]
            summary["sites"][site] = {
                "time_spent": minutes,
                "limit": limit,
                "percentage": (minutes / limit) * 100 if limit > 0 else 0,
                "over_limit": minutes > limit
            }
        
        return summary


# Test the monitor with notifications
if __name__ == "__main__":
    print("🩺 DoomScrollDoctor is now running!")
    print("="*50)
    print("Monitoring your activity...")
    print("You'll get desktop notifications when you need a nudge!")
    print("Press Ctrl+C to stop\n")
    
    monitor = ActivityMonitor()
    
    try:
        while True:
            nudge = monitor.update_session()
            
            if nudge:
                # Send notification instead of just printing
                monitor.notifier.send_nudge(nudge)
                
                # Still print to console for debugging
                print(f"\n📬 Nudge sent: {nudge['type']}")
            
            time.sleep(2)  # Check every 2 seconds
            
    except KeyboardInterrupt:
        print("\n\n📊 Generating Daily Summary...")
        summary = monitor.get_daily_summary()
        
        # Send summary notification
        monitor.notifier.send_daily_summary(summary)
        
        # Print to console too
        print("="*50)
        for site, stats in summary["sites"].items():
            print(f"\n{site}:")
            print(f"  Time spent: {stats['time_spent']:.1f} minutes")
            print(f"  Limit: {stats['limit']} minutes")
            print(f"  Status: {'⚠️  OVER LIMIT' if stats['over_limit'] else '✅ Within limit'}")
        
        print("\n👋 DoomScrollDoctor stopped. Stay focused!")