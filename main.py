from AppInterface import *


def main():
    # Create root window
    root = Tk()

    # change root window background color
    root.configure(bg='#FFF0E1')
    root.columnconfigure(0, weight=1)
    # root.columnconfigure(1, weight=1)

    # Change the title
    root.title('Tkinter To Do List')

    # Change the window size
    root.geometry('800x800')
    root.resizable(FALSE, FALSE)
    app = MyApp(root)


main()
