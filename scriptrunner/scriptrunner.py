from __future__ import print_function
import threading
import time
import queue

import os, fnmatch
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk


class FuncThread(threading.Thread):
    def __init__(self, func, *args, **kwargs):
        threading.Thread.__init__(self)
        self.func = func          # function to call
        self.args = args          # optional positional argument(s) for call
        self.kwargs = kwargs      # optional keyword argument(s) for call
        self.runable = True
        print('KWARGS',self.kwargs)
    def run(self):
        self.func(*self.args, **self.kwargs)

class AutoScrollbar(ttk.Scrollbar):
    # a scrollbar that hides itself if it's not needed.  only
    # works if you use the grid geometry manager.
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        ttk.Scrollbar.set(self, lo, hi)

class SrWidget():
    def __init__(self, element):
        self.label_text = None
        self.type  = None
        self.var   = None
        self.element = element

        if 'Label' in self.element:
            self.label_text = self.element['Label']
        if 'Type' in self.element:
            self.type = self.element['Type']
        if 'Var' in self.element:
            self.var = self.element['Var']
        if 'Name' in self.element:
            self.name = self.element['Name']

class TextEntry(SrWidget):
    def __init__(self, left, right, element = {}):
        super(TextEntry, self).__init__(element=element)
        self.left = left
        self.right = right

        if 'Show' in self.element:
            self.show = self.element['Show']

        self.label = ttk.Label(left, text = self.label_text, anchor = tk.E)
        self.label.pack(side=tk.TOP, expand=True, fill=tk.X)

        self.entry = ttk.Entry(right, show = self.show, textvariable = self.var)
        self.entry.pack(side=tk.TOP, expand=True, fill=tk.X)

class FileNameEntry(SrWidget):
    def __init__(self, left, right, element = {}):
        super(FileNameEntry, self).__init__(element=element)
        self.left = left
        self.right = right

        self.label = ttk.Label(left, text = self.label_text, anchor = tk.E)
        self.label.pack(side=tk.TOP, expand = True, fill = tk.X)

        self.button = ttk.Button(right, text='...', command=self.askopenfile)
        self.button.pack(side=tk.TOP, expand = True, fill = tk.X)

    def askopenfile(self, SetFileName = True):
        """Returns file name and sets button text."""
        self.var.set(tk.filedialog.askopenfilename())
        if SetFileName:
            self.button.config(text = self.var.get())

class DirectoryNameEntry(SrWidget):
    def __init__(self, left, right, element = {}):
        super(DirectoryNameEntry, self).__init__(element=element)
        self.left = left
        self.right = right

        self.label = ttk.Label(left, text = self.label_text, anchor = tk.E)
        self.label.pack(side=tk.TOP, expand = True, fill = tk.X)

        self.button = ttk.Button(right, text='...', command=self.askdirectory)
        self.button.pack(side=tk.TOP, expand = True, fill = tk.X)

    def askdirectory(self, SetFileName = True):
        """Returns file name and sets button text."""
        self.var.set(tk.filedialog.askdirectory())
        if SetFileName:
            self.button.config(text = self.var.get())

class ActionButton(SrWidget):
    def __init__(self, frame, element = {}, stdouts = None):
        super(ActionButton, self).__init__(element=element)
        self.frame = frame

        self.action = 'Run'
        self.args   = []
        self.kwargs = {}
        self.queue = None
        self.func = None
        self.stdouts = stdouts
        self.stdout_name = None
        self.active_stdout = None

        if 'Action' in element:
            self.action = element['Action']
        if 'Function' in element:
            self.func = element['Function']
        if 'Args' in element:
            self.args = element['Args']
        if 'Kwargs' in element:
            self.kwargs = element['Kwargs']
            if 'OutQueue' in element['Kwargs']:
                self.queue = element['Kwargs']['OutQueue']
        if 'StdoutName' in element:
            self.stdout_name = element['StdoutName']
        if 'OutQueue' in element and self.queue == None:
            self.queue = element['OutQueue']

        self.labelFrame = ttk.LabelFrame(self.frame, text = self.label_text)
        self.labelFrame.pack(side=tk.LEFT)
        self.button = ttk.Button(self.labelFrame , text=self.action, command=self.run)
        self.button.pack(side=tk.LEFT,expand=True, fill='both')

    def check_thread(self, mt):
        # Still alive? Check again in half a second
        if mt.isAlive() or (self.queue != None and not self.queue.empty()):
            if self.active_stdout == None:
                if self.stdout_name != None and self.stdout_name in self.stdouts:
                    self.active_stdout = self.stdouts[self.stdout_name]
                elif len(self.stdouts.keys()) > 0:
                    self.active_stdout = self.stdouts[self.stdouts.keys()[0]]
            if self.active_stdout != None:
                self.active_stdout.configure(state='normal')
                while not self.queue.empty():
                    item = self.queue.get()
                    self.active_stdout.insert(tk.constants.END, item)
                    self.queue.task_done()
                self.active_stdout.configure(state='disabled')
            self.frame.after(500, self.check_thread, mt)
        else:
            self.button.config(state='active')


    def run(self):
        print('Start Function')
        self.button.config(state='disabled')
        self.mt = FuncThread(self.func,**(self.kwargs))
        self.mt.start()
        self.check_thread(self.mt)



class FileDirTree(SrWidget):
    def __init__(self, frame, element={}, is_file = True):
        super(FileDirTree, self).__init__(element=element)
        self.frame = frame
        self.match = tk.StringVar()
        self.is_file = is_file
        self.dirs = {}
        self.dests = {}
        self.search_sub_dir = tk.IntVar()
        self.search_sub_dir.set(1)

        if 'FileTypes' in element:
            self.match.set(element['FileTypes'])

        if 'Expandable' in element:
            self.expand = element['Expandable']

        self.f1 = ttk.LabelFrame(self.frame, text = self.label_text)
        self.f1.pack(side=tk.TOP, expand=self.expand, fill='both')

        self.tf = ttk.Frame(self.f1)
        self.tf.pack(side=tk.TOP, expand=True, fill='both')

        self.tree = ttk.Treeview(self.tf, height='3', show='tree')
        self.ysb = ttk.Scrollbar(self.tf, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=self.ysb.set)

        self.tree.pack(side = tk.LEFT, expand=True, fill='both')
        self.ysb.pack(side = tk.LEFT, expand = False, fill = tk.Y)

        self.bf = ttk.Frame(self.f1)
        self.bf.pack( side=tk.TOP, expand=False, fill=tk.X)

        self.button1 = ttk.Button(self.bf, text='Add directory', command=self.AddDirectory)
        self.button1.pack(side = tk.LEFT,expand = False,anchor = tk.S)

        # create a popup menu
        self.aMenu = tk.Menu(self.frame, tearoff=0)
        self.aMenu.add_command(label="Remove", command=self.RemoveItem)

        # attach popup to frame
        self.tree.bind("<Button-3>", self.Popup)

        if self.is_file:
            self.button2 = ttk.Button(self.bf, text='Add file', command=self.AddFile)
            self.button2.pack(side = tk.LEFT,expand = False,anchor = tk.S)

            sep = ttk.Separator(self.bf, orient=tk.VERTICAL)
            sep.pack(side=tk.LEFT, expand=True, fill=tk.Y)

            self.cb = ttk.Checkbutton(self.bf, text="Sub directories", variable=self.search_sub_dir)
            self.cb.pack(side = tk.RIGHT,expand = False,anchor = tk.S)

            self.ef = ttk.LabelFrame(self.bf, text='File Type')
            self.ef.pack(side=tk.RIGHT, expand=False)

            self.TypeRegex = ttk.Entry(self.ef,  textvariable=self.match)
            self.TypeRegex.pack(side = tk.LEFT,expand = True, fill='both')

            self.button3 = ttk.Button(self.bf, text='Find all', command=self.find_all)
            self.button3.pack(side=tk.RIGHT, expand=False, anchor=tk.S)

    def Popup(self, event):
        """action in event of button 3 on tree view"""
        # select row under mouse
        iid = self.tree.identify_row(event.y)
        if iid:
            self.current_iid = iid
            self.aMenu.post(event.x_root, event.y_root)
        else:
            # mouse pointer not over item
            # occurs when items do not fill frame
            # no action required
            pass

    def RemoveItem(self):
        print(self.tree.item(self.current_iid ))
        dkey = self.tree.item(self.current_iid)['values']
        for key in self.dirs[dkey[0]].keys():
            self.dests.pop(key,None)
        self.tree.delete(self.current_iid)
        del self.var[:]
        for key in self.dests:
            if self.dests[key] or not self.is_file:
                self.var += [key]

    def ClearTree(self):
        self.tree.delete(*self.tree.get_children())

    def SplitDir(self,path, dest):
        if (path in self.dirs and dest in self.dirs[path]) or len(path) == 0:
            return
        if path in self.dirs:
            self.dirs[path][dest] = True
        else:
            self.dirs[path] = {dest:True}
        splits = os.path.split(path)
        self.SplitDir(path=splits[0],dest=dest)

    def FindFiles(self):
        new_dests = {}
        print('SubDirs',self.search_sub_dir.get())
        for dir in self.dests:
            #skip files
            if self.dests[dir]: continue
            for (dirpath, dirnames, filenames) in os.walk(dir):
                for name in filenames:
                    path = os.path.join(dirpath,name)
                    if path not in self.dests:
                        for type in self.match.get().split(';'):
                            if fnmatch.fnmatch(path, type):
                                new_dests[path] = True
                                break
                if self.search_sub_dir.get()==0: break
        self.dests.update(new_dests)

    def BuildTree(self, do_find_files = False):
        if do_find_files:
            self.FindFiles()
        self.dirs = {}
        for dest in self.dests:
            self.SplitDir(path = dest, dest=dest)
        del self.var[:]
        for key in self.dests:
            if self.dests[key] or not self.is_file:
                self.var += [key]

        self.ClearTree()
        added = {}
        for dir in sorted(list(self.dirs.keys())):
            splits = os.path.split(dir)
            if splits[0] in added:
                added[dir] = self.tree.insert(added[splits[0]], tk.constants.END, text=(splits[1] or splits[0]), values=[dir],open=True)
            else:
                added[dir] = self.tree.insert('', tk.constants.END, text=(splits[1] or splits[0]), values=[dir],open=True)

    def AddDirectory(self):
        """Returns file name and sets button text."""
        dir = tk.filedialog.askdirectory()
        print('AskDir',dir)
        if dir != '':
            dir = os.path.abspath(dir)
            if dir not in self.dests:
                self.dests[dir] = False
            self.BuildTree(do_find_files = False)

    def AddFile(self):
        """Returns file name and sets button text."""
        file = tk.filedialog.askopenfilename()
        print('AskDir', file)
        if file != '':
            file = os.path.abspath(file)
            if file not in self.dests:
                print(file)
                self.dests[file] = True
            self.BuildTree(do_find_files = False)

    def find_all(self):
        self.BuildTree(do_find_files = True)


class ScriptRunner(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.entries = {}
        self.stdouts = {}
        self.vpanes = []
        self.frames = []
        self.panes = []

        self.panedw = tk.PanedWindow(self, orient='vertical', showhandle=1,width=1000, height=1000)
        self.panedw.pack(expand=True, fill='both')
        self.minheigth = 0


    def get_srwidget_name(self,widget):
        name = widget.name
        if name == None:
            name == '__GenName_'+str(len(self.entries.keys))
        return name


    def addPanel(self,pwd,titel, minsize=0, new_pane = True, expand = True):
        f = None
        if new_pane or len(self.vpanes) == 0:
            f = tk.Frame(pwd)
            pwd.add(f,minsize=minsize)
        else:
            f = self.vpanes[-1].master
        lf = ttk.LabelFrame(f, text=titel)
        self.vpanes += [lf]
        lf.pack(side=tk.TOP, expand=expand, fill='both')
        return self.vpanes[-1]

    def addOneColumns(self, frame):
        f = ttk.Frame(frame)
        self.frames += [f]
        f.pack(side=tk.TOP,expand=True, fill='both')
        return [self.frames[-1]]

    def addTwoColumns(self,frame):
        f = ttk.Frame(frame)
        self.frames += [f]
        f.pack(side = tk.TOP,expand=False, fill='both')

        fl = ttk.Frame(f)
        self.frames += [fl]
        fl.pack(side=tk.LEFT, expand=False, fill='both')

        fr = ttk.Frame(f)
        self.frames += [fr]
        fr.pack(side=tk.LEFT, expand=True, fill='both')
        return self.frames[-2:]

    def add_elements(self,title, elements, new_pane, expand):
        if new_pane or len(self.vpanes)==0:
            self.minheigth = 0
        labelframe = self.addPanel(self.panedw, title,new_pane = new_pane, expand=expand)
        pane = labelframe.master
        frames = []
        ncols = 0
        side = tk.TOP
        W = None
        for ele in elements:
            if 'Type' in ele:
                add_minheigth = 0
                if ele['Type'] in ['FileList','DirList']:
                    if ncols != 1 or side != tk.TOP:
                        frames = self.addOneColumns(labelframe)
                        ncols = 1
                        side = tk.TOP
                elif ele['Type'] in ['Action']:
                        frames = self.addOneColumns(labelframe)
                        ncols = 1
                        side = tk.LEFT
                elif ncols != 2:
                    frames = self.addTwoColumns(labelframe)
                    ncols = 2
                if ele['Type'] == 'Entry':
                    W = TextEntry(left=frames[0], right=frames[1], element = ele)
                elif ele['Type'] == 'File':
                    W = FileNameEntry(left=frames[0], right=frames[1], element=ele)
                elif ele['Type'] == 'Dir':
                    W = DirectoryNameEntry(left=frames[0], right=frames[1], element=ele)
                elif ele['Type'] == 'FileList':
                    W = FileDirTree(frame=frames[0], element=ele, is_file = True)
                    add_minheigth = 130
                elif ele['Type'] == 'DirList':
                    W = FileDirTree(frame=frames[0], element=ele, is_file = False)
                    add_minheigth = 130
                elif ele['Type'] == 'Action':
                    W = ActionButton(frame=frames[0], element=ele, stdouts = self.stdouts)

            if W != None:
                self.entries[self.get_srwidget_name(W)] = W
                self.panedw.update()
                if add_minheigth == 0:
                    add_minheigth = frames[0].winfo_height()
                self.minheigth += add_minheigth

        self.panedw.paneconfigure(pane, minsize=self.minheigth)



    def add_textpad(self, name, title):
        lf = self.addPanel(self.panedw, title,minsize =100,new_pane = True)

        self.textPad = tk.Text(lf, width=100, height=100, state = 'disabled')
        self.ysb = ttk.Scrollbar(lf, orient='vertical', command=self.textPad.yview)
        self.textPad.configure(yscroll=self.ysb.set)
        self.stdouts[name] = self.textPad

        self.textPad.pack(side = tk.LEFT, expand = True, fill = 'both')
        self.ysb.pack(side = tk.LEFT, expand = False, fill = tk.Y)



def WorkerFunc(OutQueue,database,password,files):
    print('WorkerFunc',database.get(),password.get(),files)
    OutQueue.put(database.get())
    OutQueue.put('\n')
    OutQueue.put(password.get())
    OutQueue.put('\n')
    OutQueue.put(files)
    OutQueue.put('\n')
    #for i in range(0, 10):
    #    print("Worker: " + str(i)+"\n")
    #    OutQueue.put("WorkerQueue: " + str(i)+"\n")
    #    time.sleep(1)


def main():

    txt_queue = queue.Queue()
    sr = ScriptRunner()

    database = tk.StringVar()
    password = tk.StringVar()
    git_exe  = tk.StringVar()
    git_dir  = tk.StringVar()
    Files = []

    config_elments = []
    config_elments += [{'Name':'Database','Type':'Entry','Label':'Database','Show':'','Var':database}]
    config_elments += [{'Name':'Password','Type':'Entry','Label':'Password for user WEG','Show':'*','Var':password}]
    config_elments += [{'Name':'GitExe','Type':'File','Label':'Git.exe','Show':'','Var':git_exe}]
    config_elments += [{'Name':'GitInstallDir','Type':'Dir','Label':'git directory','Show':'','Var':git_dir}]
    config_elments += [{'Name': 'FileTree', 'Type': 'FileList', 'Label': None, 'Show': '','Expandable': False,'FileTypes':'*.cbproj', 'Var': Files}]
    config_elments += [{'Name': 'FileTree', 'Type': 'FileList', 'Label': None, 'Show': '', 'Expandable': True, 'FileTypes': '*.cbproj','Var': Files}]
    sr.add_elements(title='Config',elements=config_elments,new_pane=True,expand=True)


    action_elements = []
    action_elements += [{'Name':'Run1','Type':'Action','Label':None,'Action':'Run Script','Function':WorkerFunc,'Kwargs':{'OutQueue':txt_queue,},'StdoutName':'TextPad1'}]
    action_elements += [{'Name': 'Run2', 'Type': 'Action', 'Label': 'Run Script2', 'Action': 'Run', 'Function': WorkerFunc,'Kwargs': {'OutQueue': txt_queue,'database':database,'password':password,'files':Files}, 'StdoutName': 'TextPad1'}]
    sr.add_elements(title='Actions',elements=action_elements,new_pane=False,expand=False)

    sr.add_textpad(name = 'TextPad1', title = 'Output')
    sr.mainloop()

if __name__ == "__main__":
    main()