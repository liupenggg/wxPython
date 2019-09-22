import wx
import wx.adv
import re


# 登录功能
class LoginInterface(wx.Panel):
    def __init__(self, nb, parent, dbhelper):
        wx.Panel.__init__(self, nb)
        # 需要用到的数据库接口
        self.dbhelper = dbhelper
        # 用来调用父frame,便于更新
        self.parent = parent
        self.panel = self
        # 绑定背景图片
        self.panel.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBack)
        #
        font1 = wx.Font(pointSize=14, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL, underline=False)
        sfz = wx.StaticText(self.panel, -1, '身份证号:', pos=(450, 300))
        mm = wx.StaticText(self.panel, -1, '密    码:', pos=(450, 340))
        sfz.SetFont(font1)
        mm.SetFont(font1)
        #
        self.accountInput = wx.TextCtrl(self.panel, -1, '', pos=(550, 300), size=(200, -1))
        self.passwordInput = wx.TextCtrl(self.panel, -1, '', pos=(550, 340), size=(200, -1), style=wx.TE_PASSWORD)
        self.accountInput.SetFont(font1)
        self.passwordInput.SetFont(font1)
        #
        loginButton = wx.Button(self.panel, -1, '登  录', pos=(500, 390), size=(100, 36), style=wx.BORDER_MASK)
        loginButton.SetFont(font1)

        cancelButton = wx.Button(self.panel, -1, '取  消', pos=(630, 390), size=(100, 36), style=wx.BORDER_MASK)
        cancelButton.SetFont(font1)
        # 为'Button'绑定事件
        loginButton.Bind(wx.EVT_BUTTON, self.LoginButton)
        cancelButton.Bind(wx.EVT_BUTTON, self.CancelButton)

    def OnEraseBack(self, event):
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("image/login.jpg")
        dc.DrawBitmap(bmp, 0, 0)

    # 登录按钮
    def LoginButton(self, event):
        IDCard = 0
        np = self.judeg_user_type(2)
        if self.accountInput.GetValue().strip() and self.passwordInput.GetValue().strip():  # 确保用户名和密码都不为空
            certNo = self.accountInput.GetValue().strip()
            eid = re.search(r"^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{4}$",
                            certNo)  # 身份证号
            if eid == None:
                warn = wx.MessageDialog(self, message="身份证输入不合法", caption="温馨提示",
                                        style=wx.OK | wx.ICON_INFORMATION)
                warn.ShowModal()  # 提示错误
                warn.Destroy()
            else:
                for i in np:
                    if i[0] == self.accountInput.GetValue().strip():
                        IDCard = 1
                if IDCard == 1:
                        pd, user_type = self.judeg_user_type(3)
                        if pd == self.passwordInput.GetValue().strip():
                            if user_type == '管理员':
                                    self.judeg_user_type(0)
                            elif user_type == '用户':
                                    self.judeg_user_type(1)
                        else:
                            warn = wx.MessageDialog(self, message="密码不正确！", caption="温馨提示",
                                                    style=wx.OK | wx.ICON_INFORMATION)
                            warn.ShowModal()  # 提示错误
                            warn.Destroy()
                elif IDCard == 0:
                    warn = wx.MessageDialog(self, message="用户不存在！", caption="温馨提示",
                                            style=wx.OK | wx.ICON_INFORMATION)
                    warn.ShowModal()  # 提示错误
                    warn.Destroy()
        elif self.accountInput.GetValue().strip() == '':
            warn = wx.MessageDialog(self, message="身份证号不能为空！", caption="温馨提示",
                                    style=wx.OK | wx.ICON_INFORMATION)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
        elif self.passwordInput.GetValue().strip() == '':
            certNo = self.accountInput.GetValue().strip()
            eid = re.search(r"^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{4}$",
                            certNo)  # 身份证号
            if eid == None:
                warn = wx.MessageDialog(self, message="身份证输入不合法", caption="温馨提示",
                                        style=wx.OK | wx.ICON_INFORMATION)
                warn.ShowModal()  # 提示错误
                warn.Destroy()
            else:
                warn = wx.MessageDialog(self, message="密码不能为空！", caption="温馨提示",
                                        style=wx.OK | wx.ICON_INFORMATION)
                warn.ShowModal()  # 提示错误
                warn.Destroy()

    def judeg_user_type(self, user_type):
        sql_1 = "select IDCard from user_info"
        sql_2 = "select Password,user_Category.CategoryName from user_info \
                    INNER JOIN user_category ON user_info.UserCategory=user_category.id where IDCard=%s"
        sql = "select user_state.StateName,TrueName from user_info\
                    INNER JOIN user_state ON user_info.UserStatus=user_state.id where IDCard=%s  "
        # 判断管理员登录
        if user_type == 0:
            try:
                param = (self.accountInput.GetValue(),)
                result = self.dbhelper.SelectRecord(sql, param)
                self.parent.Userfun(result[0][0], result[0][1], self.accountInput.GetValue(), '管理员')
            except Exception as e:
                print("查询记录失败:", e)
        # 判断用户登录
        elif user_type == 1:
            try:
                param = (self.accountInput.GetValue(),)
                result = self.dbhelper.SelectRecord(sql, param)
                self.parent.Userfun(result[0][0], result[0][1], self.accountInput.GetValue(), '用户')
            except Exception as e:
                print("查询记录失败:", e)
        # 验证身份证号
        elif user_type == 2:
            try:
                param = ()
                result = self.dbhelper.SelectRecord(sql_1, param)
                return result
            except Exception as e:
                print("查询记录失败:", e)
        # 验证密码和用户类别
        elif user_type == 3:
            try:
                param = (self.accountInput.GetValue(),)
                result = self.dbhelper.SelectRecord(sql_2, param)
                return result[0][0], result[0][1]
            except Exception as e:
                print("查询记录失败:", e)

    # 退出界面
    def CancelButton(self, event):
        dlg = wx.MessageDialog(self, '确定要退出吗?', '温馨提示', wx.YES_NO | wx.ICON_INFORMATION)
        retCode = dlg.ShowModal()
        if (retCode == wx.ID_YES):
            self.parent.notebook.DeleteAllPages()
            self.parent._mgr.Update()
            self.parent.login_state = 0
        else:
            pass
