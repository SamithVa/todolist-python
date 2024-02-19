import os
import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from DragAndDropListBox import *

import random

# Make the Dpi look more clear on window
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

PROGRAM_NAME = 'TKINTER TODO LIST'
file_name = None

# Color Theme
color_schemes = {
    'Default': '#000000.#FFFFFF',
    'Gregarious': '#83406A.#D1D4D1',
    'Aquamarine': '#5B8340.#D1E7E0',
    'Bold Beige': '#4B4620.#FFF0E1',
    'Cobalt Blue': '#ffffBB.#3333aa',
    'Olive Green': '#D1E7E0.#5B8340',
    'Night Mode': '#FFFFFF.#000000',
}


class MyApp:
    def __init__(self, M):

        # 导入 File 中的图标
        to_do_icon = PhotoImage(file='icons/to_do_list_icon.png')
        new_file_icon = PhotoImage(file='icons/new_file.png')
        open_file_icon = PhotoImage(file='icons/open_file.png')
        save_file_icon = PhotoImage(file='icons/save.png')
        close_icon = PhotoImage(file='icons/close.png')

        # 导入颜色的图标
        default = PhotoImage(file='color_icons/default.png')
        aquamarine = PhotoImage(file='color_icons/aquamarine.png')
        bold_beige = PhotoImage(file='color_icons/bold_beige.png')
        cobalt_blue = PhotoImage(file='color_icons/cobalt_blue.png')
        gregarious = PhotoImage(file='color_icons/gregarious.png')
        olive_green = PhotoImage(file='color_icons/olive_green.png')
        night_mode = PhotoImage(file='color_icons/night_mode.png')

        # 创建菜单
        self.master = M
        self.master.rowconfigure(0, weight=1)
        self.master.iconphoto(False, to_do_icon)
        menu = Menu(self.master)
        self.master.configure(menu=menu)

        # File 菜单
        fileMenu = Menu(menu, tearoff=0)
        menu.add_cascade(label='File', menu=fileMenu)
        fileMenu.add_command(label='New', compound='left', image=new_file_icon,
                             accelerator='Ctrl+N', command=self.new_file)
        fileMenu.add_command(label='Open...', compound='left', image=open_file_icon,
                             accelerator='Ctrl+O', command=self.open_file)
        fileMenu.add_command(label='Save', compound='left', image=save_file_icon,
                             accelerator='Ctrl+S', command=self.save)
        fileMenu.add_command(label='Save as ...', compound='left', image=save_file_icon,
                             accelerator='Shift+Ctrl+S', command=self.save_as)
        fileMenu.add_separator()
        fileMenu.add_command(label='Exit', compound='left', image=close_icon,
                             accelerator='Alt+F4', command=self.exit)

        # Theme 菜单
        themeMenu = Menu(menu, tearoff=0)
        menu.add_cascade(label='Theme', menu=themeMenu)
        self.theme_choice = StringVar()
        self.theme_choice.set('Default')
        self.change_theme()
        color_dic = {
            'aquamarine': aquamarine,
            'bold_beige': bold_beige,
            'cobalt_blue': cobalt_blue,
            'default': default,
            'gregarious': gregarious,
            'night_mode': night_mode,
            'olive_green': olive_green
        }
        for color in sorted(color_schemes):
            color_image_name = color.lower().replace(' ', '_')
            themeMenu.add_radiobutton(label=color, variable=self.theme_choice, compound=LEFT,
                                      image=color_dic[color_image_name],
                                      command=self.change_theme)

        # About 菜单
        aboutMenu = Menu(menu, tearoff=0)
        menu.add_command(label='About', command=self.about, compound=LEFT)

        # 标题一
        lbl_title = Label(self.master, text='To-Do-List', font=('Arial', 15), bg='white')
        lbl_title.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        # 显示一个空字符串在 "To do List" 标题下面
        self.lbl_display = Label(self.master, text='', font=('Arial', 12), bg='white')
        self.lbl_display.grid(row=1, column=0, columnspan=2, sticky=NSEW)

        # 用户输入框格
        self.input = StringVar()
        self.txt_input = Entry(self.master, width=25, border=4, textvariable=self.input,
                               font=('Arial', 10))
        self.txt_input.insert(0, 'Enter Your Task Here ...')
        self.txt_input.bind('<Return>', self.add_task)

        # 当输入按输入框格时删除里面的字符串
        self.txt_input.bind('<Button-1>', lambda a: self.txt_input.delete(0, 'end'))

        self.txt_input.grid(row=2, column=0, sticky=NSEW, pady=5, padx=5)

        # 所有右边的按钮
        btn_add_task = Button(self.master, text='Add Task', command=self.add_task)
        btn_add_task.grid(row=2, column=1, sticky=NSEW, padx=2, pady=0)

        btn_del_all = Button(self.master, text='Delete All Tasks', command=self.del_all)
        btn_del_all.grid(row=3, column=1, sticky=NSEW, pady=5, padx=2)

        btn_del_one = Button(self.master, text='Delete One Task', command=self.del_one)
        btn_del_one.grid(row=4, column=1, sticky=NSEW, pady=5, padx=2)

        btn_sort_asc = Button(self.master, text='Sort Ascending', command=self.sort_asc)
        btn_sort_asc.grid(row=5, column=1, sticky=NSEW, pady=5, padx=2)

        btn_sort_desc = Button(self.master, text='Sort Descending', command=self.sort_desc)
        btn_sort_desc.grid(row=6, column=1, sticky=NSEW, pady=5, padx=2)

        btn_choose_random = Button(self.master, text='Choose Random',
                                   command=self.choose_random)
        btn_choose_random.grid(row=7, column=1, sticky=NSEW, pady=5, padx=2)

        btn_number_tasks = Button(self.master, text='Number of Tasks',
                                  command=self.show_number_tasks)
        btn_number_tasks.grid(row=8, column=1, sticky=NSEW, pady=5, padx=2)

        btn_exit = Button(self.master, text='Exit', command=self.exit)
        btn_exit.grid(row=9, column=1, sticky=NSEW, pady=5, padx=2)

        # 一开始创建一个空字符串列表用来保存任务
        self.tasks = []

        # 事件绑定
        self.master.bind('<Control-N>', self.new_file)
        self.master.bind('<Control-n>', self.new_file)
        self.master.bind('<Control-s>', self.save)
        self.master.bind('<Control-S>', self.save_as)
        self.master.bind('<Control-o>', self.open_file)
        self.master.bind('<Control-O>', self.open_file)

        # 用 List Box 来显示数据
        self.lb_tasks = Drag_and_Drop_Listbox(self.master)
        self.lb_tasks.config(borderwidth=5)
        self.lb_tasks.grid(row=3, column=0, rowspan=8, sticky=NSEW)

        self.master.protocol('WM_DELETE_WINDOW', self.exit)
        self.master.mainloop()

    # 加入新的任务
    def add_task(self, event=None):
        newTask = self.input.get()
        if newTask != '' and newTask != '\n' and newTask != 'Enter Your Task Here ...' and newTask not in self.tasks:
            print("Added Task:" + self.input.get())
            self.tasks.append(newTask)
            self.txt_input.delete(0, END)
            self.update_listbox()
        # 当用户输入已经存在的任务时 删除输入框格的字符
        elif newTask in self.tasks:
            self.txt_input.delete(0, END)

    # 用来更新 listbox 的数据
    def update_listbox(self):
        self.clear_listbox()
        for task in self.tasks:
            self.lb_tasks.insert('end', task)

    # 删除 listbox 的所有元素
    def clear_listbox(self):
        self.lb_tasks.delete(0, 'end')

    # 删除的所有任务
    def del_all(self):
        confirm_delete = messagebox.askokcancel(self.master, 'Confirm to delete all tasks')
        if confirm_delete:
            print('Delete All is Clicked')
            self.tasks = []
            self.lb_tasks.delete(0, 'end')

    # 删除的一个任务
    def del_one(self):
        print('Delete one is Clicked')
        # Get the text of the currently selected item
        task = self.lb_tasks.get('active')
        if task in self.tasks:
            self.tasks.remove(task)
        self.update_listbox()

    # 把任务按字符排列从小到大
    def sort_asc(self):
        self.tasks.sort()
        self.clear_listbox()
        self.update_listbox()

    # 把任务按字符排列从大到小
    def sort_desc(self):
        self.tasks.sort(reverse=True)
        self.clear_listbox()
        self.update_listbox()

    # 显示目前的任务个数
    def show_number_tasks(self):
        count = len(self.tasks)
        t = 'Tasks number: ' + str(count)
        self.lbl_display.configure(text=t)

    # 随机地选一个任务
    def choose_random(self):
        # Choose a random task
        tmp = self.lbl_display.cget('text')[len("Your random task is: "):]
        if len(self.tasks) != 0:
            task = random.choice(self.tasks)
            while tmp == task:
                task = random.choice(self.tasks)
                if len(self.tasks) == 1:
                    break
            task = "Your random task is: " + task

            # 显示结果给用户
            self.lbl_display.configure(text=task)

    # 换外观
    def change_theme(self, event=None):
        selected_theme = self.theme_choice.get()
        print(self.theme_choice.get())
        fg_bg_colors = color_schemes.get(selected_theme)
        foreground_color, background_color = fg_bg_colors.split('.')
        print(foreground_color, background_color)

        # 把所有 widget 换颜色
        self.master.configure(bg=background_color)
        self.change_color(background_color, foreground_color, self.master)

    # 把所有 widget 换颜色
    def change_color(self, background_color, foreground_color, container=None):
        for child in container.winfo_children():
            if type(child) is Frame:
                for c in child.winfo_children():
                    if type(c) == Button or type(c) == Label:
                        c.config(fg=foreground_color, bg=background_color)
            elif type(child) == Label or type(child) == Button or type(child) == Entry or type(
                    child) == Drag_and_Drop_Listbox:
                child.config(fg=foreground_color, bg=background_color)

    # 用户创建一个新文件
    def new_file(self, event=None):
        self.master.title("Untitled")
        global file_name
        file_name = None
        self.tasks = []
        self.update_listbox()

    # 用户打开一个文件 而且只允许打开 txt 文件
    def open_file(self, event=None):
        input_file_name = tkinter.filedialog.askopenfilename(defaultextension=".txt",
                                                             filetypes=[("All Files", "*.*"),
                                                                        ("Text Documents", "*.txt")])
        if input_file_name:
            global file_name
            file_name = input_file_name
            self.tasks = []
            self.master.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME))
            with open(file_name) as _file:
                for task in _file.readlines():
                    if task != '\n':
                        self.tasks.append(task)
                self.update_listbox()

    # 用户保存目前存在的任务
    def save(self, event=None):
        global file_name
        if not file_name:
            self.save_as()
        else:
            self.write_to_file(file_name)
        return "break"

    # 用户保存目前存在的任务到电脑的一个位置
    def save_as(self, event=None):
        input_file_name = tkinter.filedialog.asksaveasfilename(defaultextension=".txt",
                                                               filetypes=[("All Files", "*.*"),
                                                                          ("Text Documents", "*.txt")])
        if input_file_name:
            global file_name
            file_name = input_file_name
            self.write_to_file(file_name)
            self.master.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME))
        return "break"

    # 写到txt文件 如果存在错误显示给用户
    def write_to_file(self, file_name):
        try:
            with open(file_name, 'w') as the_file:
                for task in self.tasks:
                    the_file.write(task)
                    the_file.write('\n')
        except IOError:
            messagebox.showwarning("Save", "Could not save the file.")

    # 退出软件
    def exit(self, event=None):
        msgbox = messagebox.askyesno('Exit', 'Are you sure you want to exit the application?')
        if msgbox:
            self.master.destroy()
        else:
            return

    # 显示软件的信息
    def about(self, event=None):
        messagebox.showinfo('About', 'Tkinter To Do List Version 1.0')
