import os, tkinter, re, sys
from tkinter import *
from tkinter import ttk, filedialog, messagebox

src = os.path.join(os.path.expanduser("~"), 'Downloads')
dest = os.path.join(os.path.expanduser("~"), 'Pictures/Wallpapers/Bing')

def move_file(src, dest):
    if os.path.exists(src):
        os.rename(src, dest)

def get_file_size(file):
    if os.path.exists(file):
        size = os.path.getsize(file)
        if size < 1024:
            return str(size) + ' B'
        elif size < 1024 * 1024:
            return str(round(size / 1024, 2)) + ' KB'
        elif size < 1024 * 1024 * 1024:
            return str(round(size / 1024 / 1024, 2)) + ' MB'
        else:
            return str(round(size / 1024 / 1024 / 1024, 2)) + ' GB'
    else:
        return 0

def get_next_name():
    i = 0
    for file in os.listdir(dest):
        if re.match(r'^[0-9]+.jpg$', file):
            if i < int(file.split('.')[0]):
                i = int(file.split('.')[0])
    return str(int(i) + 1)

def transfer_pictures(src, dest):
    for file in os.listdir(src):
        if re.match(r'^BingWallpaper.*\.jpg$', file):
            print(file)
            move_file(os.path.join(src, file), os.path.join(dest, get_next_name() + '.jpg'))

def open_path(path):
    if sys.platform == 'win32':
        os.startfile(path)
    elif sys.platform == 'darwin':
        os.system(f'open "{path}"')
    else:
        os.system(f'xdg-open "{path}"')

class App(Tk):
    def __init__(self, master=None):
        super().__init__(master)
        self.title('Bing Wallpaper Transfer')
        # self.geometry('300x100')
        self.protocol('WM_DELETE_WINDOW', self.quit)

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(expand=True, fill=BOTH)

        self.src = StringVar()
        self.src.set(os.path.join(os.path.expanduser("~"), 'Downloads'))
        self.src_frame = ttk.Frame(self.main_frame)
        self.src_frame.pack(side=TOP, fill=X, expand=False, padx=5, pady=5)
        self.src_label = ttk.Label(self.src_frame, text='Source:')
        self.src_label.pack(side=LEFT)
        self.src_entry = ttk.Entry(
            self.src_frame, 
            textvariable=self.src, 
            validate="all", 
            validatecommand=self.update_src, 
            width=50,
            state='readonly',
        )
        self.src_entry.pack(side=LEFT, fill=X, expand=True)
        self.src_button = ttk.Button(self.src_frame, text='Browse', command=self.get_src)
        self.src_button.pack(side=LEFT)

        self.dest = StringVar()
        self.dest.set(os.path.join(os.path.expanduser("~"), 'Pictures/Wallpapers/Bing'))
        self.dest_frame = ttk.Frame(self.main_frame)
        self.dest_frame.pack(side=TOP, fill=X, expand=False, padx=5, pady=5)
        self.dest_label = ttk.Label(self.dest_frame, text='Destination:')
        self.dest_label.pack(side=LEFT)
        self.dest_entry = ttk.Entry(
            self.dest_frame, 
            textvariable=self.dest, 
            width=50,
            state='readonly',
        )
        self.dest_entry.pack(side=LEFT, fill=X, expand=True)
        self.dest_button = ttk.Button(self.dest_frame, text='Browse', command=self.get_dest)
        self.dest_button.pack(side=LEFT)

        self.button_frame = ttk.Frame(self.main_frame)
        self.button = ttk.Button(self.button_frame, text='Transfer', command=self.transfer)
        self.button.pack(side='left', padx=5, pady=5)
        self.refresh_button = ttk.Button(self.button_frame, text='Refresh', command=self.refresh)
        self.refresh_button.pack(side='left', padx=5, pady=5)
        self.quit_button = ttk.Button(self.button_frame, text='Quit', command=self.quit)
        self.quit_button.pack(side='left', padx=5, pady=5)
        self.button_frame.pack(side=BOTTOM, expand=False)

        self.file_list = ttk.Treeview(self.main_frame, columns=('File', 'Size'), show='headings')
        self.file_list.heading('File', text='File')
        self.file_list.heading('Size', text='Size')
        self.file_list.column('File', width=450)
        self.file_list.column('Size', width=10)
        self.file_list.pack(side=TOP, fill=BOTH, expand=True)
        self.file_list.bind('<Double-1>', self.open_file)

        self.refresh()

    def open_file(self, event):
        file = self.file_list.item(self.file_list.focus(), 'values')[0]
        if os.path.exists(os.path.join(self.src.get(), file)):
            open_path(os.path.join(self.src.get(), file))
        else:
            self.refresh()

    def refresh(self):
        self.file_list.delete(*self.file_list.get_children())
        for file in os.listdir(self.src.get()):
            if re.match(r'^BingWallpaper.*\.jpg$', file):
                self.file_list.insert('', 'end', values=(file, get_file_size(os.path.join(self.src.get(), file))))

    def update_src(self):
        self.refresh()

    def get_src(self):
        src = filedialog.askdirectory(initialdir=self.src.get())
        if src:
            self.src.set(src)

    def get_dest(self):
        dest = filedialog.askdirectory(initialdir=self.dest.get())
        if dest:
            self.dest.set(dest)

    def transfer(self):
        if os.path.isdir(self.src.get()) and os.path.isdir(self.dest.get()):
            transfer_pictures(self.src.get(), self.dest.get())
            messagebox.showinfo('Success', 'Transfer completed.')
            if os.path.isdir(self.dest.get()):
                open_path(self.dest.get())
        else:
            messagebox.showinfo('Failure', 'Source or destination is not a directory.')
        self.refresh()

    def quit(self):
        self.destroy()


if __name__ == '__main__':
    App().mainloop()