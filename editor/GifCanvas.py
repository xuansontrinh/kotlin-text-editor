import tkinter as tk
from PIL import Image, ImageTk
from itertools import count


class GifCanvas(tk.Canvas):
    """a label that displays images, and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.delete("all")
        self.frames = None

    def next_frame(self):
        self.update()
        canvas_width, canvas_height = self.winfo_width(), self.winfo_height()
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.create_image(canvas_width/2, canvas_height/2, image=self.frames[self.loc])
            # self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)