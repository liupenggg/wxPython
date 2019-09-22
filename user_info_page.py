import wx
import wx.adv
import time
import re
#
from user import UserInfo


# 用户基本信息界面
class User_info(wx.Panel):
    def __init__(self, notebook, parent, eid, dbhelper):

        wx.Panel.__init__(self, notebook)
        # 需要用到的数据库接口
        self.dbhelper = dbhelper
        # 用来调用父frame,便于更新
        self.parent = parent
        self.panel = self
        #
        self.eID = eid  # 身份证号
        self.gender = '男'  # 默认性别男
        # 最外层布局
        vbox = wx.BoxSizer(wx.VERTICAL)
        # 控件
        st_title = wx.StaticText(self.panel, -1, label=u'用户信息')  # 标题
        font = st_title.GetFont()
        font.PointSize = font.PointSize + 8
        font = font.Bold()
        st_title.SetFont(font)
        #
        st_Name = wx.StaticText(self.panel, -1, label="姓名")
        st_password = wx.StaticText(self.panel, -1, label="* 密码")
        st_confirmpd = wx.StaticText(self.panel, -1, label="* 确认密码")
        st_certNo = wx.StaticText(self.panel, -1, label=u'身份证号')
        st_sex = wx.StaticText(self.panel, -1, label=u'性别')
        st_birth = wx.StaticText(self.panel, -1, label=u'出生日期')
        st_job = wx.StaticText(self.panel, -1, label=u'职业')
        st_school = wx.StaticText(self.panel, -1, label=u'毕业学校')
        st_degree = wx.StaticText(self.panel, -1, label=u'学历/学位')
        st_danwei = wx.StaticText(self.panel, -1, label=u'单位')
        st_zhicheng = wx.StaticText(self.panel, -1, label=u'职称')
        st_phone = wx.StaticText(self.panel, -1, label=u'联系电话')
        st_QQ = wx.StaticText(self.panel, -1, label=u'QQ')
        st_email = wx.StaticText(self.panel, -1, label=u'电子邮箱')
        #
        tc_Name = wx.TextCtrl(self.panel, -1)  # 姓名
        tc_password = wx.TextCtrl(self.panel, -1)  # 密码
        tc_confirmpd = wx.TextCtrl(self.panel, -1)  # 确认密码
        tc_certNo = wx.TextCtrl(self.panel, -1)  # 身份证号
        tc_certNo.SetEditable(False)
        # 性别
        rb_sex1 = wx.RadioButton(self.panel, -1, label=u'男')
        rb_sex2 = wx.RadioButton(self.panel, -1, label=u'女')
        # 出生日期
        dt_birth = wx.adv.DatePickerCtrl(self.panel, -1,
                                         style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY | wx.adv.DP_ALLOWNONE)
        #
        tc_job = wx.ComboBox(self.panel, -1, choices=self.data_translate((), 1), style=wx.CB_READONLY)  # 职业
        tc_school = wx.ComboBox(self.panel, -1, choices=self.data_translate((), 2), style=wx.CB_READONLY)  # 毕业学校
        cb_degreeType = wx.ComboBox(self.panel, -1, choices=self.data_translate((), 3), style=wx.CB_READONLY)
        tc_danwei = wx.ComboBox(self.panel, -1, choices=self.data_translate((), 4), style=wx.CB_READONLY)  # 单位
        #
        tc_zhicheng = wx.TextCtrl(self.panel, -1)  # 职称
        tc_phone = wx.TextCtrl(self.panel, -1)  # 联系电话
        tc_QQ = wx.TextCtrl(self.panel, -1)  # QQ
        tc_email = wx.TextCtrl(self.panel, -1)  # 电子邮箱

        #
        self.password = tc_password
        self.confirmpd = tc_confirmpd
        self.XingMing = tc_Name
        self.certNo = tc_certNo
        self.sex1 = rb_sex1
        self.sex2 = rb_sex2
        self.birth = dt_birth
        self.job = tc_job
        self.school = tc_school
        self.degreeType = cb_degreeType
        self.danwei = tc_danwei
        self.zhicheng = tc_zhicheng
        self.phone = tc_phone
        self.QQ = tc_QQ
        self.email = tc_email
        #
        font1 = wx.Font(pointSize=14, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL, underline=False)
        btn_submit = wx.Button(self.panel, -1, label=u'提  交', pos=(400, 555), size=(100, 35), style=wx.BORDER_MASK)
        btn_reset = wx.Button(self.panel, -1, label=u'重  置', pos=(550, 555), size=(100, 35), style=wx.BORDER_MASK)
        btn_exit = wx.Button(self.panel, -1, label=u'退  出', pos=(1000, 555), size=(100, 35), style=wx.BORDER_MASK)
        btn_submit.SetFont(font1)
        btn_reset.SetFont(font1)
        btn_exit.SetFont(font1)
        # 性别布局
        hsex = wx.GridSizer(1, 2, 0, 0)
        hsex.Add(rb_sex1)
        hsex.Add(rb_sex2)

        # 信息布局
        flex = wx.FlexGridSizer(14, 2, 10, 10)
        flex.AddMany([
            (st_Name, 0, wx.ALIGN_RIGHT), (tc_Name, 0, wx.EXPAND),
            (st_certNo, 0, wx.ALIGN_RIGHT), (tc_certNo, 0, wx.EXPAND),
            (st_password, 0, wx.ALIGN_RIGHT), (tc_password, 0, wx.EXPAND),
            (st_confirmpd, 0, wx.ALIGN_RIGHT), (tc_confirmpd, 0, wx.EXPAND),
            (st_sex, 0, wx.ALIGN_RIGHT), (hsex, wx.EXPAND),
            (st_birth, 0, wx.ALIGN_RIGHT), (dt_birth, 0, wx.EXPAND),
            (st_job, 0, wx.ALIGN_RIGHT), (tc_job, 0, wx.EXPAND),
            (st_school, 0, wx.ALIGN_RIGHT), (tc_school, 0, wx.EXPAND),
            (st_degree, 0, wx.ALIGN_RIGHT), (cb_degreeType, 0, wx.EXPAND),
            (st_danwei, 0, wx.ALIGN_RIGHT), (tc_danwei, 0, wx.EXPAND),
            (st_zhicheng, 0, wx.ALIGN_RIGHT), (tc_zhicheng, 0, wx.EXPAND),
            (st_phone, 0, wx.ALIGN_RIGHT), (tc_phone, 0, wx.EXPAND),
            (st_QQ, 0, wx.ALIGN_RIGHT), (tc_QQ, 0, wx.EXPAND),
            (st_email, 0, wx.ALIGN_RIGHT), (tc_email, 0, wx.EXPAND)
        ])
        hbox_add = wx.BoxSizer(wx.HORIZONTAL)
        hbox_add.Add(flex, 1, wx.EXPAND | wx.RIGHT, 350)

        flex.AddGrowableCol(0, 1)
        flex.AddGrowableCol(1, 2)
        vbox.Add(st_title, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        vbox.Add(hbox_add, 1, wx.EXPAND | wx.ALL, 10)
        self.panel.SetSizer(vbox)
        # 绑定单击事件
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadiogroup)
        self.Bind(wx.EVT_BUTTON, self.saveUpdate, btn_submit)
        self.Bind(wx.EVT_BUTTON, self.Reset_Button, btn_reset)
        self.Bind(wx.EVT_BUTTON, self.CancelButton, btn_exit)
        #
        self.showAllText()  # 展现所有的text原来取值

    def showAllText(self):
        '''显示用户信息'''
        data = self.getPersonalInfo(self.eID)  # 通过身份证号获取申请人信息
        self.password.SetValue(data[0])  # 设置登录密码
        self.confirmpd.SetValue(data[0])
        self.XingMing.SetValue(str(data[1]))  # 设置姓名
        self.certNo.SetValue(str(data[2]))  # 设置身份证号
        if data[3] == '男':
            self.sex1.SetValue(True)  # 将单选按钮设置为选中或取消选中状态。
        else:
            self.sex2.SetValue(True)  # 设置性别2
        # 处理时间
        a = str(data[4])
        year = a[:4]
        month = a[5:7]
        day = a[8:10]
        othertime = wx.DateTime(day=int(day), month=int(month) - 1, year=int(year), hour=0, minute=0, second=0,
                                millisec=0)
        self.birth.SetValue(othertime)  # 设置出生日期
        self.job.SetValue(str(data[5]))  # 设置职业
        self.school.SetValue(str(data[6]))  # 设置毕业学校
        self.degreeType.SetValue(str(data[7]))  # 设置学历/学位类别
        self.danwei.SetValue(str(data[8]))  # 设置单位
        self.zhicheng.SetValue(str(data[9]))  # 设置职称
        self.phone.SetValue(str(data[10]))  # 设置手机号
        self.QQ.SetValue(str(data[11]))  # 设置QQ
        self.email.SetValue(str(data[12]))  # 设置电子邮箱

    # 修改申请人信息并保存
    def saveUpdate(self, evt):
        judge = 1
        '''保存修改后的信息'''
        password = self.password.GetValue().strip()  # 获得修改后的值
        confirmpd = self.confirmpd.GetValue().strip()
        name = self.XingMing.GetValue().strip()
        certNo = self.certNo.GetValue().strip()
        gender = self.gender
        #
        birthday = self.birth.GetValue()
        birthday_time = self.datetime_to_str(str(birthday))
        #
        job = self.data_translate(self.job.GetValue(), 1)  # 职业
        graduschool = self.data_translate(self.school.GetValue(), 2)
        degree = self.data_translate(self.degreeType.GetValue(), 3)
        danwei = self.data_translate(self.danwei.GetValue(), 4)
        #
        zhicheng = self.zhicheng.GetValue()
        shoujihao = self.phone.GetValue().strip()
        qq = self.QQ.GetValue().strip()
        email = self.email.GetValue().strip()
        # 判断注册时输入的格式是否正确
        password_test = re.search(r"^[a-zA-Z0-9]{4,10}$", password)  # 密码
        true_name = re.search(r"^[\u4E00-\u9FA5]{2,4}$", name)  # 姓名
        shenfenzheng = re.search(r"^(\d{6})(\d{4})(\d{2})(\d{2})(\d{3})([0-9]|X)$", certNo)  # 身份证号
        if name == "":
            warn = wx.MessageDialog(self, message="姓名不能为空！！！", caption="温馨提示", style=wx.OK | wx.ICON_INFORMATION)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            judge = 0
        elif true_name == None:
            # 消息对话框
            warn = wx.MessageDialog(self, message="真实姓名填写有误", caption="温馨提示",
                                    style=wx.OK | wx.ICON_INFORMATION)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            judge = 0
        elif certNo == "":
            warn = wx.MessageDialog(self, message="身份证号不能为空！！！", caption="温馨提示", style=wx.OK | wx.ICON_INFORMATION)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            judge = 0
        elif shenfenzheng == None:
            # 消息对话框
            warn = wx.MessageDialog(self, message="身份证输入不合法", caption="温馨提示",
                                    style=wx.OK | wx.ICON_INFORMATION)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            judge = 0
        elif password == "":
            # 消息对话框
            warn = wx.MessageDialog(self, message="登录密码不能为空！！！", caption="温馨提示", style=wx.OK | wx.ICON_INFORMATION)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            judge = 0
        elif password_test == None:
            # 消息对话框
            warn = wx.MessageDialog(self, message="密码不能含有非法字符，长度在4-10之间", caption="温馨提示",
                                    style=wx.OK | wx.ICON_INFORMATION)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            judge = 0
        elif confirmpd == "":
            # 消息对话框
            warn = wx.MessageDialog(self, message="确认密码不能为空！！！", caption="温馨提示", style=wx.OK | wx.ICON_INFORMATION)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            judge = 0
        elif password != confirmpd:
            # 消息对话框
            warn = wx.MessageDialog(self, message="两次密码不同，请重新输入", caption="温馨提示",
                                    style=wx.OK | wx.ICON_INFORMATION)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            judge = 0
        if shoujihao != '':
            phone = re.search(r"^1[3-9]\d{9}$", shoujihao)  # 验证手机号
            if phone == None:
                warn = wx.MessageDialog(self, message="手机号码不正确，请重新输入", caption="温馨提示",
                                        style=wx.OK | wx.ICON_INFORMATION)
                warn.ShowModal()  # 提示错误
                warn.Destroy()
                judge = 0
        if qq != '':
            QQ = re.search(r"^[1-9][0-9]{4,11}$", qq)  # 验证QQ号
            if QQ == None:
                warn = wx.MessageDialog(self, message="QQ号不正确，例如843278021", caption="温馨提示",
                                        style=wx.OK | wx.ICON_INFORMATION)
                warn.ShowModal()  # 提示错误
                warn.Destroy()
                judge = 0
        if email != '':
            email_test = re.search(r"^\w+@\w+(\.[a-zA-Z]{2,3}){1,2}$", email)  # 验证邮箱
            if email_test == None:
                warn = wx.MessageDialog(self, message="Email格式不正确，例如6666@qq.com", caption="温馨提示",
                                        style=wx.OK | wx.ICON_INFORMATION)
                warn.ShowModal()  # 提示错误
                warn.Destroy()
                judge = 0
        if password != "" and name != "" and certNo != "" and judge == 1:
            print("开始将修改后的数据保存到数据库中")
            applicant = UserInfo('', password, name, certNo, gender, birthday_time, job[0][0], graduschool[0][0],
                                 degree[0][0],
                                 danwei[0][0], zhicheng, shoujihao, qq, email)
            try:
                param_2 = (applicant.getpassword(), applicant.getApplicantName(), applicant.getApplicantID(),
                           applicant.getgender(), applicant.getbirthday(),
                           applicant.getprofession(), applicant.getgraduationschool(), applicant.getdegree(),
                           applicant.getdepartment(), applicant.getzhicheng(),
                           applicant.getCellPhoneNumber(),
                           applicant.getQQ(), applicant.getzhicheng(), applicant.getemail(),
                           applicant.getApplicantID())
                sql_2 = "update user_info set Password=%s, TrueName=%s, IDCard=%s, Gender=%s, Birthday=%s, " \
                        "Job=%s,School=%s, Degree=%s, Unit=%s, Title=%s, Phone=%s , QQ=%s, Title=%s, Email=%s" \
                        " where IDCard=%s"
                self.dbhelper.UpdateData(sql_2, param_2)
                # 对话框
                warn = wx.MessageDialog(self, message="提交成功", caption="温馨提示",
                                        style=wx.OK | wx.ICON_INFORMATION)
                warn.ShowModal()  # 提示
                warn.Destroy()
            except Exception as e:
                print("查询记录失败:", e)

    # 重置按钮
    def Reset_Button(self, evt):
        self.password.Clear()
        self.XingMing.Clear()
        self.certNo.Clear()
        self.sex1.SetValue(False)
        self.sex2.SetValue(False)
        self.birth.SetValue(wx.DateTime.Now())
        self.job.SetValue('未填写')
        self.school.SetValue('未填写')
        self.degreeType.SetValue('未填写')
        self.danwei.SetValue('未填写')
        self.zhicheng.Clear()
        self.phone.Clear()
        self.QQ.Clear()
        self.email.Clear()

    # 把字符串转换为数字，这个地方要写活，用数据库语句
    def data_translate(self, data, i):
        param = (data,)
        data_list = []
        sql = ""
        sql_1 = ""
        if i == 1:
            sql = "select id from job  where JobName=%s"
            sql_1 = "select JobName from job"
        elif i == 2:
            sql = "select id from school  where SchoolName=%s"
            sql_1 = "select SchoolName from school"
        elif i == 3:
            sql = "select id from degree  where DegreeName=%s"
            sql_1 = "select DegreeName from degree"
        elif i == 4:
            sql = "select id from unit  where UnitName=%s"
            sql_1 = "select UnitName from unit"
        elif i == 5:
            sql = "select id from user_state  where StateName=%s"
            sql_1 = "select StateName from user_state"
        elif i == 6:
            sql = "select id from user_category  where CategoryName=%s"
            sql_1 = "select CategoryName from user_category"
        try:
            if param[0] == ():
                param = ()
                net = self.dbhelper.SelectRecord(sql_1, param)

                for j in net:
                    data_list.append(j[0])
                return data_list
            else:
                net = self.dbhelper.SelectRecord(sql, param)
                return net
        except Exception as e:
            print("查询记录失败:", e)

    # 用户登录后，查看基本信息时使用，已完成修改
    def getPersonalInfo(self, eID):
        sql = "select Password,TrueName,IDCard,Gender,Birthday,job.JobName,school.SchoolName,degree.DegreeName,unit.UnitName,\
                          Title,Phone,QQ, Email \
                           from user_info \
                                INNER JOIN job ON user_info.Job=job.id\
                                INNER JOIN school ON user_info.School=school.id \
                                INNER JOIN degree ON user_info.Degree=degree.id \
                                INNER JOIN unit ON user_info.Unit=unit.id \
                                where IDCard=%s"
        try:
            param = (eID,)
            datas = self.dbhelper.SelectRecord(sql, param)  # 执行并返回找到的行数
            return datas[0]
        except Exception as e:
            print("SQL执行错误，原因：", e)

    # 单选按钮操作
    def OnRadiogroup(self, evt):
        rb = evt.GetEventObject()
        self.gender = rb.GetLabel()

    # 时间格式转换
    def datetime_to_str(self, dateTime):
        # Python time strptime() 函数根据指定的格式把一个时间字符串解析为时间元组。
        tempTime = time.strptime(dateTime, '%a %b %d %H:%M:%S %Y')
        # Python time strftime() 函数接收以时间元组，并返回以可读字符串表示的当地时间，格式由参数format决定。
        resTime = time.strftime('%Y-%m-%d', tempTime)
        return resTime

    # 退出界面
    def CancelButton(self, evt):
        dlg = wx.MessageDialog(self, '确定要退出界面吗?', '温馨提示', wx.YES_NO | wx.ICON_INFORMATION)
        retCode = dlg.ShowModal()
        if (retCode == wx.ID_YES):
            self.parent.nb.DeleteAllPages()
            p1 = self.parent._mgr.GetPane('CenterPanel1')
            p1.Show(False)
            self.parent._mgr.Update()
            self.parent.fun_state = 0
        else:
            pass
