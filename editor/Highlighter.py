import tkinter as tk

from Common.Utils import parse_language_file, parse_theme_file


class Highlighter:
    def __init__(self, text_widget, language='kotlin', theme='dracula'):
        self.language_file = parse_language_file(language=language)
        self.theme_file = parse_theme_file(theme=theme)
        self.text_widget = text_widget
        self.disallowed_previous_chars = ["_", "-", "."]
        self.configure_tags()

        self.text_widget.bind('<KeyRelease>', self.on_key_release)

    def configure_tags(self):
        for category in self.theme_file['categories'].keys():
            color = self.theme_file['categories'][category]['color']
            self.text_widget.tag_configure(category, foreground=color)
        self.text_widget.tag_configure("number", foreground=self.theme_file['numbers']['color'])
        self.text_widget.tag_configure("string", foreground=self.theme_file['strings']['color'])
        self.text_widget.tag_configure("comment", foreground=self.theme_file['comments']['color'])

    def highlight_string_num_comment(self, regex, tag):
        length = tk.IntVar()
        start = 1.0
        idx = self.text_widget.search(regex, start, stopindex=tk.END, regexp=1, count=length)
        while idx:
            end = f"{idx}+{length.get()}c"
            self.text_widget.tag_add(tag, idx, end)
            start = end
            idx = self.text_widget.search(regex, start, stopindex=tk.END, regexp=1, count=length)

    def highlight(self, event=None):
        # # Remove outdated tags
        # for tag in self.text_widget.tag_names():
        #     self.text_widget.tag_remove(tag, "1.0", tk.END)

        length = tk.IntVar()

        # Keywords highlighting
        for category in self.language_file['categories']:
            matches = self.language_file['categories'][category]['matches']
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

        # Number Highlighting
        self.highlight_string_num_comment(self.language_file['numbers']['match'], "number")

        # String Highlighting
        self.highlight_string_num_comment(self.language_file['strings']['match'], "string")

        # Comment Highlighting
        self.highlight_string_num_comment(self.language_file['comments']['match'], "comment")
    
    def on_key_release(self, event=None):
        self.highlight()