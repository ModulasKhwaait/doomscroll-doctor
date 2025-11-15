import pystray
from PIL import Image, ImageDraw
from threading import Thread
import time
from monitor import ActivityMonitor


class DoomScrollDoctorTray:
    """System tray application for DoomScrollDoctor."""
    
    def __init__(self):
        self.monitor = ActivityMonitor()
        self.running = False
        self.icon = None
        
    def create_icon_image(self):
        """Create a simple icon image."""
        # Create a simple icon (green circle with 'D')
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), 'white')
        dc = ImageDraw.Draw(image)
        
        # Draw green circle
        dc.ellipse([4, 4, width-4, height-4], fill='#4CAF50', outline='#2E7D32')
        
        # Draw 'D' in white (simplified)
        dc.text((20, 15), 'D', fill='white')
        
        return image
    
    def monitor_loop(self):
        """Main monitoring loop running in background thread."""
        print("🩺 DoomScrollDoctor monitoring started...")
        
        while self.running:
            try:
                nudge = self.monitor.update_session()
                
                if nudge:
                    self.monitor.notifier.send_nudge(nudge)
                
                time.sleep(2)
            except Exception as e:
                print(f"Error in monitor loop: {e}")
                time.sleep(5)
    
    def show_stats(self, icon, item):
        """Show current stats (when clicked)."""
        summary = self.monitor.get_daily_summary()
        self.monitor.notifier.send_daily_summary(summary)
    
    def quit_app(self, icon, item):
        """Quit the application."""
        print("\n📊 Generating final summary...")
        summary = self.monitor.get_daily_summary()
        self.monitor.notifier.send_daily_summary(summary)
        
        self.running = False
        icon.stop()
        print("👋 DoomScrollDoctor stopped. Stay focused!")
    
    def run(self):
        """Start the system tray app."""
        self.running = True
        
        # Start monitoring in background thread
        monitor_thread = Thread(target=self.monitor_loop, daemon=True)
        monitor_thread.start()
        
        # Create system tray icon
        icon_image = self.create_icon_image()
        
        menu = pystray.Menu(
            pystray.MenuItem("📊 Show Stats", self.show_stats),
            pystray.MenuItem("❌ Quit", self.quit_app)
        )
        
        self.icon = pystray.Icon(
            "DoomScrollDoctor",
            icon_image,
            "DoomScrollDoctor - Monitoring",
            menu
        )
        
        # Show startup notification
        self.monitor.notifier.send_notification(
            title="🩺 DoomScrollDoctor Started",
            message="Now monitoring your activity.\nRight-click the tray icon to see stats or quit.",
            timeout=5
        )
        
        # Run the icon (this blocks)
        self.icon.run()


if __name__ == "__main__":
    print("Starting DoomScrollDoctor with system tray...")
    app = DoomScrollDoctorTray()
    app.run()