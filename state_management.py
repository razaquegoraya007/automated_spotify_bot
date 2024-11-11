from selenium.webdriver.common.by import By
import time

class StateManagement:
    def __init__(self, bot):
        """Initialize with reference to the SpotifyBot instance."""
        self.bot = bot
        self.previous_state = None

    def capture_current_state(self):
        """Captures the current state of the page."""
        try:
            
            play_button = self.bot.driver.find_element(By.XPATH, "//button[@data-testid='control-button-playpause']")
            self.previous_state = play_button.is_displayed()
        except Exception:
            self.previous_state = None

    def check_for_change(self):
        """Checks if there has been a change in the page state."""
        current_state = None
        try:
            play_button = self.bot.driver.find_element(By.XPATH, "//button[@data-testid='control-button-playpause']")
            current_state = play_button.is_displayed()
        except Exception:
            pass

        
        if current_state != self.previous_state:
            self.previous_state = current_state
            return True
        return False