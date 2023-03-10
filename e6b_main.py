"Module for e6b_manager.py"
import json
from tkinter import END
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import askyesno

import download


class Main():
    "Main functions"
    filename=None

    def __init__(self):
        pass

    def encodehex(self,_in):
        "Encodes input to hexadecimal"
        return format(int.from_bytes(_in.encode()),'x')

    def decodehex(self,_in):
        "Decodes hexadecimal input"
        return bytes.fromhex(_in).decode()

    def getfile(self,_text):
        "Prompts user to select an existing .e6b file"
        self.filename=askopenfilename(filetypes=[('e621 bulk files','*.e6b')])
        with open(self.filename,'r+',encoding='UTF-8') as file:
            _text.delete(1.0,END)
            _text.insert(END,self.decodehex(file.read()))

    def fileread(self,_file):
        "Reads .e6b files"
        return self.decodehex(_file.read().split('\n'))

    def saveas(self,_text):
        "Prompts user to save file with a name"
        self.filename=asksaveasfilename(filetypes=(('e621 bulk file','*.e6b'),
        ('All Files','*.*')),confirmoverwrite=True)

        with open(self.filename,'r+',encoding='UTF-8') as file:
            file.write(self.encodehex(_text))

    def exportfromjson(self):
        "Exports and filters links from a posts.json file"
        with open('tmp\\posts.json',encoding='UTF-8') as file:
            posts=json.load(file)
        links=[]

        for i in posts['posts']:
            links.append(i['file']['url'])

        self.saveas('\n'.join(links))

    def exportanddownload(self,_text):
        "Exports input links to the file 'tmp\\links'"
        with open('tmp\\links','w',encoding='UTF-8') as file:
            file.write(_text)
        download.Download()

    def closerootconfirmation(self,_root):
        "Prompts user to make sure they saved their changes"
        if askyesno('Warning','Are you sure you want to quit? Any unsaved changes will be lost.'):
            _root.destroy()
