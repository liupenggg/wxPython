import wx
import wx.lib.agw.aui as aui

# 导入数据库
from db_operation import Sql_operation
# 导入专利信息管理界面
from admin_patent_info_page import AdminPatent
# 导入用户信息管理界面
from admin_user_info_page import AdminApplicant
# 导入用户专利信息界面
from user_patent_info_page import OneManPatent
# 导入查询专利信息界面
from user_query_patent_info_page import UserQueryPatent
# 导入用户基本信息界面
from user_info_page import User_info
# 导入登录界面
from login_page import LoginInterface
# 导入注册界面
from register_page import RegisterInterface
# 导入系统说明界面
from help_page import Set_page, About


class mainFrame(wx.Frame):
    '''程序主窗口类，继承自wx.Frame'''

    def __init__(self, parent, title):
        '''构造函数'''
        # self=Frame父类框，parent=None
        wx.Frame.__init__(self, parent, -1, title, style=wx.MAXIMIZE | wx.DEFAULT_FRAME_STYLE)
        # 设置背景为白色
        self.SetBackgroundColour("#FFFFFF")
        self.count_page = 0
        # 设置页面开启关闭状态
        self.login_state = 0  # 登录界面
        self.register_state = 0  # 注册界面
        self.set_state = 0  # 设置界面
        self.about_state = 0  # 关于界面
        self.fun_state = 0  # 功能界面
        #  数据库连接状态
        self.dbhelper = None
        self.connect_state = 0
        # 设置面板
        p_top = wx.Panel(self, -1)  # 标题
        p_left = wx.Panel(self, -1)  # 操作界面
        #  设置字体
        self.font1 = wx.Font(pointSize=14, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL, underline=False)
        self.font2 = wx.Font(pointSize=13, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL, underline=False)
        # 设置多标签页面
        self.p_center0 = wx.Panel(self, -1)
        self.notebook = wx.Notebook(self.p_center0, -1)
        # 设置多标签页面
        self.p_center1 = wx.Panel(self, -1)
        self.nb = wx.Notebook(self.p_center1, -1)
        #
        self.notebook.SetFont(self.font2)
        self.nb.SetFont(self.font2)
        # 创建操作按钮
        login_button = wx.Button(p_left, label="登  录", pos=(50, 100), size=(100, 40))
        register_button = wx.Button(p_left, label="注  册", pos=(50, 200), size=(100, 40))
        set_button = wx.Button(p_left, label="设  置", pos=(50, 300), size=(100, 40))
        about_button = wx.Button(p_left, label="关  于", pos=(50, 400), size=(100, 40))
        quit_button = wx.Button(p_left, label="退  出", pos=(50, 500), size=(100, 40))
        #
        login_button.SetFont(self.font1)
        register_button.SetFont(self.font1)
        set_button.SetFont(self.font1)
        about_button.SetFont(self.font1)
        quit_button.SetFont(self.font1)
        # 绑定事件处理
        register_button.Bind(wx.EVT_BUTTON, self.register)  # 注册
        login_button.Bind(wx.EVT_BUTTON, self.login)  # 登录
        set_button.Bind(wx.EVT_BUTTON, self.set_page)  # 设置
        about_button.Bind(wx.EVT_BUTTON, self.about)  # 关于
        quit_button.Bind(wx.EVT_BUTTON, self.OnExit)  # 退出
        # 创建logo静态文本，设置字体属性和图片
        bmp = wx.Image("image/logo.jpg", wx.BITMAP_TYPE_JPEG)
        wx.StaticBitmap(p_top, -1, bitmap=bmp.ConvertToBitmap())
        logo = wx.StaticText(p_top, label="专 利 管 理 系 统", pos=(500, 20))
        # 设置字体
        font = wx.Font(pointSize=35, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.BOLD, underline=False)
        logo.SetFont(font)
        #
        self._mgr = aui.AuiManager()  # 创建一个布局管理器
        self._mgr.SetManagedWindow(self)  # 告诉主窗口由mgr来管理界面
        # 添加界面上的各个区域
        self._mgr.AddPane(p_top,
                          aui.AuiPaneInfo().Name("topPanel").Top().MinSize((0, 80)).Caption(u"标题栏").CaptionVisible
                          (False).Resizable(False))
        self._mgr.AddPane(p_left,
                          aui.AuiPaneInfo().Name("LeftPanel").Left().MinSize((200, -1)).Caption(u"操作区").CaptionVisible
                          (False).MinimizeButton(False).MaximizeButton(False).CloseButton(False).Resizable(False))
        self._mgr.AddPane(self.p_center0,
                          aui.AuiPaneInfo().Name("CenterPanel0").CenterPane().Hide()
                          )
        self._mgr.AddPane(self.p_center1,
                          aui.AuiPaneInfo().Name("CenterPanel1").CenterPane().Hide()
                          )

        # 更新界面显示
        self._mgr.Update()

    # 读操作
    def readfile(self):
        filename = 'db_connect_info.txt'
        db_list = []
        dbhelper = None
        dbstate = 0
        with open(filename) as file_object:
            for line in file_object:
                db_list.append(line.strip())
        #  连接数据库
        try:
            dbhelper = Sql_operation(db_list[0], db_list[1], db_list[2], db_list[3], db_list[4])
            dbstate = dbhelper.connect_success
            return dbhelper, dbstate
        except Exception as e:
            dlg = wx.MessageDialog(self, '设置信息有误，请先进行设置', '温馨提示', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            print("连接数据库失败:", e)
            return dbhelper, dbstate

    # 登录
    def login(self, event):
        '''登录窗口'''
        if self.login_state == 0 and self.register_state == 0 and self.set_state == 0 and self.about_state == 0 \
                and self.fun_state == 0:
            if self.count_page == 0:
                self.dbhelper, self.connect_state = self.readfile()
                if self.connect_state == 1:
                    self.login_page = LoginInterface(self.notebook, self, self.dbhelper)
                    self.notebook.AddPage(self.login_page, "登录界面", select=True)
                    sizer = wx.BoxSizer()
                    sizer.Add(self.notebook, 1, wx.EXPAND)
                    self.p_center0.SetSizer(sizer)
                    p0 = self._mgr.GetPane('CenterPanel0')
                    p0.Show(True)
                    self.login_state = 1  # 从关闭变为开启
                    #
                    p1 = self._mgr.GetPane('CenterPanel1')
                    p1.Show(False)
                    self.count_page = 1
            elif self.count_page == 1:
                self.login_page = LoginInterface(self.notebook, self, self.dbhelper)
                self.notebook.AddPage(self.login_page, "登录界面", select=True)
                sizer = wx.BoxSizer()
                sizer.Add(self.notebook, 1, wx.EXPAND)
                self.p_center0.SetSizer(sizer)
                p0 = self._mgr.GetPane('CenterPanel0')
                p0.Show(True)
                self.login_state = 1  # 从关闭变为开启
                #
                p1 = self._mgr.GetPane('CenterPanel1')
                p1.Show(False)
                self.count_page = 1
        elif self.register_state == 1:  # 如果注册窗口打开
            dlg = wx.MessageDialog(self, '请先关闭注册窗口', '温馨提示', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
        elif self.set_state == 1:  # 如果设置窗口已打开
            dlg = wx.MessageDialog(self, '请先关闭设置窗口', '温馨提示', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
        elif self.about_state == 1:  # 如果关于窗口已打开
            dlg = wx.MessageDialog(self, '请先关闭关于窗口', '温馨提示', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
        elif self.fun_state == 1:  # 如果功能窗口已打开
            dlg = wx.MessageDialog(self, '请先关闭所有窗口', '温馨提示', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
        elif self.login_state == 1:
            warn = wx.MessageDialog(self, message="登录界面已打开", caption="温馨提示", style=wx.OK | wx.ICON_INFORMATION)
            warn.ShowModal()  # 提示错误
            warn.Destroy()

        self._mgr.Update()

    # 注册
    def register(self, event):
        '''注册窗口'''
        if self.register_state == 0 and self.login_state == 0 and self.set_state == 0 and self.about_state == 0 \
                and self.fun_state == 0:
            if self.count_page == 0:
                self.dbhelper, self.connect_state = self.readfile()
                if self.connect_state == 1:
                    self.register = RegisterInterface(self.notebook, self, self.dbhelper)
                    self.notebook.AddPage(self.register, "注册界面", select=True)
                    sizer = wx.BoxSizer()
                    sizer.Add(self.notebook, 1, wx.EXPAND)
                    self.p_center0.SetSizer(sizer)
                    p0 = self._mgr.GetPane('CenterPanel0')
                    p0.Show(True)
                    self.register_state = 1
                    #
                    p1 = self._mgr.GetPane('CenterPanel1')
                    p1.Show(False)
                    self.count_page = 1
            elif self.count_page == 1:
                self.register = RegisterInterface(self.notebook, self, self.dbhelper)
                self.notebook.AddPage(self.register, "注册界面", select=True)
                sizer = wx.BoxSizer()
                sizer.Add(self.notebook, 1, wx.EXPAND)
                self.p_center0.SetSizer(sizer)
                p0 = self._mgr.GetPane('CenterPanel0')
                p0.Show(True)
                self.register_state = 1
                #
                p1 = self._mgr.GetPane('CenterPanel1')
                p1.Show(False)
                self.count_page = 1
        elif self.login_state == 1:  # 如果登录窗口已打开
            dlg = wx.MessageDialog(self, '请先关闭登录窗口', '温馨提示', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
        elif self.set_state == 1:  # 如果设置窗口已打开
            dlg = wx.MessageDialog(self, '请先关闭设置窗口', '温馨提示', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
        elif self.about_state == 1:  # 如果关于窗口已打开
            dlg = wx.MessageDialog(self, '请先关闭关于窗口', '温馨提示', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
        elif self.fun_state == 1:  # 如果功能窗口已打开
            dlg = wx.MessageDialog(self, '请先关闭所有窗口', '温馨提示', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
        elif self.register_state == 1:
            warn = wx.MessageDialog(self, message="注册界面已打开", caption="温馨提示", style=wx.OK | wx.ICON_INFORMATION)
            warn.ShowModal()  # 提示错误
            warn.Destroy()

        self._mgr.Update()

    # 设置
    def set_page(self, evt):
        if self.register_state == 0 and self.login_state == 0 and self.set_state == 0 and self.about_state == 0 \
                and self.fun_state == 0:
            self.Set_page = Set_page(self.notebook, self)
            self.notebook.AddPage(self.Set_page, "设置", select=True)
            sizer = wx.BoxSizer()
            sizer.Add(self.notebook, 1, wx.EXPAND)
            self.p_center0.SetSizer(sizer)
            p0 = self._mgr.GetPane('CenterPanel0')
            p0.Show(True)
            self.set_state = 1  # 设置界面
            #
            p1 = self._mgr.GetPane('CenterPanel1')
            p1.Show(False)
        elif self.login_state == 1:  # 如果登录窗口已打开
            dlg = wx.MessageDialog(self, '请先关闭登录窗口', '温馨提示', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
        elif self.register_state == 1:  # 如果注册窗口已打开
            dlg = wx.MessageDialog(self, '请先关闭注册窗口', '温馨提示', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
        elif self.about_state == 1:  # 如果关于窗口已打开
            dlg = wx.MessageDialog(self, '请先关闭关于窗口', '温馨提示', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
        elif self.fun_state == 1:  # 如果功能窗口已打开
            dlg = wx.MessageDialog(self, '请先关闭所有窗口', '温馨提示', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
        elif self.set_state == 1:
            warn = wx.MessageDialog(self, message="设置界面已打开", caption="温馨提示", style=wx.OK | wx.ICON_INFORMATION)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
        self._mgr.Update()

    # 关于
    def about(self, evt):
        if self.register_state == 0 and self.login_state == 0 and self.set_state == 0 and self.about_state == 0 \
                and self.fun_state == 0:
            self.About_page = About(self.notebook, self)
            self.notebook.AddPage(self.About_page, "关于", select=True)
            sizer = wx.BoxSizer()
            sizer.Add(self.notebook, 1, wx.EXPAND)
            self.p_center0.SetSizer(sizer)
            p0 = self._mgr.GetPane('CenterPanel0')
            p0.Show(True)
            self.about_state = 1  # 关于界面
            #
            p1 = self._mgr.GetPane('CenterPanel1')
            p1.Show(False)
        elif self.login_state == 1:  # 如果登录窗口已打开
            dlg = wx.MessageDialog(self, '请先关闭登录窗口', '温馨提示', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
        elif self.register_state == 1:  # 如果注册窗口已打开
            dlg = wx.MessageDialog(self, '请先关闭注册窗口', '温馨提示', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
        elif self.set_state == 1:  # 如果设置窗口已打开
            dlg = wx.MessageDialog(self, '请先关闭设置窗口', '温馨提示', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
        elif self.fun_state == 1:  # 如果功能窗口已打开
            dlg = wx.MessageDialog(self, '请先关闭所有窗口', '温馨提示', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
        elif self.about_state == 1:
            warn = wx.MessageDialog(self, message="关于界面已打开", caption="温馨提示", style=wx.OK | wx.ICON_INFORMATION)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
        self._mgr.Update()

    # 功能菜单
    def Userfun(self, user_state, true_name, eID, user_type):
        '''登录窗口'''
        # 登陆成功后关闭登录界面
        p0 = self._mgr.GetPane('CenterPanel0')
        p0.Show(False)
        self.notebook.DeleteAllPages()
        #
        if user_type == '用户':
            self.patentInfo = OneManPatent(self.nb, self, user_state, true_name, eID, self.dbhelper)
            self.Query = UserQueryPatent(self.nb, self, self.dbhelper)
            self.userInfo = User_info(self.nb, self, eID, self.dbhelper)
            #
            self.nb.AddPage(self.patentInfo, "用户专利信息")
            self.nb.AddPage(self.Query, "专利查询")
            self.nb.AddPage(self.userInfo, "用户基本信息")
            #
            sizer = wx.BoxSizer()
            sizer.Add(self.nb, 1, wx.EXPAND)
            self.p_center1.SetSizer(sizer)
            self.fun_state = 1  # 开启状态
            self.login_state = 0  # 登录界面关闭状态
            self.user_Info_page = 1
            self.user_Patent_page = 1
            self.user_query_page = 1
        elif user_type == '管理员':
            #
            self.managePatent = AdminPatent(self.nb, self, self.dbhelper)
            self.manageUser = AdminApplicant(self.nb, self, self.dbhelper)
            #
            self.nb.AddPage(self.managePatent, "专利信息管理")
            self.nb.AddPage(self.manageUser, "用户信息管理")
            #
            sizer = wx.BoxSizer()
            sizer.Add(self.nb, 1, wx.EXPAND)
            self.p_center1.SetSizer(sizer)
            self.fun_state = 1  # 开启状态
            self.login_state = 0  # 重置登录界面状态
            self.admin_user_page = 1
            self.admin_patent_page = 1
        #
        p1 = self._mgr.GetPane('CenterPanel1')
        p1.Show(True)

        self._mgr.Update()

    # 退出
    def OnExit(self, evt):
        dlg = wx.MessageDialog(self, '确定要退出系统吗?', '温馨提示', wx.YES_NO | wx.ICON_INFORMATION)
        retCode = dlg.ShowModal()
        if (retCode == wx.ID_YES):
            self.Show(False)
        else:
            pass


class mainApp(wx.App):
    def OnInit(self):
        Frame = mainFrame(None, '')
        Frame.Show()
        return True


if __name__ == "__main__":
    app = mainApp()
    app.MainLoop()
