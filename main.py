from tkinter import *
from tkinter.font import Font

import string
from functools import partial

class Application(Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.grid()

        # fonts
        self.font_30 = Font(family = "Arial Rounded MT Bold", size = 30)

        # globs
        self.modes_set = ["bin", "oct", "int", "hex"]
        self.modes_set_sys = [2, 8, 10, 16]

        # vars
        self.traceback = StringVar()

        self.ui()

        # post
        self.change_mode("hex", 0)
        self.change_mode("int", 1)

    def ui(self):
        self.format_label = Button(text = "hex\nint", font = self.font_30, bg = "#362534", fg = "white", height = 1, command = self.swap)

        self.input_field = Entry(textvariable = self.traceback, font = self.font_30, bg = "#303030", fg = "white")
        self.output_field = Entry(font = self.font_30, bg = "#303030", fg = "white")

        self.modes_togglers = [Button(text = mode, command = partial(self.change_mode, mode, 0), font = self.font_30, width = 3, bg = "#7b79ed")
                               for mode in self.modes_set] + [Button(text = mode, command = partial(self.change_mode, mode, 1), 
                               font = self.font_30, width = 3, bg = "#a579ed") for mode in self.modes_set]

        self.buttons = [Button(text = char, command = partial(self.insert_char, char), font = self.font_30, bg = "#ad7c4b", width = 3, 
                        disabledforeground = "#303040") for char in string.hexdigits[0 : 10]] + [Button(text = char, 
                        command = partial(self.insert_char, char), font = self.font_30, bg = "#ad8b4b", width = 3, 
                        disabledforeground = "#303040") for char in string.hexdigits[16 : 22]]

        self.backspace_button = Button(text = "BS", command = self.backspace, font = self.font_30, bg = "#ad524b", width = 2)
        self.clear_button = Button(text = "C", command = self.clear, font = self.font_30, bg = "#ad524b")

        # place
        self.format_label.grid(row = 0, column = 0, rowspan = 2, columnspan = 2, stick = NSEW)
        self.input_field.grid(row = 0, column = 2, columnspan = 5, stick = NSEW)
        self.output_field.grid(row = 1, column = 2, columnspan = 5, stick = NSEW)

        [toggler.grid(row = divmod(self.modes_togglers.index(toggler), 4)[1] + 2, column = divmod(self.modes_togglers.index(toggler), 4)[0],
         stick = NSEW) for toggler in self.modes_togglers]

        [button.grid(row = divmod(self.buttons.index(button) - 1, 3)[0] + 2, column = divmod(self.buttons.index(button) - 1, 3)[1] + 2,
         stick = NSEW) for button in self.buttons[1:10]]
        [button.grid(row = divmod(self.buttons.index(button) - 10, 2)[0] + 2, column = divmod(self.buttons.index(button), 2)[1] + 5,
         stick = NSEW) for button in self.buttons[10:16]]
        self.buttons[0].grid(row = 5, column = 2, columnspan = 3, stick = NSEW)

        self.backspace_button.grid(row = 5, column = 5, stick = NSEW)
        self.clear_button.grid(row = 5, column = 6, stick = NSEW)

        # post
        self.traceback.trace("w", self.run)

    def write_to_field(self, field, value = None):
        if field == 0:
            self.input_field.delete(0, END)
            self.input_field.insert(0, value)

        elif field == 1:
            self.output_field.delete(0, END)
            self.output_field.insert(0, value)

        else:
            self.write_to_field(0, self.output_field.get())
            self.run()
        
    def insert_char(self, char):
        self.write_to_field(0, self.input_field.get() + char)

    def backspace(self):
        self.write_to_field(0, self.input_field.get()[0 : -1])

    def clear(self):
        self.write_to_field(0, "")
        self.write_to_field(1, "")

    def run(self, *args):
        from_mode, to_mode = self.format_label["text"].split("\n")

        if self.input_field.get() == "":
            self.write_to_field(1, "")
            return None

        try:
            integer = int(self.input_field.get(), self.modes_set_sys[self.modes_set.index(from_mode)])

            if to_mode == "bin":
                self.write_to_field(1, bin(integer)[2:])
            elif to_mode == "oct":
                self.write_to_field(1, oct(integer)[2:])
            elif to_mode == "int":
                self.write_to_field(1, str(integer))
            else:
                self.write_to_field(1, "".join([char if char in string.hexdigits[0 : 10] + string.hexdigits[16 : 22] else 
                                    string.hexdigits[string.hexdigits.index(char) + 6] for char in hex(integer)[2:]]))

        except:
            self.write_to_field(1, "Error")

    def change_mode(self, mode, kind):
        for toggler in self.modes_togglers:
            if self.modes_togglers.index(toggler) < 4 and kind == 0:
                toggler["bg"] = "#7b79ed"
                toggler["fg"] = "black"

            elif self.modes_togglers.index(toggler) > 3 and kind == 1:
                toggler["bg"] = "#a579ed"
                toggler["fg"] = "black"

            else:
                None

        if kind == 0:
            self.format_label["text"] = mode + "\n" + self.format_label["text"].split("\n")[1]
            self.modes_togglers[self.modes_set.index(mode)]["bg"] = "#132d40"
            self.modes_togglers[self.modes_set.index(mode)]["fg"] = "white"

        else:
            self.format_label["text"] = self.format_label["text"].split("\n")[0] + "\n" + mode
            self.modes_togglers[self.modes_set.index(mode) + 4]["bg"] = "#231340"
            self.modes_togglers[self.modes_set.index(mode) + 4]["fg"] = "white"

        self.run()
        self.checker()

    def swap(self):
        from_mode, to_mode = self.format_label["text"].split("\n")

        if self.output_field.get() == "Error":
            self.clear()

        else:
            self.write_to_field(2)

        self.change_mode(from_mode, 1)
        self.change_mode(to_mode, 0)

    def checker(self):
        for button in self.buttons:
            button["state"] = DISABLED

        for i in range(self.modes_set_sys[self.modes_set.index(self.format_label["text"].split("\n")[0])]):
            self.buttons[i]["state"] = NORMAL

if __name__ == "__main__":
    root = Tk()
    root.title("Converter")
    app = Application(master = root)
    app.mainloop()