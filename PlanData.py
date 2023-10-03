class PlanData:
    def __init__(self, name, description, todo, done, dependencies, ui, specs, logic):
        self.name = name
        self.desc = description
        self.todo = todo
        self.done = done
        self.depend = dependencies
        self.ui = ui
        self.specs = specs
        self.logic = logic

    def writeData(self):
        f = open(
            "Plans.txt",
            "r",
        )
        data = f.read()
        startIndex = data.find(self.name + "~")
        if startIndex != -1:
            endIndex = data[startIndex:].find("~>")
            data = (
                data[:startIndex]
                + (
                    self.name
                    + "~"
                    + self.desc
                    + "~"
                    + self.todo
                    + "~"
                    + self.done
                    + "~"
                    + self.depend
                    + "~"
                    + self.ui
                    + "~"
                    + self.specs
                    + "~"
                    + self.logic
                    + "~>"
                )
                + data[endIndex:]
            )
        else:
            data += (
                self.name
                + "~"
                + self.desc
                + "~"
                + self.todo
                + "~"
                + self.done
                + "~"
                + self.depend
                + "~"
                + self.ui
                + "~"
                + self.specs
                + "~"
                + self.logic
                + "~>"
            )
        f.close()

        f = open("Plans.txt", "w")
        f.write(data)
        f.close()
