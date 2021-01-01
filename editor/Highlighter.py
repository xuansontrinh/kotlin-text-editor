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
            for to_del_tag in self.text_widget.tag_names():
                if to_del_tag != 'sel':
                    self.text_widget.tag_remove(to_del_tag, idx, end)
            self.text_widget.tag_add(tag, idx, end)
            start = end
            idx = self.text_widget.search(regex, start, stopindex=tk.END, regexp=1, count=length)

    def highlight(self, event=None):
        # # Remove outdated tags
        for to_del_tag in self.text_widget.tag_names():
            if to_del_tag != 'sel':
                self.text_widget.tag_remove(to_del_tag, "1.0", tk.END)

        length = tk.IntVar()

        # Keywords highlighting
        for category in self.language_file['categories']:
            matches = self.language_file['categories'][category]['matches']
            for keyword in matches:
                start = 1.0
                keyword = f"\m{keyword}(?!\w)"
                idx = self.text_widget.search(keyword, start,\
                    stopindex=tk.END, count=length, regexp=1)
                while idx:                   
                    end = f"{idx}+{length.get()}c"
                    self.text_widget.tag_add(category, idx, end)
                    start = end
                    idx = self.text_widget.search(keyword, start, stopindex=tk.END, count=length, regexp=1)
        
        # Comment Highlighting
        for match in self.language_file['comments']['matches']:
            self.highlight_string_num_comment(match, "comment")

        # Number Highlighting
        self.highlight_string_num_comment(f"\m{self.language_file['numbers']['match']}(?!\w)", "number")

        # String Highlighting
        self.highlight_string_num_comment(f"(^|\W){self.language_file['strings']['match']}(?!\w)", "string")

    
    def on_key_release(self, event=None):
        self.highlight()