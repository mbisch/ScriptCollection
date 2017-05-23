import wx
from wx import xrc
from threading import *
from gen_docu import JmsDocGenerator

EVT_RESULT_ID = wx.NewId()
def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_RESULT_ID, func)

class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data

class WorkerThread(Thread):
    """Worker Thread Class."""
    def __init__(self, user, pw, db, dest, filename, gen_ins, notify_window):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.user = user
        self.pw = pw
        self.db = db
        self.dest = dest
        self.filename = filename
        self.gen_ins = gen_ins
        self._notify_window = notify_window
        self.dGen = JmsDocGenerator(is_wx=True)
        self.start()

    def run(self):
        """Run Worker Thread."""
        self.dGen.getConnection(self.user, self.pw, self.db)
        self.dGen.openWorkbook(self.filename)
        self.dGen.enable_code_gen(self.gen_ins)
        self.dGen.fillExcel(self.dest)
        self.dGen.close_all()

        wx.PostEvent(self._notify_window, ResultEvent('Done'))

    def abort(self):
        """abort worker thread."""
        # Method for use by main thread to signal an abort
        self._want_abort = 1

class MyApp(wx.App):

    def __init__(self, redirect):
        super(self.__class__, self).__init__(redirect)
        self.worker = None
        EVT_RESULT(self, self.OnResult)
        self.start_btn = None

    def OnInit(self):
        self.res = xrc.XmlResource('gui.xrc')
        self.init_frame()
        return True

    def init_frame(self):
        self.frame = self.res.LoadFrame(None, 'mainFrame')
        self.bind_buttons()
        self.frame.Show()

    def bind_buttons(self):
        self.frame.Bind(wx.EVT_BUTTON, self.OnStart, id=xrc.XRCID("m_button_start"))

    def OnStart(self, evt):
        self.start_btn = evt.GetEventObject()
        self.start_btn.Disable()

        db = xrc.XRCCTRL(self.frame, 'm_textCtrl_db').GetValue()
        user = xrc.XRCCTRL(self.frame, 'm_textCtrl_user').GetValue()
        pw = xrc.XRCCTRL(self.frame, 'm_textCtrl_pw').GetValue()
        dest = xrc.XRCCTRL(self.frame, 'm_textCtrl_dest').GetValue()
        filename = xrc.XRCCTRL(self.frame, 'm_textCtr_file').GetValue()
        gen_ins = xrc.XRCCTRL(self.frame, 'm_check_gen_ins').GetValue()

        if not self.worker:
            self.worker = WorkerThread(user, pw, db, dest, filename, gen_ins, self)


    def OnResult(self, event):
        self.start_btn.Enable()
        self.worker = None

if __name__ == '__main__':
    app = MyApp(redirect = False)
    app.MainLoop()