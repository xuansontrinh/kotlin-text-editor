import tkinter as tk

from Common.Utils import parse_language_file, parse_theme_file


class Highlighter:
    def __init__(self, text_widget, language='kotlin', theme='dracula'):
        self.language = parse_language_file(language=language)
        self.theme = parse_theme_file(theme=theme)
        self.text_widget = text_widget
        self.disallowed_previous_chars = ["_", "-", "."]
        self.configure_tags()

        self.text_widget.bind('<KeyRelease>', self.on_key_release)

    def configure_tags(self):
        for category in self.theme['categories'].keys():
            color = self.theme['categories'][category]['color']
            self.text_widget.tag_configure(category, foreground=color)

    def highlight(self, event=None):

        length = tk.IntVar()

        # Keywords highlighting
        for category in self.language['categories']:
            matches = self.language['categories'][category]['matches']
            for keyword in matches:
                start = 1.0
                keyword = "(^|\W)" + keyword + "[^A-Za-z0-9_-]"
                idx = self.text_widget.search(keyword, start,\
                    stopindex=tk.END, count=length, regexp=1)
                while idx:
                    end = f"{idx}+{length.get() - 1}c"
                    self.text_widget.tag_add(category, idx, end)
                    start = end
                    idx = self.text_widget.search(keyword, start, stopindex=tk.END, count=length, regexp=1)

    
    def on_key_release(self, event=None):
        self.highlight()