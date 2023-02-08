from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import askyesno
import os, json

f = None
filename = None

def encodehex(_in):
    _out = hex(int.from_bytes(_in.encode(), 'big'))[2:]
    return(_out)

def decodehex(_in):
    _out = bytes.fromhex(_in).decode()
    return(_out)

def update(_text):
    _text.delete(1,END)

def getfile(_text):
    global f, filename
    filename = askopenfilename(filetypes=[('e621 bulk files','*.e6b')])
    f = open(filename, 'r+')
    _text.delete(1.0,END)
    _text.insert(END,decodehex(f.read()))

def filewrite(_contents,_file):
    _file.write(encodehex(_contents)+'\n')

def fileread(_file):
    d = _file.read().split('\n')
    return(decodehex(d))

def save(_text):
    global f
    if f == None:
        return
    f.close()
    f = open(filename,'w')
    f.write(encodehex(_text.get(1.0,END)))
    
def saveas(_text):
    f=open(asksaveasfilename(filetypes=(('e621 bulk file','*.e6b'),('All Files','*.*')),confirmoverwrite=True),'w')
    f.write(encodehex(_text))
    f.close()

def exportfromjson():
    posts = json.load(open('tmp\\posts.json'))
    links = list()
    linkstr = str()

    for i in posts['posts']:
        links.append(i['file']['url'])
    
    linkstr = '\n'.join(links)
    saveas(linkstr)
    

def closerootconfirmation(_root):
    if askyesno('Warning','Are you sure you want to quit? Any unsaved changes will be lost.'):
        _root.destroy()
    return


root = Tk()

menubar = Menu(root)

text = Text(root)
text.grid()

exportmenu = Menu(menubar, tearoff=0)
file = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=file)
file.add_command(label = 'Open...', command = lambda:getfile(text))
file.add_command(label = 'Save as...', command= lambda:saveas(text.get(1.0,END)))
file.add_command(label = 'Save', command = lambda:save(text))
file.add_separator()
file.add_cascade(label='Export...', menu=exportmenu)
exportmenu.add_command(label = 'Export .json to .e6b', command = lambda:exportfromjson())
exportmenu.add_command(label = 'Export .e6b to download links')
file.add_separator()
file.add_command(label ='Exit', command = lambda:closerootconfirmation(root))

edit = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Edit', menu=edit)
edit.add_command(label='[None]', state=DISABLED)


root.config(menu=menubar)
root.mainloop()
try:
    f.close()
except:
    None