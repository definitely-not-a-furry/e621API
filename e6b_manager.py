"This is a basic app to create/read/write .e6b files"
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import askyesno
import json

class Main():
    "Main functions"
    file=None
    filename=None

    def __init__(self):
        pass

    def encodehex(self,_in):
        "Encodes to hexadecimal strings"
        _out=hex(int.from_bytes(_in.encode(), 'big'))[2:]
        return _out

    def decodehex(self,_in):
        "Decodes hexadecimal strings"
        _out=bytes.fromhex(_in).decode()
        return _out

    def getfile(self,_text):
        "Prompts user to select an existing .e6b file"
        self.filename=askopenfilename(filetypes=[('e621 bulk files','*.e6b')])
        self.file=open(self.filename, 'r+',encoding='UTF-8')
        _text.delete(1.0,tk.END)
        _text.insert(tk.END,self.decodehex(self.file.read()))

    def filewrite(self,_contents,_file):
        "Writes to .e6b files"
        _file.write(self.encodehex(_contents)+'\n')

    def fileread(self,_file):
        "Reads .e6b files"
        temp=_file.read().split('\n')
        return self.decodehex(temp)

    def save(self,_text):
        "Saves file"
        if self.file is None:
            return
        self.file.close()
        self.file=open(self.filename,'w',encoding='UTF-8')
        self.file.write(self.encodehex(_text.get(1.0,tk.END)))

    def saveas(self,_text):
        "prompts user to save file with a name"
        self.file=open(asksaveasfilename(filetypes=(('e621 bulk file','*.e6b'),('All Files','*.*')),
        confirmoverwrite=True),'w',encoding='UTF-8')
        self.file.write(self.encodehex(_text))
        self.file.close()

    def exportfromjson(self):
        "Exports and filters links from a posts.json file"
        posts=json.load(open('tmp\\posts.json',encoding='UTF-8'))
        links=[]
        linkstr=str()

        for i in posts['posts']:
            links.append(i['file']['url'])

        linkstr='\n'.join(links)
        self.saveas(linkstr)

    def closerootconfirmation(self,_root):
        "Prompts user to make sure they saved their changes"
        if askyesno('Warning','Are you sure you want to quit? Any unsaved changes will be lost.'):
            _root.destroy()

class App(tk.Tk):
    "Main window"
    def __init__(self):
        super().__init__()
        self.menubar=tk.Menu(root)

        self.text=tk.Text(root)
        self.text.grid()

        self.exportmenu=tk.Menu(self.menubar,tearoff=0)
        self.file=tk.Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label='File',menu=self.file)
        self.file.add_command(label='Open...',command=lambda:Main.getfile(Main,self.text))
        self.file.add_command(label='Save as...',
        command=lambda:Main.saveas(Main,self.text.get(1.0,tk.END)))
        self.file.add_command(label='Save',command=lambda:Main.save(Main,self.text))
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

root=App()
root.config(menu=App.menubar)
root.mainloop()

try:
    Main.file.close()
finally:
    print('NoFile')
