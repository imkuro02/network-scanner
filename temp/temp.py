import tkinter as Tk
from tkinter import font as tkFont

#Create a listbox
master = Tk.Tk()
listbox = Tk.Listbox(master, width=40, height=20)
listbox.pack()

# Dummy strings to align
stringsLeft = ["short", "medium", "extra-------long", "short", "medium", "short"]
stringsRight = ["one", "two", "three", "four", "five", "six"]

listbox.configure(exportselection=False)


# Get the listbox font
listFont = tkFont.Font(font=listbox.cget("font"))

# Define spacing between left and right strings in terms of single "space" length
spaceLength = listFont.measure(" ")
spacing = 12 * spaceLength

# find longest string in the left strings
leftLengths = [listFont.measure(s) for s in stringsLeft]
longestLength = max(leftLengths)

# combine left and righ strings with the right number of spaces in between
for i in range(len(stringsLeft)):
    neededSpacing = longestLength + spacing - leftLengths[i]
    spacesToAdd = int(round(neededSpacing/spaceLength))
    listbox.insert(Tk.END, stringsLeft[i] + spacesToAdd * " " + stringsRight[i])

Tk.mainloop()
