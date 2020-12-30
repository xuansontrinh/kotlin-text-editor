import tkinter as tk

class LineNumbers(tk.Text):
    def __init__(self, master, text_widget, **kwargs):
        super().__init__(master, **kwargs)
        self.text_widget = text_widget
        self.text_widget.bind('<KeyPress>', self.on_key_press)
        self.tag_configure("right", justify=tk.RIGHT)

        self.insert(1.0, '1')
        self.tag_add("right", 1.0, "end")
        self.configure(state='disabled', width=2)

    def on_key_press(self, event=None):
        final_index = str(self.text_widget.index(tk.END))
        num_of_lines = final_index.split('.')[0]
        line_numbers_string = "\n".join(str(no + 1) for no in range(int(num_of_lines)))
        width = len(str(num_of_lines)) + 1
        self.configure(state='normal', width=width)
        self.delete(1.0, tk.END)

        self.insert(1.0, line_numbers_string)
        self.tag_add("right", 1.0, "end")
        self.configure(state='disabled')