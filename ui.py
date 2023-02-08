from tkinter import *
from tkinter.ttk import *

import os, re, json

colorpalette = ['#152f56','#1f3c67','#020f23','#ffffff']

clear = lambda:os.system('cls')

order = ''
rating = ''
ftype = ''
incldel = False
silent_mode = json.load(open('config.json'))['silent-mode']
debug_mode = json.load(open('config.json'))['debug-mode']
clear_terminal = json.load(open('config.json'))['clear-terminal']

ordermodes = ['no ordering','id','score','favcount','tagcount','comment_count','comment_bumped','mpixels','filesize','landscape','change','duration','random','score_asc','favcount_asc','tagcount_asc','comment_count_asc','comment_bumped_asc','mpixels_asc','filesize_asc','portrait','duration_asc']
ratingmodes = ['all','explicit','safe','questionable','-explicit','-safe','-questionable']
filetypes = ['all','jpg','png','gif','swf','webm']
minusratings = ['-explicit','-safe','-questionable']

if clear_terminal:
    clear()
    
def verifyinput(_order,_rating,_filetype,_amount,_tags):
    global order, rating, ftype
    if _order == 'no ordering' or _order not in ordermodes:
        order = None
    else:
        order = f'order:{_order}'
    if _rating == 'all' or _rating not in ratingmodes:
        rating = None
    elif _rating in minusratings:
        rating == f'-rating:{(minusratings.index(_rating))[1:]}'
    else:
        rating = f'rating:{_rating}'
    if _filetype == 'all' or _filetype not in filetypes:
        ftype = None
    else:
        ftype = f'filetype:{_filetype}'

    tags = _tags.split()
    x = '+'.join(tags)
    x = f'{order}+{rating}+{ftype}+{x}'
    x = re.split("[+]", x)
    while("" in x):
        x.remove("")
    while("None" in x):
        x.remove("None")
    tags = '+'.join(x)
    tags = tags.replace('\n','')

    if _amount == '':
        amount = 0
    else:
        amount = int(_amount)
    if amount >= 321:
        amount = 320
        if not silent_mode or debug_mode:
            print('The hard-limit of posts per session is 320.')

    if not silent_mode or debug_mode:
        print('Summary:')
        print(f'- tags: {tags}')
        print(f'- ordering by: {order}')
        print(f'- rating filter: {rating}')
        print(f'- filtering filetype by: {ftype}')
        print(f'- amount: {amount}')
    os.system(f'python get.py "{tags}" "{amount}"')
    root.destroy()

def testVal(inStr,acttyp):
    if acttyp == '1':
        if not inStr.isdigit():
            return False
    return True

root = Tk()
root.title('e621 bulk downloader selection UI')
root.configure(background=colorpalette[0])
root.attributes('-toolwindow', True)
style = Style()

style.configure('c.TCombobox',background=colorpalette[0])
style.configure('c.TButton',background=colorpalette[0])
style.configure('c.TEntry',background=colorpalette[0])

tagsin = Text(root, height = 10, width = 30, background = colorpalette[1], foreground = 'white')

limitint = Entry(root, validate = 'key', style = 'c.TEntry')
limitint['validatecommand'] = (limitint.register(testVal),'%P','%d')

ordermode = Combobox(root, style = 'c.TCombobox')
ordermode['values']=(ordermodes)
ordermode.current(0)

ratingmode = Combobox(root, style = 'c.TCombobox')
ratingmode['values'] = ratingmodes
ratingmode.current(0)

filetype = Combobox(root, style = 'c.TCombobox')
filetype['values'] = filetypes
filetype.current(0)


verifybtn = Button(root,text='Done',command=lambda:verifyinput(ordermode.get(),ratingmode.get(),filetype.get(),limitint.get(),tagsin.get(1.0,END)),style='c.TButton')
Label(root, text = 'Tags:', background = colorpalette[0], foreground = colorpalette[3]).grid(row = 0, column = 0, sticky = W)
tagsin.grid(row = 1, columnspan = 2, sticky = W+E)
Label(root, text = 'Limit: ', background = colorpalette[0], foreground = colorpalette[3]).grid(row = 2, column = 0, sticky = W)
limitint.grid(row = 2,column = 1,sticky = W+E)
Label(root,text='order:',background=colorpalette[0],foreground=colorpalette[3]).grid(row=4,column=0,sticky=W)
ordermode.grid(row=4,column=1,sticky=W+E)
Label(root,text='rating:',background=colorpalette[0],foreground=colorpalette[3]).grid(row=5,column=0,sticky=W)
ratingmode.grid(row=5,column=1,sticky=W+E)
Label(root,text='type:',background=colorpalette[0],foreground=colorpalette[3]).grid(row=6,column=0,sticky=W)
filetype.grid(row=6,column=1,sticky=W+E)
Button(text = 'Close', command = lambda : root.destroy(),style='c.TButton').grid(row=7,column=1,sticky=W)
verifybtn.grid(row=7,column=0,sticky=W+E)

root.mainloop()