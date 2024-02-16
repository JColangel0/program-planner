class PlanData:
    def __init__(self, segments):
        self.name = segments[0].getText()
        self.desc = segments[1].getText()
        self.todo = segments[2].getText()
        self.done = segments[3].getText()
        self.depend = segments[4].getText()
        self.ui = segments[5].getText()
        self.specs = segments[6].getText()
        self.logic = segments[7].getText()

    def writeData(self):
        f = open(
            "/Users/josephcolangelo/PersonalFiles/Plans.txt",
            "r",
        )
        data = f.read()
        startIndex = data.find("<" + self.name)
        if startIndex != -1:
            endIndex = data[startIndex:].find(">") + 1
            data = (
                data[:startIndex]
                + (
                    "<"
                    + self.name
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
                    + ">"
                )
                + data[startIndex + endIndex :]
            )
        else:
            data += (
                "<"
                + self.name
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
                + ">"
            )
        f.close()

        f = open("/Users/josephcolangelo/PersonalFiles/Plans.txt", "w")
        f.write(data)
        f.close()
