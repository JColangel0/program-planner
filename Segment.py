from tkinter import *


class Segment:
    def __init__(self, x, y, width, height, text, root, contents):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.contents = contents
        self.root = root

    def createSegment(self):
        label = Label(self.root, text=self.text)
        label.place(x=self.x, y=self.y)
        self.textbox = Text(self.root, width=self.width, height=self.height,
                            yscrollcommand=set(), spacing1=3, spacing2=3, spacing3=3)
        self.textbox.insert("1.0", self.contents)
        self.textbox.place(x=self.x, y=self.y+30)

    def getText(self):
        return self.textbox.get("1.0", END)
