import asyncio
import threading
import os
import subprocess
import tkinter as tk
from tkinter.constants import NSEW
import tkinter.ttk as ttk
from tkinter import font


from Common.Utils import parse_theme_file, parse_language_file, get_icon, FONT_FAMILY, FONT_SIZE_MAP, FONT_SIZE_DEFAULT, FILE_NAME
from CustomTkText import CustomTkText
from Highlighter import Highlighter
from GifCanvas import GifCanvas
from LineNumbers import TextLineNumbers


class TextEditor:
    def __init__(self, language='kotlin', theme='dracula'):

        self.language = language
        self.theme = theme
        self.window = tk.Tk()
        self.font_size = tk.IntVar()
        self.window.title('{} Text Editor'.format(self.language[0].upper() + self.language[1:]))

        self.theme_file = parse_theme_file(theme=self.theme)
        self.language_file = parse_language_file(language=self.language)
        self.script_file_name = FILE_NAME + '.' + self.language_file['script_extension']
        self.editor = CustomTkText(
            self.window, 
            background=self.theme_file['background']['color'], 
            foreground=self.theme_file['foreground']['color'], 
            insertbackground=self.theme_file['foreground']['color'],
            width=40,
            tabs=('1c'),
            wrap=tk.NONE
        )
        
        self.current_editor_index = tk.StringVar()
        self.editor_lab = tk.Label(self.window, textvar=self.current_editor_index)
        self.editor.bind('<<CursorChange>>', self.updateEditorIndex)
        
        self.editor_vertical_scroll_bar = tk.Scrollbar(
            orient=tk.VERTICAL, 
            command=self.editor.yview,)
        self.editor_horizontal_scroll_bar = tk.Scrollbar(
            orient=tk.HORIZONTAL, 
            command=self.editor.xview)
        self.editor.configure(yscrollcommand=self.editor_vertical_scroll_bar.set)
        self.editor.configure(xscrollcommand=self.editor_horizontal_scroll_bar.set)
        self.line_numbers = TextLineNumbers(
            self.window
        )
        self.line_numbers.attach(self.editor)
        self.editor.bind("<<ViewScroll>>", self.onEditorViewScroll)
        h = Highlighter(self.editor, language=self.language, theme=self.theme)

        self.buildMenuBar()

        self.output = tk.Text(
            self.window,
            width=20
        )
        self.output_vertical_scroll_bar = tk.Scrollbar(orient="vertical", command=self.output.yview)
        self.output.configure(yscrollcommand=self.output_vertical_scroll_bar.set)
        self.output.tag_configure("error", foreground="red")
        self.output.tag_configure("error_location", foreground="blue", underline=True)
        self.output.tag_bind("error_location", "<Button-1>", self.onErrorLocationClicked)
        self.loading_spinner = get_icon('spinner', ext='gif')
        self.loading_canvas = GifCanvas(
            self.window,
            width=self.loading_spinner.width(),
            height=self.loading_spinner.height())

        play_image = get_icon('play')

        # Init `Execute` button
        self.execute_button = tk.Button(
            self.window,
            background=self.theme_file['background']['color'],
            foreground=self.theme_file['foreground']['color'],
            text=' Execute', 
            image=play_image, 
            compound=tk.LEFT, 
            pady=5,
            padx=10,
            command=self.onExecutePressed)

        # Init `Clear Output` button
        self.clear_output_button = tk.Button(
            self.window,
            background=self.theme_file['background']['color'],
            foreground=self.theme_file['foreground']['color'],
            text='Clear Output',
            pady=5,
            padx=10,
            command=self.clearOutputPane)

        # Layout Arrangement (in a grid)

        # Set weight for each column
        for i in range(30):
            if i not in [0,1,17,29]:
                self.window.columnconfigure(i, weight=1, uniform='son', minsize=0)

        self.window.rowconfigure(0, weight=1)

        # First row
        self.line_numbers.grid(column=0, columnspan=2, row=0, sticky=tk.NSEW)
        self.editor.grid(column=2, columnspan=15, row=0, sticky=tk.NSEW)
        self.editor_vertical_scroll_bar.grid(column=17, row=0, sticky=tk.NS + tk.W, padx=(0,10))
        self.output.grid(column=18, columnspan=11, row=0, sticky=tk.NSEW)
        self.output_vertical_scroll_bar.grid(column=29, row=0, sticky=tk.NS + tk.W)

        # Second row
        self.editor_horizontal_scroll_bar.grid(column=2, columnspan=15, row=1, sticky=tk.EW)


        # Third row
        self.editor_lab.grid(column=2, columnspan=15, row=2, sticky=tk.NSEW)

        self.execute_button.grid(column=18, columnspan=2, row=2, sticky=tk.NSEW)
        self.loading_canvas.grid(column=20, row=2, sticky=tk.NSEW)
        self.clear_output_button.grid(column=21, columnspan=2, row=2, sticky=tk.NSEW)
        self.execute_button.image = play_image

        # Init values for widgets in the layout
        self.font_size.set(FONT_SIZE_MAP[FONT_SIZE_DEFAULT])
        self.updateOutputPane()
        self.changeFontSize()
        self.editor.focus()
        self.updateEditorIndex()

    def onEditorViewScroll(self, event=None):
        self.line_numbers.redraw(font=(FONT_FAMILY, self.font_size.get()))

    def updateEditorIndex(self, event=None):
        cursor_position = self.editor.index(tk.INSERT)
        cursor_position_pieces = str(cursor_position).split('.')
        cursor_line = cursor_position_pieces[0]
        cursor_char = cursor_position_pieces[1]
        self.current_editor_index.set(f'line: {cursor_line}  col: {int(cursor_char) + 1}')

    def onErrorLocationClicked(self, event):

        # get the index of the mouse click
        index = event.widget.index("@%s,%s" % (event.x, event.y))

        # get the indices of all "adj" tags
        tag_indices = list(event.widget.tag_ranges('error_location'))

        # iterate them pairwise (start and end index)
        for start, end in zip(tag_indices[0::2], tag_indices[1::2]):
            # check if the tag matches the mouse click index
            if event.widget.compare(start, '<=', index) and event.widget.compare(index, '<', end):
                # return string between tag start and end
                tmp = self.output.get(start, end).split(':')[1:]
                tmp[1] = str(int(tmp[1]) - 1)
                
                self.editor.mark_set(tk.INSERT, f"{tmp[0]}.{tmp[1]}")
                self.editor.see(tk.INSERT)
                self.editor.focus()
                         
                return "break"

    # Execute script in a non-blocking manner
    def onExecutePressed(self):
        if not self.output.compare("end-1c", "==", "1.0"):
            self.updateOutputPane('\n-------\n', stderr=False)
        os.chdir(os.path.dirname(os.path.realpath(__file__)))

        file = open(self.script_file_name, 'w')
        file.write(self.editor.get('1.0', tk.END + '-1c'))
        file.close()

        self.loading_canvas.load(get_icon('spinner', ext='gif', path_only=True))
        self.execute_button.config(state=tk.DISABLED)

        self.popenAndCall(
            self.onFinishExecute, 
            self.language_file['execution_command'] + [self.script_file_name],
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            shell=True)


    def onFinishExecute(self, stdout, stderr):
        stdout_str = stdout.decode("utf-8")
        stderr_str = stderr.decode("utf-8")

        if len(stdout_str) != 0:
            self.updateOutputPane(stdout_str, stderr=False)   
        if len(stderr_str) != 0:
            self.updateOutputPane(stderr_str, stderr=True)
        
        self.loading_canvas.unload()
        self.execute_button.config(state=tk.NORMAL)

    def popenAndCall(self, on_exit, *popen_args, **popen_kwargs):
        
        def runInThread(on_exit, popen_args, popen_kwargs):
            process = subprocess.Popen(*popen_args, **popen_kwargs)
            stdout, stderr = process.communicate()
            on_exit(stdout, stderr)
            return
        thread = threading.Thread(target=runInThread, args=(on_exit, popen_args, popen_kwargs))
        thread.start()
        # returns immediately after the thread starts
        return thread
        


    def clearOutputPane(self):
        self.output.configure(state=tk.NORMAL)
        self.output.delete('1.0', tk.END)
        self.output.configure(state=tk.DISABLED)

    def changeFontSize(self):
        self.editor.config(font=(FONT_FAMILY, self.font_size.get()))
        # self.line_numbers.config(font=(FONT_FAMILY, self.font_size.get()))
        self.line_numbers.redraw(font=(FONT_FAMILY, self.font_size.get()))
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

    def updateOutputPane(self, text='', stderr=False):
        self.output.configure(state=tk.NORMAL)
        start = self.output.index(tk.END) + '-1c linestart'
        self.output.insert(tk.END, text)
        if stderr:
            length = tk.IntVar()

            # Styling the error
            end = self.output.index(tk.END) + '-1c'
            self.output.tag_add("error", start, end)

            # Styling the error locations
            keyword = self.language_file['error_terms']['match']
            idx = self.output.search(keyword, start,\
                stopindex=tk.END, count=length, regexp=1)
            while idx:
                end = f"{idx}+{length.get()}c"
                self.output.tag_add("error_location", idx, end)
                start = end
                idx = self.output.search(keyword, start, stopindex=tk.END, count=length, regexp=1)

        self.output.configure(state=tk.DISABLED)
    
    def render(self):
        self.window.mainloop()
