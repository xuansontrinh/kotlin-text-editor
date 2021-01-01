import tkinter as tk

# Implement line number for text editor using tk Canvas
class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None
        self.config(width=100)

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
            self.create_text(90,y,anchor=tk.NE, text=linenum, font=kwargs['font'])
            i = self.textwidget.index("%s+1line" % i)