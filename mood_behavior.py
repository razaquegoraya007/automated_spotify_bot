import random
import numpy as np  
class MoodBehavior:
    def __init__(self, bot):
        """Initialize with a reference to the SpotifyBot instance."""
        self.bot = bot

    def set_random_mood(self):
        """Sets a random mood that influences bot behavior."""
        moods = ["happy", "neutral", "sad"]
        self.bot.current_mood = random.choice(moods)

    def adjust_probabilities_based_on_mood(self):
        """Adjust play and like probabilities based on predicted mood."""
        if self.bot.model:
           
            mood_prediction = self.bot.model.predict(np.array([[1]]))[0][0] 
            if mood_prediction > 0.5:
                self.bot.play_prob += 0.1
                self.bot.like_prob += 0.05
            else:
                self.bot.play_prob -= 0.1
                self.bot.like_prob -= 0.05

            
            self.bot.play_prob = min(max(self.bot.play_prob, 0), 1)
            self.bot.like_prob = min(max(self.bot.like_prob, 0), 1)
