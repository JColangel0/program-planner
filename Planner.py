from tkinter import *
import PlanData as pd
import Segment as seg

root = Tk()
root.resizable(False, False)

state = "select"


def saveFile(name, description, todo, done, dependencies, ui, specs, logic):
    dataSet = pd.PlanData(name, description, todo, done, dependencies, ui, specs, logic)
    dataSet.writeData()
    root.quit()


def createPage(widget, contents):
    global state
    state = "project"
    widget.pack_forget()
    root.geometry("1400x800")

    name = seg.Segment(20, -10, 30, 1, "", root, contents[0])
    name.createSegment()

    description = seg.Segment(20, 60, 66, 4, "Project Description", root, contents[1])
    description.createSegment()

    toDoList = seg.Segment(20, 190, 30, 15, "To-Do List", root, contents[2])
    toDoList.createSegment()

    doneTasks = seg.Segment(270, 190, 30, 15, "Completed Tasks", root, contents[3])
    doneTasks.createSegment()

    dependencies = seg.Segment(20, 530, 66, 10, "Dependencies", root, contents[4])
    dependencies.createSegment()

    UISeg = seg.Segment(550, 20, 50, 10, "UI (If Applicable)", root, contents[5])
    UISeg.createSegment()

    specs = seg.Segment(550, 266, 50, 24, "Project Specs", root, contents[6])
    specs.createSegment()

    logic = seg.Segment(970, 20, 50, 37, "Logic", root, contents[7])
    logic.createSegment()

    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(
        label="Save and Exit",
        command=lambda: saveFile(
            name.getText(),
            description.getText(),
            toDoList.getText(),
            doneTasks.getText(),
            dependencies.getText(),
            UISeg.getText(),
            specs.getText(),
            logic.getText(),
        ),
    )
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)


def fetchData(widget, name):
    contents = []
    f = open("Plans.txt")
    data = f.read()
    sI = data.find(name)
    if sI == -1:
        return
    eI = data[sI:].find("~>")
    data = data[sI : eI + sI + 1]
    value = ""
    for x in data:
        if x != "~":
            value += x
        else:
            contents.append(value[:-1])
            value = ""
    f.close()
    createPage(widget, contents)


def loadProjectPage(widget):
    global state
    state = "load"
    widget.pack_forget()
    frame = Frame(root, padx=20, pady=20)
    frame.pack()
    label = Label(frame, text="Enter Project Name: ")
    label.pack()
    projectNameVar = StringVar()
    projectName = Entry(frame, textvariable=projectNameVar)
    projectName.pack()
    loadProjectButton = Button(
        frame, text="Load", command=lambda: fetchData(frame, projectNameVar.get())
    )
    loadProjectButton.pack()

    def handler(e):
        if state == "load":
            fetchData(frame, projectNameVar.get())

    root.bind("<Return>", handler)


def loadScreen():
    root.title("Planner")
    frame = Frame(root, padx=5, pady=10)
    frame.pack()
    newProject = Button(
        frame,
        text="New Project",
        height=2,
        command=lambda: createPage(frame, ["Project Name", "", "", "", "", "", "", ""]),
    )
    newProject.pack(side=LEFT)
    loadProject = Button(
        frame, text="Load Project", height=2, command=lambda: loadProjectPage(frame)
    )
    loadProject.pack(side=RIGHT)


if __name__ == "__main__":
    loadScreen()
    root.mainloop()
