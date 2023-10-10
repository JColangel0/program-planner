from tkinter import *
import PlanData as pd
import Segment as seg
import StateMachine as sm

root = Tk()
root.resizable(False, False)

state = sm.StateMachine()

def saveFile(segments, close):
    dataSet = pd.PlanData(segments)
    dataSet.writeData()
    if close:
        root.quit()

def saveAndLoad(segments, widget):
    saveFile(segments, False)
    widget.destroy()
    root.geometry("200x120")
    loadProjectPage(widget)
    
def saveAndReturn(segments, widget):
    saveFile(segments, False)
    widget.destroy()
    createStartScreen()

def clearAndReturn(widget):
    widget.pack_forget()
    createStartScreen()

def createPage(widget, contents):
    state.setState(1)
    widget.pack_forget()
    root.geometry("1400x800")
    
    frame = Frame(root, width=1400, height=800)
    frame.place(x=0,y=0)

    name = seg.Segment(20, -10, 30, 1, "", frame, contents[0])
    name.createSegment()

    description = seg.Segment(20, 60, 66, 4, "Project Description", frame, contents[1])
    description.createSegment()

    toDoList = seg.Segment(20, 190, 30, 15, "To-Do List", frame, contents[2])
    toDoList.createSegment()

    doneTasks = seg.Segment(270, 190, 30, 15, "Completed Tasks", frame, contents[3])
    doneTasks.createSegment()

    dependencies = seg.Segment(20, 530, 66, 10, "Dependencies", frame, contents[4])
    dependencies.createSegment()

    UISeg = seg.Segment(550, 20, 50, 10, "UI (If Applicable)", frame, contents[5])
    UISeg.createSegment()

    specs = seg.Segment(550, 266, 50, 24, "Project Specs", frame, contents[6])
    specs.createSegment()

    logic = seg.Segment(970, 20, 50, 37, "Logic", frame, contents[7])
    logic.createSegment()

    segments = [name, description, toDoList, doneTasks, dependencies, UISeg, specs, logic]

    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(
        label = "Save",
        command = lambda: saveFile(segments, False)
    )
    filemenu.add_command(
        label="Save And Close",
        command = lambda: saveFile(segments, True)
    )
    filemenu.add_command(
        label = "Load Project",
        command = lambda: saveAndLoad(segments, frame)

    )
    filemenu.add_command(
        label = "Back",
        command = lambda: saveAndReturn(segments, frame)
    )
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)

    def save(e):
        saveFile(segments, False)

    root.bind("<Command-s>", save)


def fetchData(widget, name):
    contents = []
    with open("Plans.txt", "r") as f:
        data = f.read()
        sI = data.find(name)
        if sI == -1:
            return
        eI = data[sI:].find(">")
        data = data[sI : eI + sI + 1]
        value = ""
        for x in data:
            if x != "~" and x != ">":
                value += x
            else:
                contents.append(value[:-1])
                value = ""
    createPage(widget, contents)

def removeChunk(name, widget):
    data = ""
    with open("Plans.txt", "r") as f:
        data = f.read()
        startIndex = data.find("<"+name)
        if startIndex == -1:
            return
        endIndex = data[startIndex:].find(">") + 1
        data = data[:startIndex] + data[startIndex+endIndex:]
    with open("Plans.txt", "w") as f:
        f.write(data)
    clearAndReturn(widget)

def findRecentProjects():
    MAX_PROJECTS = 5
    names = []
    with open("Plans.txt", "r") as f:
        data = f.read()
        index = indexE = numProjects = 0
        while numProjects <= MAX_PROJECTS:
            index = data.find("<")
            indexE = data[index:].find("~")
            if index < 0 or indexE < 0:
                break
            index += 1
            names.append(data[index:index+indexE-2])
            data = data[index+indexE:]
            numProjects += 1
    return names


def loadProjectPage(widget):
    state.setState(2)
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

    backButton = Button(frame, text="Back", command = lambda: clearAndReturn(frame))
    backButton.pack()

    def handler(e):
        if state.getStateIndex() == 2:
            fetchData(frame, projectNameVar.get())

    root.bind("<Return>", handler)

def deletePage(widget):
    state.setState(3)
    widget.pack_forget()

    frame = Frame(root, padx=20, pady=20)
    frame.pack()
    label = Label(frame, text="Enter Project Name: ")
    label.pack()

    projectNameVar = StringVar()
    projectName = Entry(frame, textvariable=projectNameVar)
    projectName.pack()

    loadProjectButton = Button(
        frame, text="Delete", command=lambda: removeChunk(projectNameVar.get(), frame))
    loadProjectButton.pack()

    backButton = Button(frame, text = "Back", command=lambda:clearAndReturn(frame))
    backButton.pack()

    def handler(e):
        if state.getStateIndex() == 3:
            removeChunk(projectNameVar.get(), frame)

    root.bind("<Return>", handler)


def createStartScreen():
    state.setState(0)
    root.title("Planner")
    frame = Frame(root, padx=5, pady=10)
    frame.pack()
    buttonFrame = Frame(frame)
    buttonFrame.pack()
    newProject = Button(
        buttonFrame,
        text="New Project",
        height=2,
        command=lambda: createPage(frame, ["Project Name", "", "", "", "", "", "", ""]),
    )
    newProject.pack(side=LEFT)
    deleteProject = Button(
        buttonFrame,
        text = "Delete Project",
        height = 2,
        command = lambda: deletePage(frame)
    )
    deleteProject.pack(side=RIGHT)
    loadProject = Button(
        buttonFrame, 
        text="Load Project", 
        height=2, 
        command=lambda: loadProjectPage(frame)
    )
    loadProject.pack()
    recentsFrame = Frame(frame, padx=5)
    recentsFrame.pack()
    recents = Label(recentsFrame, text="Recent Projects:", pady=3)
    recents.pack()
    names = findRecentProjects()
    for x in names:
        label = Label(recentsFrame, text=x)
        label.pack()

if __name__ == "__main__":
    createStartScreen()
    root.mainloop()
