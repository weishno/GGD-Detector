import pyautogui
import time

class ScreenshotCollector:
    def __init__(self, interval=5):
        self.interval = interval

    def collect_screenshots(self, duration):
        end_time = time.time() + duration
        while time.time() < end_time:
            screenshot = pyautogui.screenshot()
            screenshot.save(f'screenshot_{int(time.time())}.png')
            time.sleep(self.interval)

if __name__ == '__main__':
    collector = ScreenshotCollector(interval=5)
    collector.collect_screenshots(duration=60)  # Collect screenshots for 60 seconds
