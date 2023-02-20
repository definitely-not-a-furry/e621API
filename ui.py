"The UI module for e621API"
import os
import re
import json

from tkinter import Label, Tk, Text, END, W, E
from tkinter.ttk import Combobox, Style, Button, Entry

colorpalette=['#152f56','#1f3c67','#020f23','#ffffff']
# this is going to be used for themes in the future

class QLabel(Label):
    "Quick label creation for improved code readability"
    def __init__(self,_contents,_gridx,_gridy):
        super().__init__()
        super().configure(text=_contents,foreground=colorpalette[3],background=colorpalette[0])
        super().grid(column=_gridx,row=_gridy,sticky=W)

def q_grid(_object,gridx,gridy):
    "Quick grid assignment"
    _object.grid(column=gridx,row=gridy,sticky=W+E)

def clear():
    "Clears terminal"
    os.system('cls')

with open('config.json') as f:
    f=json.load(f)
    silent_mode=f['silent-mode']
    debug_mode=f['debug-mode']
    clear_terminal=f['clear-terminal']

ordermodes=['no ordering','id','score','favcount','tagcount','comment_count','comment_bumped',
            'mpixels','filesize','landscape','change','duration','random','score_asc',
            'favcount_asc','tagcount_asc','comment_count_asc','comment_bumped_asc','mpixels_asc',
            'filesize_asc','portrait','duration_asc']
ratingmodes=['all','explicit','safe','questionable','-explicit','-safe','-questionable']
filetypes=['all','jpg','png','gif','swf','webm']
minusratings=['-explicit','-safe','-questionable']

if clear_terminal:
    clear()

def verifyinput(order,rating,filetype,amount,tags):
    "Build the string to prepare for request"
    if order == 'no ordering' or order not in ordermodes:
        order=None
    else:
        order=f'order:{order}'
    if rating == 'all' or rating not in ratingmodes:
        rating=None
    elif rating in minusratings:
        rating=f'-rating:{(minusratings.index(rating))[1:]}'
    else:
        rating=f'rating:{rating}'
    if filetype == 'all' or filetype not in filetypes:
        ftype=None
    else:
        ftype=f'filetype:{filetype}'

    tags=tags.split()
    tags='+'.join(tags)
    tags=f'{order}+{rating}+{ftype}+{tags}'
    tags=re.split("[+]",tags)

    # I did this even though it is not necessary; e621 ignores double '+' and 'None':
    while "" in tags:
        tags.remove("")
    while "None" in tags:
        tags.remove("None")
    tags='+'.join(tags)
    tags=tags.replace('\n','')

    if amount == None:
        amount=0
    else:
        amount=int(amount)
    if amount >= 321:
        amount=320 # probably not necessary but just in case
        if not silent_mode or debug_mode:
            print('The hard-limit of posts per session is 320.')

    if debug_mode:
        print('Summary:')
        print(f'- tags: {tags}')
        print(f'- ordering by: {order}')
        print(f'- rating filter: {rating}')
        print(f'- filtering filetype by: {ftype}')
        print(f'- amount: {amount}')
    os.system(f'python get.py "{tags}" "{amount}"')
    root.destroy()

def test_val(in_str,acttyp):
    "limits input to only numbers"
    if acttyp == '1':
        if not in_str.isdigit():
            return False
    return True

root=Tk()
root.title('e621 bulk downloader selection UI')
root.configure(background=colorpalette[0])
root.attributes('-toolwindow',True)

style=Style()
style.configure('c.TCombobox',background=colorpalette[0])
style.configure('c.TButton',background=colorpalette[0])
style.configure('c.TEntry',background=colorpalette[0])

tagsin=Text(root,height=10,width=30,background=colorpalette[1],foreground='white')

limitint=Entry(root,validate='key',style='c.TEntry')
limitint['validatecommand']=(limitint.register(test_val),'%P','%d')

ordermode=Combobox(root,style='c.TCombobox',values=ordermodes)
ordermode.current(2)

ratingmode=Combobox(root,style='c.TCombobox',values=ratingmodes)
ratingmode.current(2)

filetype=Combobox(root,style='c.TCombobox',values=filetypes)
filetype.current(0)

verifybtn=Button(root,text='Done',command=lambda:verifyinput(ordermode.get(),ratingmode.get(),
filetype.get(),int(limitint.get()),tagsin.get(1.0,END)),style='c.TButton')

QLabel('Tags: ',0,0)
q_grid(tagsin,0,1)
QLabel('Limit: ',0,2)
q_grid(limitint,1,2)
QLabel('Order: ',0,4)
q_grid(ordermode,1,4)
QLabel('Rating: ',0,5)
q_grid(ratingmode,1,5)
QLabel('Type: ',0,6)
q_grid(filetype,1,6)
q_grid(verifybtn,0,7)
verifybtn.grid(columnspan=2)
tagsin.grid(columnspan=2)
root.mainloop()
