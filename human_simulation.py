import pyautogui
import time
import random
import string

class HumanSimulation:
    def simulate_human_mouse_movements(self):
        """Simulates human-like mouse movements with small random pauses."""
        for _ in range(random.randint(5, 10)):
            x, y = random.randint(100, 800), random.randint(100, 600)
            pyautogui.moveTo(x, y, duration=random.uniform(0.1, 0.5))
            time.sleep(random.uniform(0.05, 0.2))

    def random_typing(self):
        """Simulates random typing to mimic human interaction."""
        text = ''.join(random.choices(string.ascii_lowercase + ' ', k=random.randint(5, 15)))
        for char in text:
            pyautogui.typewrite(char)
            time.sleep(random.uniform(0.05, 0.2))