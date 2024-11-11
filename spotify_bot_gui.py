# src/interface/spotify_bot_gui.py

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from initialization.spotify_bot import SpotifyBot  # Assuming this is the bot class
from core_functions.spotify_actions import SpotifyActions  # Adjust this import as necessary

class SpotifyBotGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Spotify Bot GUI")
        self.geometry("800x600")
        self.configure(bg="#1DB954")

        # Initialize bot instance for actions
        self.bot = SpotifyBot()
        self.actions = SpotifyActions(self.bot)  # Use SpotifyActions with self.bot

        self.accounts = []
        self.executor = ThreadPoolExecutor(max_workers=5)

        self.create_widgets()

    def create_widgets(self):
        # Account Management Section
        self.account_frame = ttk.LabelFrame(self, text="Account Management")
        self.account_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.account_label = ttk.Label(self.account_frame, text="Accounts:")
        self.account_label.grid(row=0, column=0, padx=5, pady=5)

        self.account_listbox = tk.Listbox(self.account_frame, height=5)
        self.account_listbox.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.add_account_button = ttk.Button(self.account_frame, text="Add Account", command=self.add_account)
        self.add_account_button.grid(row=2, column=0, padx=5, pady=5)

        self.remove_account_button = ttk.Button(self.account_frame, text="Remove Account", command=self.remove_account)
        self.remove_account_button.grid(row=2, column=1, padx=5, pady=5)

        # Parameter Settings Section
        self.parameter_frame = ttk.LabelFrame(self, text="Settings")
        self.parameter_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.create_parameter_widgets()

        # Control Buttons Section
        self.controls_frame = ttk.LabelFrame(self, text="Controls")
        self.controls_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

        self.start_button = ttk.Button(self.controls_frame, text="Start", command=self.start_bot)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)

        self.stop_button = ttk.Button(self.controls_frame, text="Stop", command=self.stop_bot)
        self.stop_button.grid(row=0, column=1, padx=5, pady=5)

        # Monitor Section
        self.monitor_frame = ttk.LabelFrame(self, text="Monitor")
        self.monitor_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.monitor_text = ScrolledText(self.monitor_frame, state="disabled", height=10)
        self.monitor_text.grid(row=0, column=0, padx=5, pady=5)

    def create_parameter_widgets(self):
        """Creates parameter input fields for configurable settings."""
        settings = [
            ("Play Probability:", "play_prob_entry"),
            ("Like Probability:", "like_prob_entry"),
            ("Playlist Probability:", "playlist_prob_entry"),
            ("Skip Probability:", "skip_prob_entry"),
            ("Streaming Goal:", "streaming_goal_entry"),
            ("Main Artist URI:", "main_artist_entry")
        ]
        for i, (label, var) in enumerate(settings):
            ttk.Label(self.parameter_frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            entry = ttk.Entry(self.parameter_frame)
            entry.grid(row=i, column=1, padx=5, pady=5)
            setattr(self, var, entry)

    def add_account(self):
        """Opens a dialog to add a new account with email, password, and proxy."""
        account_window = tk.Toplevel(self)
        account_window.title("Add Account")

        tk.Label(account_window, text="Email:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        email_entry = tk.Entry(account_window)
        email_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(account_window, text="Password:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        password_entry = tk.Entry(account_window, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(account_window, text="Proxy:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        proxy_entry = tk.Entry(account_window)
        proxy_entry.grid(row=2, column=1, padx=10, pady=5)

        def save_account():
            email = email_entry.get()
            password = password_entry.get()
            proxy = proxy_entry.get()
            if email and password:
                self.accounts.append({"email": email, "password": password, "proxy": proxy})
                self.account_listbox.insert(tk.END, email)
                account_window.destroy()
            else:
                messagebox.showwarning("Warning", "Please fill in all fields!")

        tk.Button(account_window, text="Save", command=save_account).grid(row=3, column=1, padx=10, pady=5, sticky="e")

    def remove_account(self):
        """Removes the selected account from the list."""
        selected_index = self.account_listbox.curselection()
        if selected_index:
            self.account_listbox.delete(selected_index)
            del self.accounts[selected_index[0]]

    def log_to_monitor(self, message):
        """Logs a message to the monitor window."""
        self.monitor_text.config(state="normal")
        self.monitor_text.insert(tk.END, f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
        self.monitor_text.yview(tk.END)
        self.monitor_text.config(state="disabled")

    def start_bot(self):
        """Starts bot tasks for each account."""
        try:
            params = {
                "play_prob": float(self.play_prob_entry.get()),
                "like_prob": float(self.like_prob_entry.get()),
                "playlist_prob": float(self.playlist_prob_entry.get()),
                "skip_prob": float(self.skip_prob_entry.get()),
                "streaming_goal": int(self.streaming_goal_entry.get()),
                "main_artist_uri": self.main_artist_entry.get(),
            }
        except ValueError:
            messagebox.showerror("Error", "Please enter valid values for all parameters.")
            return

        for account in self.accounts:
            self.executor.submit(self.run_bot_for_account, account, params)

    def run_bot_for_account(self, account, params):
        """Runs the bot for a specific account."""
        options = Options()
        options.add_argument("--headless")  # Headless mode for background execution
        options.add_argument("--window-size=1920,1080")
        if account.get("proxy"):
            options.add_argument(f"--proxy-server={account['proxy']}")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

        try:
            bot = SpotifyActions(driver, **params)
            bot.login(account["email"], account["password"])
            bot.perform_streaming(params["main_artist_uri"])
            self.log_to_monitor(f"Bot started for {account['email']}")
        except Exception as e:
            self.log_to_monitor(f"Error for {account['email']}: {str(e)}")
        finally:
            driver.quit()

    def stop_bot(self):
        """Stops all running bot tasks."""
        self.executor.shutdown(wait=False)
        self.executor = ThreadPoolExecutor(max_workers=5)
        self.log_to_monitor("All bots stopped")


if __name__ == "__main__":
    app = SpotifyBotGUI()
    app.mainloop()
