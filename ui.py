"The UI module for e621API"
import json
import os
import platform
from tkinter import END, E, Frame, Label, Text, Tk, W
from tkinter.ttk import Button, Combobox, Entry, Style

colorpalette=['#152f56','#1f3c67','#020f23','#ffffff']
#this is going to be used for themes in the future

class QLabel(Label):
    "Quick label creation for improved code readability"
    def __init__(self,_contents,_gridx,_gridy,frame):
        super().__init__(frame)
        super().configure(text=_contents,foreground=colorpalette[3],background=colorpalette[0])
        super().grid(column=_gridx,row=_gridy,sticky=W)

def q_grid(_object,gridx,gridy):
    "Quick grid assignment"
    _object.grid(column=gridx,row=gridy,sticky=W+E)

def clear():
    "Clears terminal"
    if platform.platform()=='Windows':
        os.system('cls')
    else:
        os.system('clear')

with open('config.json') as f: #pylint:disable=unspecified-encoding
    f=json.load(f)
    silent_mode=f['silent-mode']
    debug_mode=f['debug-mode']
    clear_terminal=f['clear-terminal']
    toolwindow=f['toolwindow']

ordermodes=['no ordering','id','score','favcount','tagcount','comment_count','comment_bumped',
            'mpixels','filesize','landscape','change','duration','random','score_asc',
            'favcount_asc','tagcount_asc','comment_count_asc','comment_bumped_asc','mpixels_asc',
            'filesize_asc','portrait','duration_asc']
ratingmodes=['all','explicit','safe','questionable','-explicit','-safe','-questionable']
filetypes=['all','jpg','png','gif','swf','webm']
minusratings=['-explicit','-safe','-questionable']

if clear_terminal:
    clear()

def verifyinput(order,rating,filetype,amount,tags,app):
    "Build the string to prepare for request"
    if order=='no ordering' or order not in ordermodes:
        order=None
    else:
        order=f'order:{order}'
    if rating=='all' or rating not in ratingmodes:
        rating=None
    elif rating in minusratings:
        rating=f'-rating:{(minusratings.index(rating))[1:]}'
    else:
        rating=f'rating:{rating}'
    if filetype=='all' or filetype not in filetypes:
        ftype=None
    else:
        ftype=f'filetype:{filetype}'
    #everything above is to make sure for example "score" is converted to "order:score"

    tags=tags.split()
    tags='+'.join(tags)
    tags=f'{order}+{rating}+{ftype}+{tags}'
    tags=tags.split("+")

    #I did this even though it is not necessary; e621 ignores double '+' and 'None':
    while "" in tags:
        tags.remove("")
    while "None" in tags:
        tags.remove("None")
    tags='+'.join(tags)
    tags=tags.replace('\n','')

    if amount is None:
        amount=0
    else:
        amount=int(amount)
    if amount>=321:
        amount=320 #probably not necessary but just in case
        if not silent_mode or debug_mode:
            print('The hard-limit of posts per session is 320.')

    if debug_mode:
        print('Summary:')
        print(f'- tags: {tags}')
        print(f'- ordering by: {order}')
        print(f'- rating filter: {rating}')
        print(f'- filtering filetype by: {ftype}')
        print(f'- amount: {amount}')
    with open('tmp\\request','w',encoding='UTF-8') as f: #pylint:disable=invalid-name,redefined-outer-name
        f.write(f'{tags}\n{amount}')
    os.system('python get.py')
    app.destroy()

def test_val(in_str,acttyp):
    "limits input to only numbers"
    if acttyp=='1':
        if not in_str.isdigit():
            return False
    return True

class Application(Tk):
    "Main application"
    def __init__(self):
        super().__init__()
        self.title('e621 bulk downloader selection UI')
        self.configure(background=colorpalette[0])
        self.attributes('-toolwindow',toolwindow)
        self.resizable(False,False)

        self.style=Style()
        self.style.configure('c.TCombobox',background=colorpalette[0])
        self.style.configure('c.TButton',background=colorpalette[0])
        self.style.configure('c.TEntry',background=colorpalette[0])

        self.frame=Frame(self)
        self.frame.configure(padx=10,pady=10,background=colorpalette[0])
        self.tagsin=Text(self.frame,height=10,width=30,background=colorpalette[1],
        foreground='white')

        self.limitint=Entry(self.frame,validate='key',style='c.TEntry')
        self.limitint['validatecommand']=(self.limitint.register(test_val),'%P','%d')

        self.ordermode=Combobox(self.frame,style='c.TCombobox',values=ordermodes)
        self.ordermode.current(2)

        self.ratingmode=Combobox(self.frame,style='c.TCombobox',values=ratingmodes)
        self.ratingmode.current(2)

        self.filemode=Combobox(self.frame,style='c.TCombobox',values=filetypes)
        self.filemode.current(0)

        self.verifybtn=Button(self.frame,text='Done',command=lambda:verifyinput(self.ordermode.get()
        ,self.ratingmode.get(),self.filemode.get(),int(self.limitint.get()),self.tagsin.get(1.0,END)
        ,self),style='c.TButton')

        QLabel('Tags:',0,0,self.frame)
        q_grid(self.tagsin,0,1)
        QLabel('Limit:',0,2,self.frame)
        q_grid(self.limitint,1,2)
        QLabel('Order:',0,4,self.frame)
        q_grid(self.ordermode,1,4)
        QLabel('Rating:',0,5,self.frame)
        q_grid(self.ratingmode,1,5)
        QLabel('Type:',0,6,self.frame)
        q_grid(self.filemode,1,6)
        q_grid(self.verifybtn,0,7)
        self.verifybtn.grid(columnspan=2)
        self.tagsin.grid(columnspan=2)
        self.frame.grid(column=0,row=0)

root=Application()
root.mainloop()
