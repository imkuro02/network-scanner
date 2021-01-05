from tkinter import *

root = Tk()
#root.geometry('400x400')


height = 5
width = 5

def showMsg():  
    print('button')
    Lb1.delete('0','end')

button = Button(root,
	text = 'Submit',
	command = showMsg)  
button.pack()  


scrollbar = Scrollbar(root)
Lb1 = Listbox(root,height = 5)
for i in range(100):
    Lb1.insert(8,str(i))

Lb1.config(yscrollcommand=scrollbar.set)

Lb1.pack()



mainloop()
