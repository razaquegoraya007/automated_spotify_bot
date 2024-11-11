from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

class SpotifyActions:
    def __init__(self, bot):
        """Initialize with a reference to the SpotifyBot instance."""
        self.bot = bot

    def play_song(self):
        """Plays a song in the Spotify Web Player."""
        try:
            play_button = WebDriverWait(self.bot.driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='control-button-playpause']"))
            )
            play_button.click()
            print("Song is playing.")
        except Exception as e:
            print("Failed to play song:", e)

    def like_song(self):
        """Likes the currently playing song based on a probability."""
        try:
            if random.random() < self.bot.like_prob:
                like_button = WebDriverWait(self.bot.driver, 20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='control-button-like']"))
                )
                like_button.click()
                print("Song liked.")
            else:
                print("Skipped liking the song.")
        except Exception as e:
            print("Failed to like song:", e)

    def add_to_playlist(self, playlist_name="My Playlist"):
        """Adds the current song to a specified playlist."""
        try:
            add_button = WebDriverWait(self.bot.driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Add to Playlist']"))
            )
            add_button.click()

            playlist_button = WebDriverWait(self.bot.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, f"//span[text()='{playlist_name}']"))
            )
            playlist_button.click()
            print(f"Song added to playlist: {playlist_name}")
        except Exception as e:
            print("Failed to add song to playlist:", e)

    def simulate_human_behavior(self):
        """Simulates human behavior by adding random pauses and movements."""
        try:
            pause_duration = random.uniform(2, 5)
            print(f"Simulating human behavior with a {pause_duration:.2f} second pause.")
            time.sleep(pause_duration)
        except Exception as e:
            print("Failed to simulate human behavior:", e)
