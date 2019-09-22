import wx
# 导入数据库
from db_operation import Sql_operation


# 系统功能说明
class About(wx.Panel):
    def __init__(self, nb, parent):

        wx.Panel.__init__(self, nb)
        # 用来调用父frame,便于更新
        self.parent = parent
        self.panel = self
        box = wx.BoxSizer(wx.VERTICAL)
        font = wx.Font(pointSize=25, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.BOLD, underline=False)

        logo = wx.StaticText(self.panel, label="系 统 说 明", style=wx.ALIGN_CENTER)
        logo.SetFont(font)

        box.Add(logo, 0, wx.ALIGN_CENTER | wx.TOP, 40)
        #
        lbl = wx.StaticText(self.panel, -1, style=wx.ALIGN_LEFT)

        txt1 = "\n\n    1.用户功能\n"
        txt2 = "      (1) 注册 \n"
        txt3 = "      (2) 设置 \n"
        txt4 = "      (3) 登录 \n"
        txt5 = "      (4) 用户登陆成功后，可以添加、修改、删除、查询个人专利信息，完善个人基本信息; 也可以查询系统中的专利信息。 "
        txt6 = "\n\n    2.管理员 \n"
        txt7 = "      (1) 审核用户 \n"
        txt8 = "      (2) 审核用户申请的专利 "

        txt = txt1 + "\n" + txt2 + "\n" + txt3 + "\n" + txt4 + "\n" + txt5 \
               + "\n" + txt6 + "\n" + txt7 + "\n" + txt8
        font1 = wx.Font(pointSize=15, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL, underline=False)

        lbl.SetFont(font1)
        lbl.SetLabel(txt)

        box.Add(lbl, 0, wx.ALIGN_LEFT)

        self.panel.SetSizer(box)

        cancelButton = wx.Button(self.panel, -1, label=u'退  出', pos=(520, 500), size=(100, 35), style=wx.BORDER_MASK)

        cancelButton.Bind(wx.EVT_BUTTON, self.CancelButton)

    # 退出界面
    def CancelButton(self, event):
        dlg = wx.MessageDialog(self, '确定要退出吗?', '温馨提示', wx.YES_NO | wx.ICON_INFORMATION)
        retCode = dlg.ShowModal()
        if (retCode == wx.ID_YES):
            self.parent.notebook.DeleteAllPages()
            self.parent._mgr.Update()
            self.parent.about_state = 0
        else:
            pass


# 设置界面
class Set_page(wx.Panel):
    def __init__(self, nb, parent):

        # 生成一个500*500的框
        wx.Panel.__init__(self, nb)
        # 用来调用父frame,便于更新
        self.parent = parent
        self.panel = self
        # 最外层布局
        vbox = wx.BoxSizer(wx.VERTICAL)
        # 设置logo
        logo = wx.StaticText(self.panel, -1, label="系 统 设 置", pos=(500, 50))
        font = wx.Font(pointSize=20, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.BOLD, underline=False)
        logo.SetFont(font)

        #
        st_host = wx.StaticText(self.panel, -1, '服务器:')
        st_db =wx.StaticText(self.panel, -1, '数据库:')
        st_port =wx.StaticText(self.panel, -1, '端口:')
        st_name =wx.StaticText(self.panel, -1, '账号:')
        st_password =wx.StaticText(self.panel, -1, '密码:')

        #
        self.serversInput = wx.TextCtrl(self.panel, -1)
        self.databaseInput = wx.TextCtrl(self.panel, -1)
        self.portInput = wx.TextCtrl(self.panel, -1)
        self.accountInput = wx.TextCtrl(self.panel, -1)
        self.passwordInput = wx.TextCtrl(self.panel, -1)
        # 按钮
        btn_submit = wx.Button(self.panel, -1, label=u'保  存', pos=(400, 430), size=(100, 35), style=wx.BORDER_MASK)
        cancelButton = wx.Button(self.panel, -1, label=u'退  出', pos=(600, 430), size=(100, 35), style=wx.BORDER_MASK)
        # 信息布局
        flex = wx.FlexGridSizer(5, 2, 30, 30)
        flex.AddMany([
            (st_host, 0, wx.ALIGN_RIGHT), (self.serversInput, 0, wx.EXPAND),
            (st_db, 0, wx.ALIGN_RIGHT), (self.databaseInput, 0, wx.EXPAND),
            (st_port, 0, wx.ALIGN_RIGHT), (self.portInput, 0, wx.EXPAND),
            (st_name, 0, wx.ALIGN_RIGHT), (self.accountInput, 0, wx.EXPAND),
            (st_password, 0, wx.ALIGN_RIGHT), (self.passwordInput, 0, wx.EXPAND),
        ])
        hbox_add = wx.BoxSizer(wx.HORIZONTAL)
        hbox_add.Add(flex, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.RIGHT, 180)
        flex.AddGrowableCol(0, 1)
        flex.AddGrowableCol(1, 2)
        vbox.Add(hbox_add, 1, wx.EXPAND | wx.ALL|wx.TOP, 130)
        self.panel.SetSizer(vbox)
        # 为按钮绑定事件
        btn_submit.Bind(wx.EVT_BUTTON, self.saveInfo)
        cancelButton.Bind(wx.EVT_BUTTON, self.CancelButton)
        self.readfile()

    # 读操作
    def readfile(self):
        filename = 'db_connect_info.txt'
        db_list = []
        with open(filename) as file_object:
            for line in file_object:
                db_list.append(line.strip())
        # 连接数据库
        a = db_list
        host = a[0]
        database = a[1]
        port = a[2]
        user = a[3]
        password = a[4]
        # 显示信息
        self.serversInput.SetValue(host)
        self.databaseInput.SetValue(database)
        self.portInput.SetValue(port)
        self.accountInput.SetValue(user)
        self.passwordInput.SetValue(password)

    # 写操作
    def saveInfo(self, event):
        servers = self.serversInput.GetValue().strip()+"\n"
        database = self.databaseInput.GetValue().strip()+"\n"
        port = self.portInput.GetValue().strip()+"\n"
        account = self.accountInput.GetValue().strip()+"\n"
        password = self.passwordInput.GetValue().strip()+"\n"

        filename = 'db_connect_info.txt'
        with open(filename, 'w') as file_object:
            file_object.write(servers)
            file_object.write(database)
            file_object.write(port)
            file_object.write(account)
            file_object.write(password)
        # 连接数据库
        try:
            dbhelper = Sql_operation(self.serversInput.GetValue(), self.databaseInput.GetValue(), self.portInput.GetValue(),
                                          self.accountInput.GetValue(), self.passwordInput.GetValue())
            self.parent.count_page = 1
            self.parent.dbhelper = dbhelper
            dlg = wx.MessageDialog(self, message="设置成功！", caption="温馨提示", style=wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()  # 提示错误
            self.parent.notebook.DeleteAllPages()
            self.parent._mgr.Update()
            self.parent.set_state = 0
        except Exception as e:
            dlg = wx.MessageDialog(self, '设置信息有误，请先进行设置', '温馨提示', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            print("连接数据库失败:", e)

    # 退出界面
    def CancelButton(self, event):
            dlg = wx.MessageDialog(self, '确定要退出吗?', '温馨提示', wx.YES_NO | wx.ICON_INFORMATION)
            retCode = dlg.ShowModal()
            if (retCode == wx.ID_YES):
                self.parent.notebook.DeleteAllPages()
                self.parent._mgr.Update()
                self.parent.set_state = 0
            else:
                pass