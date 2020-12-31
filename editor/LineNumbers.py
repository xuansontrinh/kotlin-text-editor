import tkinter as tk

class LineNumbers(tk.Text):
    def __init__(self, master, text_widget, **kwargs):
        super().__init__(master, **kwargs)
        self.text_widget = text_widget
        self.text_widget.bind('<<ViewScroll>>', self.onKeyPress)
        self.tag_configure("right", justify=tk.RIGHT)

        self.insert(1.0, '1')
        self.tag_add("right", 1.0, "end")
        self.configure(state='disabled', width=3)

    def onKeyPress(self, event=None):
        final_index = str(self.text_widget.index(tk.END))
        num_of_lines = final_index.split('.')[0]
        line_numbers_string = "\n".join(str(no + 1) for no in range(int(num_of_lines)))
        width = len(str(num_of_lines)) + 2
        self.configure(state='normal', width=width)
        self.delete(1.0, tk.END)

        self.insert(1.0, line_numbers_string)
        self.tag_add("right", 1.0, "end")
        self.configure(state='disabled')

class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args, **kwargs):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.config(width=len(linenum) + 2)
            self.create_text(2,y,anchor=tk.NW, text=linenum, font=kwargs['font'])
            i = self.textwidget.index("%s+1line" % i)