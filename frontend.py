from tkinter import *
from backend import Database

database = Database("books.db")


class Window(object):

    def __init__(self, window):
        self.window = window
        self.window.wm_title('BookStore')

        l1 = Label(self.window, text='Title')
        l1.grid(row=0, column=0)

        l2 = Label(self.window, text='Author')
        l2.grid(row=0, column=3)

        l3 = Label(self.window, text='Year')
        l3.grid(row=1, column=0)

        l4 = Label(self.window, text='ISBN')
        l4.grid(row=1, column=3)

        self.title_text = StringVar()
        self.e1 = Entry(self.window, textvariable=self.title_text)
        self.e1.grid(row=0, column=1)

        self.author_text = StringVar()
        self.e2 = Entry(self.window, textvariable=self.author_text)
        self.e2.grid(row=0, column=4)

        self.year_text = StringVar()
        self.e3 = Entry(self.window, textvariable=self.year_text)
        self.e3.grid(row=1, column=1)

        self.isbn_text = StringVar()
        self.e4 = Entry(self.window, textvariable=self.isbn_text)
        self.e4.grid(row=1, column=4)

        self.list = Listbox(self.window, height=10, width=40)
        self.list.grid(row=2, column=0, rowspan=7, columnspan=2, padx=4)

        sb = Scrollbar(self.window)
        sb.grid(row=2, column=2, rowspan=7)

        self.list.configure(yscrollcommand=sb.set)
        sb.configure(command=self.list.yview)

        self.list.bind("<<ListboxSelect>>", self.get_selected_row)

        b1 = Button(self.window, text='View all', width=12, command=self.view_command)
        b1.grid(row=2, column=4)

        b2 = Button(self.window, text='Search Entry', width=12, command=self.search_command)
        b2.grid(row=3, column=4)

        b3 = Button(self.window, text='Add Entry', width=12, command=self.add_command)
        b3.grid(row=4, column=4)

        b4 = Button(self.window, text='Update', width=12, command=self.update_command)
        b4.grid(row=5, column=4)

        b5 = Button(self.window, text='Delete', width=12, command=self.delete_command)
        b5.grid(row=6, column=4)

        b6 = Button(self.window, text='Clear', width=12, command=self.clear_command)
        b6.grid(row=7, column=4)

        b7 = Button(self.window, text='Close', width=12, command=self.window.destroy)
        b7.grid(row=8, column=4, padx=5, pady=2)

    def get_selected_row(self, event):
        try:
            global selected_tuple
            index = self.list.curselection()[0]
            selected_tuple = self.list.get(index)
            self.e1.delete(0, END)
            self.e1.insert(END, selected_tuple[1])
            self.e2.delete(0, END)
            self.e2.insert(END, selected_tuple[2])
            self.e3.delete(0, END)
            self.e3.insert(END, selected_tuple[3])
            self.e4.delete(0, END)
            self.e4.insert(END, selected_tuple[4])
        except IndexError:
            pass

    def view_command(self):
        self.list.delete(0, END)
        for row in database.view():
            self.list.insert(END, row)

    def search_command(self):
        self.list.delete(0, END)
        for row in database.search(self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get()):
            self.list.insert(END, row)

    def add_command(self):
        database.insert(self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get())
        self.list.delete(0, END)
        self.list.insert(END, (self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get()))

    def delete_command(self):
        database.delete(selected_tuple[0])

    def update_command(self):
        database.update(selected_tuple[0], self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get())
        self.list.delete(0, END)
        self.list.insert(END, (self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get()))

    def clear_command(self):
        self.e1.delete(0, END)
        self.e2.delete(0, END)
        self.e3.delete(0, END)
        self.e4.delete(0, END)


app = Tk()
Window(app)
app.mainloop()
