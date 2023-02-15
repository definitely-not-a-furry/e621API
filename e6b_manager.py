"This is a basic app to create/read/write .e6b files"
import tkinter as tk
from e6b_main import Main

class App(tk.Tk):
    "Main window"
    def __init__(self):
        super().__init__()
        self.menubar=tk.Menu(self)

        self.text=tk.Text(self)
        self.text.grid()

        self.exportmenu=tk.Menu(self.menubar,tearoff=0)
        self.file=tk.Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label='File',menu=self.file)
        self.file.add_command(label='Open...',command=lambda:Main.getfile(Main,self.text))
        self.file.add_command(label='Save as...',
        command=lambda:Main.saveas(Main,self.text.get(1.0,tk.END)))
        self.file.add_separator()
        self.file.add_cascade(label='Export...',menu=self.exportmenu)
        self.exportmenu.add_command(label='Export .json to .e6b',
        command=lambda:Main.exportfromjson(Main))
        self.exportmenu.add_command(label='Export .e6b to download links')
        self.file.add_separator()
        self.file.add_command(label='Exit',command=lambda:Main.closerootconfirmation(Main,self))

        self.edit=tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Edit',menu=self.edit)
        self.edit.add_command(label='[None]',state=tk.DISABLED)
        self.config(menu=self.menubar)

root=App()
root.mainloop()
