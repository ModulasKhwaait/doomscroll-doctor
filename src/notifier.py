from plyer import notification
import os


class Notifier:
    """Handles desktop notifications."""
    
    def __init__(self, app_name: str = "DoomScrollDoctor"):
        self.app_name = app_name
        # You can add an icon later if you want
        self.icon_path = None
    
    def send_notification(self, title: str, message: str, timeout: int = 10):
        """
        Send a desktop notification.
        
        Args:
            title: Notification title
            message: Notification message
            timeout: How long to display (seconds)
        """
        try:
            notification.notify(
                title=title,
                message=message,
                app_name=self.app_name,
                timeout=timeout,
                app_icon=self.icon_path  # None for now, can add custom icon later
            )
            print(f"📬 Notification sent: {title}")
        except Exception as e:
            print(f"❌ Failed to send notification: {e}")
            # Fallback to console
            print(f"\n{'='*50}")
            print(f"{title}")
            print(f"{message}")
            print(f"{'='*50}\n")
    
    def send_nudge(self, nudge_data: dict):
        """Send a nudge notification based on nudge data."""
        if nudge_data["type"] == "BLOCK":
            self.send_notification(
                title="⛔ DoomScrollDoctor - BLOCKED",
                message=nudge_data["message"],
                timeout=15
            )
        elif nudge_data["type"] == "NUDGE":
            severity = nudge_data.get("severity", "info")
            
            if severity == "warning":
                title = "⚠️ DoomScrollDoctor - Warning!"
                timeout = 15
            else:
                title = "👋 DoomScrollDoctor - Friendly Nudge"
                timeout = 10
            
            self.send_notification(
                title=title,
                message=nudge_data["message"],
                timeout=timeout
            )
    
    def send_daily_summary(self, summary: dict):
        """Send end-of-day summary notification."""
        sites = summary.get("sites", {})
        
        if not sites:
            message = "No time tracked today. Great job staying focused! 🎯"
        else:
            message = "Today's screen time:\n\n"
            for site, stats in sites.items():
                status = "⚠️" if stats["over_limit"] else "✅"
                message += f"{status} {site}: {stats['time_spent']:.0f}/{stats['limit']} min\n"
        
        self.send_notification(
            title="📊 DoomScrollDoctor - Daily Summary",
            message=message,
            timeout=20
        )


# Test the notifier
if __name__ == "__main__":
    print("Testing notifications...")
    
    notifier = Notifier()
    
    # Test basic notification
    notifier.send_notification(
        title="🩺 DoomScrollDoctor Test",
        message="If you see this, notifications are working! ✅",
        timeout=5
    )
    
    print("\nYou should see a notification pop up!")
    print("If not, check your Windows notification settings.")