import tkinter as tk

# Extend the tk Text to support some additional custom events 
# and simple text manipulation shortcuts (select all, cut, copy, paste)
class CustomTkText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)
        
        self.binding_functions_config()
        self.create_binding_keys()

    def _proxy(self, *args):
        cmd = (self._orig,) + args
        try:
            result = self.tk.call(cmd)
        except Exception:
            return None

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ("insert", "delete") or 
            args[0:3] == ("mark", "set", "insert")):
            self.event_generate("<<CursorChange>>", when="tail")

        if (args[0] in ("insert", "delete") or 
            args[0:3] == ("mark", "set", "insert") or
            args[0:2] == ("xview", "moveto") or
            args[0:2] == ("xview", "scroll") or
            args[0:2] == ("yview", "moveto") or
            args[0:2] == ("yview", "scroll")):
            self.event_generate("<<ViewScroll>>", when="tail")


        return result

    def binding_functions_config(self):
        self.tag_configure("sel", background="#44475a")
        return

    def copy(self, event=None):
        self.clipboard_clear()
        text = self.get("sel.first", "sel.last")
        self.clipboard_append(text)
        return "break"
    
    def cut(self, event):
        self.copy()
        self.delete("sel.first", "sel.last")
        return "break"

    def paste(self, event):
        text = self.selection_get(selection='CLIPBOARD')
        self.insert(tk.INSERT, text)
        return "break"

    def create_binding_keys(self):
        for key in ["<Control-c>","<Control-C>"]:
            self.bind(key, self.copy)
        
        for key in ["<Control-x>","<Control-X>"]:
            self.bind(key, self.cut)
        
        for key in ["<Control-v>","<Control-V>"]:
            self.bind(key, self.paste)

        for key in ["&lt;Control-a>","&lt;Control-A>"]:
            self.bind(key, self.select_all)
        
        for key in ["&lt;Button-1>","&lt;Return>"]:
            self.bind(key, self.deselect_all)
        return

    def select_all(self, event):
        self.tag_add("sel",'1.0','end')
        return "break"


    def deselect_all(self, event):
        self.tag_remove("sel",'1.0','end')
        return "break"