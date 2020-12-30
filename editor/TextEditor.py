import tkinter as tk
from tkinter import font

from Highlighter import Highlighter
from LineNumbers import LineNumbers
from Common.Utils import parse_theme_file, FONT_FAMILY, FONT_SIZE_MAP, FONT_SIZE_DEFAULT


class TextEditor:
    def __init__(self, language='kotlin', theme='dracula'):

        self.language = language
        self.theme = theme
        self.window = tk.Tk()
        self.font_size = tk.IntVar()
        self.window.title('{} Text Editor'.format(self.language[0].upper() + self.language[1:]))

        self.theme_file = parse_theme_file(theme=self.theme)
        self.editor = tk.Text(
            self.window, 
            background=self.theme_file['background']['color'], 
            foreground=self.theme_file['foreground']['color'], 
            insertbackground=self.theme_file['foreground']['color'],
        )
        
        self.line_numbers = LineNumbers(
            self.window,
            self.editor
        )
        # self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        h = Highlighter(self.editor, language=self.language, theme=self.theme)

        self.buildMenuBar()

        self.output = tk.Text(
            self.window
        )
        # self.output.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

        # Layout Arrangement
        for i in range(20):
            self.window.columnconfigure(i, weight=1, uniform='son')
            # self.window.columnconfigure(i, weight=1)
        # self.window.columnconfigure(0, weight=1, uniform='fred')
        # self.window.columnconfigure(1, weight=1, uniform='fred')
        # self.window.columnconfigure(15, weight=1, uniform='fred')
        self.window.rowconfigure(0, weight=1)

        # self.line_numbers.columnconfigure(0, weight=1, uniform='fred')
        # self.editor.columnconfigure(1, weight=14, uniform='fred')
        # self.output.columnconfigure(15, weight=4, uniform='fred')

        self.line_numbers.grid(column=0, columnspan=1, row=0, sticky=tk.NSEW)
        self.editor.grid(column=1, columnspan=15, row=0, sticky=tk.NSEW)
        self.output.grid(column=16, columnspan=4, row=0, sticky=tk.NSEW)
        b1 = tk.Button(self.window, text='check1')
        b2 = tk.Button(self.window, text='check2')
        b1.grid(column=15, row=1, sticky=tk.NSEW)
        b2.grid(column=16, row=1, sticky=tk.NSEW)

        self.font_size.set(FONT_SIZE_MAP[FONT_SIZE_DEFAULT])
        self.changeFontSize()

        # self.updateOutputPane()
        # self.updateOutputPane()
        # self.updateOutputPane()

    def changeFontSize(self):
        self.editor.config(font=(FONT_FAMILY, self.font_size.get()))
        self.line_numbers.config(font=(FONT_FAMILY, self.font_size.get()))
        self.output.config(font=(FONT_FAMILY, self.font_size.get()))

    def buildMenuBar(self):
        self.menu_bar = tk.Menu(self.window)
        
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        sub_menu = tk.Menu(file_menu, tearoff=0)
        for key in FONT_SIZE_MAP.keys():
            sub_menu.add_radiobutton(label=key, command=self.changeFontSize, value=FONT_SIZE_MAP[key], var=self.font_size)
        file_menu.add_cascade(label='Font Size', menu=sub_menu)
        self.menu_bar.add_cascade(label='View', menu=file_menu)
        self.window.config(menu=self.menu_bar)

    def updateOutputPane(self, text='Lorem ipsum'):
        self.output.configure(state=tk.NORMAL)
        self.output.insert('end', text + '\n')
        self.output.configure(state=tk.DISABLED)
    
    def render(self):
        self.window.mainloop()
