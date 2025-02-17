import tkinter as tk
from tkinter import ttk
import math
import random

# Define a modern color scheme
COLOR_SCHEME = {
    "background": "#23272a",  # Dark background
    "primary": "#4CAF50",    # Green primary color
    "accent": "#FFC107",     # Yellow accent color
    "text": "#FFFFFF",       # White text color
    "secondary_bg": "#2c2f33" # Slightly lighter background for contrast
}

class AnimationHandler:
    def __init__(self, parent):
        self.parent = parent
        # Create a custom style for the progress bar
        style = ttk.Style(parent)
        style.theme_use('clam')
        style.configure("Modern.Horizontal.TProgressbar",
                        troughcolor=COLOR_SCHEME["secondary_bg"],  # Use secondary background color
                        background=COLOR_SCHEME["primary"],
                        bordercolor=COLOR_SCHEME["primary"],
                        lightcolor=COLOR_SCHEME["primary"],
                        darkcolor=COLOR_SCHEME["primary"])
        self.progress_bar = ttk.Progressbar(
            parent, mode="indeterminate", style="Modern.Horizontal.TProgressbar"
        )
        
    def start(self, **pack_options):
        """
        Packs and starts the classic progress bar animation.
        Accepts tkinter pack options.
        """
        self.progress_bar.pack(**pack_options)
        self.progress_bar.start(10)
        
    def stop(self):
        """
        Stops the progress bar animation and hides it.
        """
        self.progress_bar.stop()
        self.progress_bar.pack_forget()


def animate_label(label, text_list, delay=500):
    """
    Cycles through the provided text_list and updates the label every 'delay' milliseconds.
    
    Args:
        label (tk.Label): The label to animate.
        text_list (list): List of texts to display.
        delay (int): Milliseconds delay between text changes.
    """
    def cycle(index=0):
        label.config(text=text_list[index], fg=COLOR_SCHEME["accent"])
        label.after(delay, lambda: cycle((index + 1) % len(text_list)))
    cycle()


def modern_glitch_label(label, text, glitch_count=5, delay=100):
    """
    Applies a subtle glitch effect to a label by randomly altering parts of its text.
    
    Args:
        label (tk.Label): The label to animate.
        text (str): The original text for the label.
        glitch_count (int): Number of characters to randomly alter.
        delay (int): Milliseconds delay between glitch iterations.
    """
    def glitch():
        if random.random() < 0.3:
            text_chars = list(text)
            indices = random.sample(range(len(text_chars)), min(glitch_count, len(text_chars)))
            for idx in indices:
                text_chars[idx] = random.choice(['@', '#', '$', '%', '&', '!'])
            label.config(text=''.join(text_chars), fg=COLOR_SCHEME["accent"])
        else:
            label.config(text=text, fg=COLOR_SCHEME["text"])
        label.after(delay, glitch)
    glitch()