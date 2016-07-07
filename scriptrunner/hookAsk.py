try:
    # for Python2
    import Tkinter as tk
    import tkMessageBox as mb
except ImportError:
    # for Python3
    import tkinter as tk
    import tkinter.messagebox as mb

doGui = True
if doGui:
   top = tk.Tk()
   top.withdraw()
   mb.askquestion("Override rebsssssssssse hook", "Are You Sure? maybe you asdasdadasdasdasdasdd  dds  sss", icon='warning')
   if 'yes':
       print("Deleted")
   else:
       print("I'm Not Deleted Yet")
