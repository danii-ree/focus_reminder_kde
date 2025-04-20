import cv2
import numpy as np
import subprocess
import pytesseract
import time
import os
import sys
import argparse
import tempfile
import webbrowser
import random
import signal
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'focus_reminder.log')),
        logging.StreamHandler()
    ]
)

class ScreenMonitor:
    def __init__(self, keywords_file='keywords.txt'):
        # Set up signal handlers
        signal.signal(signal.SIGTERM, self.handle_shutdown)
        signal.signal(signal.SIGINT, self.handle_shutdown)
        
        # Check if Tesseract is properly installed
        try:
            pytesseract.get_tesseract_version()
        except Exception as e:
            logging.error("Tesseract OCR is not properly installed or configured.")
            logging.error("Please install Tesseract and its English language data:")
            logging.error("sudo pacman -S tesseract tesseract-data-eng")
            sys.exit(1)
            
        self.keywords = self.load_keywords(keywords_file)
        self.distraction_count = 0
        self.base_interval = 5  # Base interval in seconds
        self.interval_increase = 2  # How much to increase interval each time
        self.max_interval = 30  # Maximum interval in seconds
        self.html_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'focus_reminder.html')
        self.intro_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'intro.html')
        self.running = True
        
        # Show introduction and clear storage
        self.show_introduction()
        logging.info("Focus Reminder service started")

    def handle_shutdown(self, signum, frame):
        logging.info("Shutting down Focus Reminder service")
        self.running = False

    def load_keywords(self, filename):
        try:
            with open(filename, 'r') as f:
                return [line.strip().lower() for line in f if line.strip()]
        except FileNotFoundError:
            return ['gaming', 'entertainment', 'funny', 'comedy', 'music']

    def capture_screen(self):
        # Create a temporary file for the screenshot
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            temp_path = tmp.name
        
        try:
            # Use spectacle to capture the screen
            # -b: background mode (no GUI)
            # -n: no notification
            # -o: output file
            subprocess.run(['spectacle', '-b', '-n', '-o', temp_path], check=True)
            
            # Read the image using OpenCV
            image = cv2.imread(temp_path)
            if image is None:
                raise Exception("Failed to read the screenshot")
            
            return image
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def extract_text(self, image):
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # Apply thresholding
            _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            # Extract text using Tesseract
            text = pytesseract.image_to_string(binary)
            return text.lower()
        except Exception as e:
            logging.error(f"Error during text extraction: {str(e)}")
            return ""  # Return empty string if text extraction fails

    def check_keywords(self, text):
        for keyword in self.keywords:
            if keyword in text:
                return True
        return False

    def get_current_interval(self):
        # Calculate base interval
        current_interval = self.base_interval + (self.distraction_count * self.interval_increase)
        
        # Add random increase between 5-15 seconds
        random_increase = random.randint(5, 15)
        current_interval += random_increase
        
        # Ensure we don't exceed max interval
        return min(current_interval, self.max_interval)

    def show_focus_reminder(self):
        self.distraction_count += 1
        current_interval = self.get_current_interval()
        logging.info(f"Distraction detected! (Count: {self.distraction_count}, Next check in {current_interval} seconds)")
        
        # Open the HTML file in a new browser window with wait time parameter
        url = f"file://{self.html_file}?wait={current_interval}"
        webbrowser.open_new(url)

    def show_introduction(self):
        try:
            # Open the introduction page
            webbrowser.open_new(f"file://{self.intro_file}")
            # Wait for the introduction to be shown
            time.sleep(2)
        except Exception as e:
            logging.error(f"Error showing introduction: {str(e)}")

    def monitor(self):
        logging.info("Starting screen monitoring...")
        try:
            # Reset distraction count when starting
            self.distraction_count = 0
            while self.running:
                try:
                    # Capture screen
                    screen = self.capture_screen()
                    # Extract text
                    text = self.extract_text(screen)
                    # Check for keywords
                    if self.check_keywords(text):
                        self.show_focus_reminder()
                    time.sleep(self.get_current_interval())
                except Exception as e:
                    logging.error(f"Error in monitoring loop: {str(e)}")
                    time.sleep(5)  # Wait before retrying
        except KeyboardInterrupt:
            logging.info("\nMonitoring stopped")
        finally:
            logging.info(f"Total distractions detected: {self.distraction_count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--service', action='store_true', help='Run as systemd service')
    args = parser.parse_args()

    # Create keywords file if it doesn't exist
    if not os.path.exists('keywords.txt'):
        with open('keywords.txt', 'w') as f:
            f.write("gaming\nentertainment\nfunny\ncomedy")
    
    monitor = ScreenMonitor()
    monitor.monitor() 