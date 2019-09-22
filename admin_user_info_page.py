import wx
import wx.adv
from user import UserInfo


# 初始化审核申请人信息界面
class CheckApplicantFrame(wx.Frame):
    def __init__(self, parent, title, select_id, dbhelper):
        # 用来调用父窗口,便于更新
        self.mainframe = parent
        # 生成一个500*500的窗口
        wx.Frame.__init__(self, parent, title=title, size=(600, 700),
                          style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX))
        # 需要用到的数据库接口
        self.dbhelper = dbhelper
        # 设置窗口屏幕居中
        self.Center()
        # 设置面板大小
        self.panel = wx.Panel(self, size=(600, 700))
        font1 = wx.Font(pointSize=14, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL, underline=False)
        self.panel.SetFont(font1)
        # 设置面板背景为白色
        self.panel.SetBackgroundColour("#FFFFFF")
        # 最外层布局
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        # 设置水平布局
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        flex = wx.FlexGridSizer(14, 2, 10, 10)
        #
        st_password = wx.StaticText(self.panel, label="登录密码")
        st_Name = wx.StaticText(self.panel, label="姓名")
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
        st_checkstate = wx.StaticText(self.panel, -1, label=u'审核状态')

        #
        tc_password = wx.TextCtrl(self.panel, -1)  # 登录密码
        tc_Name = wx.TextCtrl(self.panel, -1)  # 姓名
        tc_certNo = wx.TextCtrl(self.panel, -1)  # 身份证号
        tc_gender = wx.TextCtrl(self.panel, -1)  # 性别
        tc_birth = wx.TextCtrl(self.panel, -1)  # 出生日期
        tc_job = wx.TextCtrl(self.panel, -1)  # 职业
        tc_school = wx.TextCtrl(self.panel, -1)  # 毕业学校
        # 学历/学位
        tc_degreeType = wx.TextCtrl(self.panel, -1)
        tc_danwei = wx.TextCtrl(self.panel, -1)  # 单位
        tc_zhicheng = wx.TextCtrl(self.panel, -1)  # 职称
        tc_phone = wx.TextCtrl(self.panel, -1)  # 联系电话
        tc_QQ = wx.TextCtrl(self.panel, -1)  # QQ
        tc_email = wx.TextCtrl(self.panel, -1)  # 电子邮箱
        tc_checkstate = wx.ComboBox(self.panel, -1, choices=[u'待审核', u'审核通过', u'审核未通过'])
        #
        tc_password.SetEditable(False)
        tc_Name.SetEditable(False)
        tc_certNo.SetEditable(False)
        tc_gender.SetEditable(False)  # 性别
        tc_birth.SetEditable(False)  # 出生日期
        tc_job.SetEditable(False)
        tc_school.SetEditable(False)
        tc_degreeType.SetEditable(False)
        tc_danwei.SetEditable(False)
        tc_zhicheng.SetEditable(False)
        tc_phone.SetEditable(False)
        tc_QQ.SetEditable(False)
        tc_email.SetEditable(False)
        #
        self.password = tc_password
        self.XingMing = tc_Name
        self.certNo = tc_certNo
        self.gender = tc_gender
        self.birth = tc_birth
        self.job = tc_job
        self.school = tc_school
        self.degreeType = tc_degreeType
        self.danwei = tc_danwei
        self.zhicheng = tc_zhicheng
        self.phone = tc_phone
        self.QQ = tc_QQ
        self.email = tc_email
        self.checkstate = tc_checkstate

        # 信息布局
        flex.AddMany([
            (st_Name, 0, wx.ALIGN_RIGHT), (tc_Name, 0, wx.EXPAND),
            (st_certNo, 0, wx.ALIGN_RIGHT), (tc_certNo, 0, wx.EXPAND),
            (st_password, 0, wx.ALIGN_RIGHT), (tc_password, 0, wx.EXPAND),
            (st_sex, 0, wx.ALIGN_RIGHT), (tc_gender, 0, wx.EXPAND),
            (st_birth, 0, wx.ALIGN_RIGHT), (tc_birth, 0, wx.EXPAND),
            (st_job, 0, wx.ALIGN_RIGHT), (tc_job, 0, wx.EXPAND),
            (st_school, 0, wx.ALIGN_RIGHT), (tc_school, 0, wx.EXPAND),
            (st_degree, 0, wx.ALIGN_RIGHT), (tc_degreeType, 0, wx.EXPAND),
            (st_danwei, 0, wx.ALIGN_RIGHT), (tc_danwei, 0, wx.EXPAND),
            (st_zhicheng, 0, wx.ALIGN_RIGHT), (tc_zhicheng, 0, wx.EXPAND),
            (st_phone, 0, wx.ALIGN_RIGHT), (tc_phone, 0, wx.EXPAND),
            (st_QQ, 0, wx.ALIGN_RIGHT), (tc_QQ, 0, wx.EXPAND),
            (st_email, 0, wx.ALIGN_RIGHT), (tc_email, 0, wx.EXPAND),
            (st_checkstate, 0, wx.ALIGN_RIGHT), (tc_checkstate, 0, wx.EXPAND)
        ])
        flex.AddGrowableCol(1, 1)  # 控制第二列的proportion增长
        #
        hbox.Add(flex, 2, wx.EXPAND | wx.ALL, 10)
        #
        btn_save = wx.Button(self.panel, -1, label=u'确  定')
        btn_exit = wx.Button(self.panel, -1, label=u'退  出')
        # 按钮布局
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.AddMany([(btn_save, 0, wx.ALL, 10), (btn_exit, 0, wx.ALL, 10)])
        #
        self.vbox.Add(hbox, 1, wx.EXPAND | wx.ALL)
        self.vbox.Add(hbox1, 0, wx.CENTER | wx.ALL)
        self.panel.SetSizer(self.vbox)
        #
        # 选中的id和applicantid
        self.select_id = select_id
        # 通过行号获取第2列的值
        self.id = self.mainframe.list.GetItem(select_id, 1).Text  # 得到的是身份证号

        self.Bind(wx.EVT_BUTTON, self.saveUpdate, btn_save)
        self.Bind(wx.EVT_BUTTON, self.CancelButton, btn_exit)
        #
        self.showAllText()  # 展现所有的text原来取值

    def showAllText(self):
        '''显示专利原始信息'''
        data = self.getApplicantById(self.id)  # 通过申请人id获取申请人信息

        self.password.SetValue(data[0])  # 设置登录密码
        self.XingMing.SetValue(str(data[1]))  # 设置姓名
        self.certNo.SetValue(str(data[2]))  # 设置身份证号
        self.gender.SetValue(str(data[3]))  # 将单选按钮设置为选中或取消选中状态。
        self.birth.SetValue(str(data[4]))  # 设置出生日期
        self.job.SetValue(str(data[5]))  # 设置职业
        self.school.SetValue(str(data[6]))  # 设置毕业学校
        self.degreeType.SetValue(str(data[7]))  # 设置学历/学位类别
        self.danwei.SetValue(str(data[8]))  # 设置单位
        self.zhicheng.SetValue(str(data[9]))  # 设置职称
        self.phone.SetValue(str(data[10]))  # 设置手机号
        self.QQ.SetValue(str(data[11]))  # 设置QQ
        self.email.SetValue(str(data[12]))  # 设置电子邮箱
        self.checkstate.SetValue(str(data[13]))  # 设置用户状态

    # 修改申请人信息并保存
    def saveUpdate(self, evt):
        '''保存修改后的值'''
        user_state = self.checkstate.GetValue()
        state = ''
        try:
            param_11 = (user_state,)
            sql = "select id from user_state  where StateName=%s"
            datas = self.dbhelper.SelectRecord(sql, param_11)
            state = datas[0][0]

        except Exception as err:
            print("SQL执行错误，原因：", err)
        # 插入数据库
        self.checkUserUpdate(self.id, state)
        # 插入列表
        self.mainframe.list.SetItem(self.select_id, 12, user_state)
        self.Destroy()  # 销毁隐藏Dialog

    # 管理员审核用户信息时使用,通过申请人编号查询申请人信息
    def getApplicantById(self, id):
        '''根据申请人id值来寻找申请人信息'''
        sql = "select Password,TrueName, IDCard, Gender,Birthday,job.JobName,school.SchoolName,degree.DegreeName,unit.UnitName,\
                              Title,Phone,QQ, Email,user_state.StateName \
                               from user_info \
                                        INNER JOIN job ON user_info.Job=job.id\
                                        INNER JOIN school ON user_info.School=school.id \
                                        INNER JOIN degree ON user_info.Degree=degree.id \
                                        INNER JOIN unit ON user_info.Unit=unit.id \
                                        INNER JOIN user_state ON user_info.UserStatus=user_state.id \
                                        where IDCard=%s"
        try:
            param = (id,)
            datas = self.dbhelper.SelectRecord(sql, param)
            return datas[0]
        except Exception as e:
            print("SQL执行错误，原因：", e)

    # 管理员审核已注册的用户状态
    def checkUserUpdate(self, userid, userstate):
        '''用patent对象来修改id为patentid的专利信息'''
        sql = "update user_info set UserStatus=%s where IDCard=%s"
        try:
            param = (userstate, userid)
            self.dbhelper.UpdateData(sql, param)
        except Exception as e:
            print("SQL执行错误，原因：", e)

    # 退出按钮
    def CancelButton(self, event):
        self.Destroy()  # 销毁隐藏Dialog


# 管理申请人信息界面
class AdminApplicant(wx.Panel):
    def __init__(self, notebook, parent, dbhelper):
        wx.Panel.__init__(self, notebook)
        # 需要用到的数据库接口
        self.dbhelper = dbhelper
        # 初始化分页参数
        self.curPage = 1  # 设置当前页为1
        self.pageSize = 15  # 每页显示数量
        count = self.AdminGetCount(state=3)  # 总记录数
        self.totalPage = int(count[0][0] / self.pageSize)  # 总页数
        if count[0][0] % self.pageSize == 0:
            self.totalPage = int(count[0][0] / self.pageSize)
        else:
            self.totalPage += 1
        #
        self.parent = parent
        self.panel = self
        font1 = wx.Font(pointSize=14, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL, underline=False)

        # 组合框设计
        font3 = wx.Font(pointSize=13, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL, underline=False)
        self.label = wx.StaticText(self.panel, label="类型:", pos=(100, 35), size=(30, 25))
        languages = ['未选择', '身份证号', '姓名', '电话', 'QQ']
        self.combo = wx.ComboBox(self.panel, value='未选择', choices=languages, pos=(150, 35), size=(150, 35), style=wx.CB_READONLY)
        self.combo.SetFont(font3)
        #
        self.label1 = wx.StaticText(self.panel, label="关键字:", pos=(320, 35), size=(50, 25))
        self.label_text = wx.TextCtrl(self.panel, pos=(390, 35), size=(150, 25))
        self.label_text.SetFont(font3)
        # 查询按钮设计
        query_button = wx.Button(self.panel, label="查  询", pos=(600, 35), size=(80, 30), style=wx.BORDER_MASK)

        # 生成一个列表
        self.list = wx.ListCtrl(self.panel, -1, size=(1200, 340), pos=(0, 110),
                                style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        # 列表有散列，分别是申请人身份证号,姓名，性别，出生日期等描述
        self.list.InsertColumn(0, "姓名")
        self.list.InsertColumn(1, "身份证号")
        self.list.InsertColumn(2, "性别")
        self.list.InsertColumn(3, "出生日期")
        self.list.InsertColumn(4, "职业")
        self.list.InsertColumn(5, "毕业学校")
        self.list.InsertColumn(6, "学历/学位")
        self.list.InsertColumn(7, "工作单位")
        self.list.InsertColumn(8, "职称")
        self.list.InsertColumn(9, "手机号")
        self.list.InsertColumn(10, "QQ号")
        self.list.InsertColumn(11, "电子邮箱")
        self.list.InsertColumn(12, "审核状态")

        # 设置各列的宽度
        self.list.SetColumnWidth(0, 60)  # 设置每一列的宽度
        self.list.SetColumnWidth(1, 140)  # 设置每一列的宽度
        self.list.SetColumnWidth(2, 40)
        self.list.SetColumnWidth(3, 90)
        self.list.SetColumnWidth(4, 80)
        self.list.SetColumnWidth(5, 80)
        self.list.SetColumnWidth(6, 80)
        self.list.SetColumnWidth(7, 100)
        self.list.SetColumnWidth(8, 100)
        self.list.SetColumnWidth(9, 100)
        self.list.SetColumnWidth(10, 80)
        self.list.SetColumnWidth(11, 140)
        self.list.SetColumnWidth(12, 110)
        #  设置字体
        font2 = wx.Font(pointSize=13, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL, underline=False)
        self.list.SetFont(font2)
        # 定义一组按钮
        # 首页按钮
        first_page_button = wx.Button(self.panel, label="首  页", pos=(200, 500), size=(80, 35), style=wx.BORDER_MASK)
        # 上一页按钮
        previous_page_button = wx.Button(self.panel, label="上一页", pos=(300, 500), size=(80, 35), style=wx.BORDER_MASK)
        # 页码按钮
        one_page_button = wx.Button(self.panel, label="1", pos=(390, 500), size=(30, 35))
        two_page_button = wx.Button(self.panel, label="2", pos=(430, 500), size=(30, 35))
        three_page_button = wx.Button(self.panel, label="3", pos=(470, 500), size=(30, 35))
        four_page_button = wx.Button(self.panel, label="4", pos=(510, 500), size=(30, 35))
        five_page_button = wx.Button(self.panel, label="5", pos=(550, 500), size=(30, 35))
        # 下一页按钮
        next_page_button = wx.Button(self.panel, label="下一页", pos=(590, 500), size=(80, 35), style=wx.BORDER_MASK)
        # 尾页按钮
        end_page_button = wx.Button(self.panel, label="尾  页", pos=(690, 500), size=(80, 35), style=wx.BORDER_MASK)
        # 审核
        check_button = wx.Button(self.panel, label="审  核", pos=(850, 500), size=(80, 35), style=wx.BORDER_MASK)
        # 取消
        cancel_button = wx.Button(self.panel, label="退  出", pos=(1000, 500), size=(80, 35), style=wx.BORDER_MASK)
        #
        self.label.SetFont(font1)
        self.label1.SetFont(font1)
        query_button.SetFont(font1)
        check_button.SetFont(font1)
        cancel_button.SetFont(font1)
        first_page_button.SetFont(font1)
        previous_page_button.SetFont(font1)
        one_page_button.SetFont(font1)
        two_page_button.SetFont(font1)
        three_page_button.SetFont(font1)
        four_page_button.SetFont(font1)
        five_page_button.SetFont(font1)
        next_page_button.SetFont(font1)
        end_page_button.SetFont(font1)
        # 为按钮绑定相应事件函数
        query_button.Bind(wx.EVT_BUTTON, self.queryApplicant)
        # 首页，尾页
        first_page_button.Bind(wx.EVT_BUTTON, self.PagingQuery)
        end_page_button.Bind(wx.EVT_BUTTON, self.PagingQuery)
        # 1,2,3,4,5页
        one_page_button.Bind(wx.EVT_BUTTON, self.PagingQuery)
        two_page_button.Bind(wx.EVT_BUTTON, self.PagingQuery)
        three_page_button.Bind(wx.EVT_BUTTON, self.PagingQuery)
        four_page_button.Bind(wx.EVT_BUTTON, self.PagingQuery)
        five_page_button.Bind(wx.EVT_BUTTON, self.PagingQuery)
        # 上一页，下一页
        previous_page_button.Bind(wx.EVT_BUTTON, self.PagingQuery)
        next_page_button.Bind(wx.EVT_BUTTON, self.PagingQuery)
        #
        check_button.Bind(wx.EVT_BUTTON, self.checkApplicant)
        cancel_button.Bind(wx.EVT_BUTTON, self.CancelButton)

        # self.showApplicant()

    def showApplicant(self, label_value='', label_value3='', datas=None):
        # label_value:关键字，label_value3:类型
        '''显示原始信息'''
        # 显示查找的信息
        if label_value != '' and label_value3 != '':
            # 先清空列表
            for i in range(30):
                self.list.DeleteItem(0)
            self.value = label_value
            self.value1 = label_value3
            # 初始化分页参数
            self.curPage = 1  # 设置当前页为1
            self.pageSize = 15  # 每页显示数量
            count = self.AdminGetCount(state=4, label_value=label_value, label_value2=label_value3)  # 记录数
            self.totalPage = int(count[0][0] / self.pageSize)  # 总页数
            if count[0][0] % self.pageSize == 0:
                self.totalPage = int(count[0][0] / self.pageSize)
            else:
                self.totalPage += 1
            page_num = wx.StaticText(self, label="第" + str(self.curPage) + "页" + "/共" + str(self.totalPage) + "页",
                          pos=(80, 510), size=(100, 25))
            self.P_N = page_num.GetLabel()[1]
            startRow = (self.curPage - 1) * self.pageSize  # 起始索引
            # 通过输入的关键字和下拉框中的值来查询专利信息
            datas = self.AdmingetApplicantByValue(label_value, label_value3, startRow, self.pageSize)
            if datas == ():
                warn = wx.MessageDialog(self, message="对不起，暂时没有查询到你想要的结果", caption="温馨提示",
                                        style=wx.OK | wx.ICON_INFORMATION)
                warn.ShowModal()  # 提示
                warn.Destroy()
        else:  # 分页的时候进行判断
            # 先清空列表
            for i in range(30):
                self.list.DeleteItem(0)
        for data in datas:
            index = self.list.InsertItem(self.list.GetItemCount(), str(data[0]))
            self.list.SetItem(index, 1, str(data[1]))
            self.list.SetItem(index, 2, str(data[2]))
            self.list.SetItem(index, 3, str(data[3]))
            self.list.SetItem(index, 4, str(data[4]))
            self.list.SetItem(index, 5, str(data[5]))
            self.list.SetItem(index, 6, str(data[6]))
            self.list.SetItem(index, 7, str(data[7]))
            self.list.SetItem(index, 8, str(data[8]))
            self.list.SetItem(index, 9, str(data[9]))
            self.list.SetItem(index, 10, str(data[10]))
            self.list.SetItem(index, 11, str(data[11]))
            self.list.SetItem(index, 12, str(data[12]))

    # 分页查询
    def PagingQuery(self, event):
        obj = event.GetEventObject()
        val = obj.GetLabel()
        if val == '1' or val == '2' or val == '3' or val == '4' or val == '5' or val == '6' or val == '7' or val == '8' \
                or val == '9' or val == '10':
            page_val = int(val)
            self.curPage = page_val  # 修改默认页码
            if self.curPage > self.totalPage:
                warn = wx.MessageDialog(self, message="所查数据只有"+str(self.totalPage)+"页", caption="温馨提示", style=wx.OK | wx.ICON_INFORMATION)
                warn.ShowModal()  # 提示错误
                warn.Destroy()
            else:
                page_num = wx.StaticText(self.panel, label="第" + str(self.curPage) + "页" + "/共" + str(self.totalPage) + "页",
                              pos=(80, 510), size=(100, 25))
                self.P_N = page_num.GetLabel()[1]
                startRow = (self.curPage - 1) * self.pageSize  # 起始索引
                ret = self.AdminPagingQueryUser(startRow, self.pageSize)
                self.showApplicant(label_value='1', label_value3='', datas=ret)
        elif val == "首  页":
            self.curPage = 1
            self.P_N = '1'
            wx.StaticText(self.panel, label="第" + str(self.curPage) + "页" + "/共" + str(self.totalPage) + "页",
                          pos=(80, 510), size=(100, 25))
            startRow = (self.curPage - 1) * self.pageSize  # 起始索引
            ret = self.AdminPagingQueryUser(startRow, self.pageSize)
            self.showApplicant(label_value='1', label_value3='', datas=ret)
        elif val == "上一页":
            if int(self.P_N) <= self.totalPage and int(self.P_N) > 0:
                self.curPage = int(self.P_N)
                self.P_N = str(int(self.P_N)-1)
            elif int(self.P_N) > self.totalPage:
                self.curPage = self.totalPage
                self.P_N = str(int(self.P_N)-1)
            self.curPage = self.curPage - 1
            if self.curPage <= 0:
                self.curPage = 1
                warn = wx.MessageDialog(self, message="当前是第一页", caption="温馨提示", style=wx.OK | wx.ICON_INFORMATION)
                warn.ShowModal()  # 提示错误
                warn.Destroy()
            else:
                wx.StaticText(self.panel, label="第" + str(self.curPage) + "页" + "/共" + str(self.totalPage) + "页",
                              pos=(80, 510), size=(100, 25))
                startRow = (self.curPage - 1) * self.pageSize  # 起始索引
                ret = self.AdminPagingQueryUser(startRow, self.pageSize)
                self.showApplicant(label_value='1', label_value3='', datas=ret)
        elif val == "下一页":
            if int(self.P_N) < self.totalPage and int(self.P_N) > 0:
                self.curPage = int(self.P_N)
                self.P_N = str(int(self.P_N)+1)
            self.curPage = self.curPage + 1
            if self.curPage > self.totalPage:
                self.curPage = self.curPage - 1
                warn = wx.MessageDialog(self, message="当前是最后一页", caption="温馨提示", style=wx.OK | wx.ICON_INFORMATION)
                warn.ShowModal()  # 提示错误
                warn.Destroy()
            else:
                wx.StaticText(self.panel, label="第" + str(self.curPage) + "页" + "/共" + str(self.totalPage) + "页",
                              pos=(80, 510), size=(100, 25))
                startRow = (self.curPage - 1) * self.pageSize  # 起始索引
                ret = self.AdminPagingQueryUser(startRow, self.pageSize)
                self.showApplicant(label_value='1', label_value3='', datas=ret)
        elif val == "尾  页":
            self.curPage = self.totalPage
            self.P_N = str(self.totalPage)
            wx.StaticText(self.panel, label="第" + str(self.curPage) + "页" + "/共" + str(self.totalPage) + "页",
                          pos=(80, 510), size=(100, 25))
            startRow = (self.curPage - 1) * self.pageSize  # 起始索引
            ret = self.AdminPagingQueryUser(startRow, self.pageSize)
            self.showApplicant(label_value='1', label_value3='', datas=ret)

    def queryApplicant(self, evt):
        # 获取输入的值
        label_value = self.label_text.GetValue()
        # 获取组合框的值
        label_value3 = self.combo.GetValue()
        if label_value == '':
            warn = wx.MessageDialog(self, message="未输入关键词！！！", caption="温馨提示", style=wx.OK | wx.ICON_INFORMATION)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
        else:
            self.showApplicant(label_value, label_value3)

    # 审核申请人信息
    def checkApplicant(self, evt):
        '''修改按钮响应事件，点击修改按钮，弹出修改框'''
        selectId = self.list.GetFirstSelected()  # 得到选中的行数
        if selectId == -1:
            warn = wx.MessageDialog(self, message="未选中任何条目！！！", caption="温馨提示", style=wx.OK | wx.ICON_INFORMATION)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return
        else:
            if self.list.GetItem(selectId, 12).Text == '审核通过' or self.list.GetItem(selectId, 7).Text == '审核未通过':
                warn = wx.MessageDialog(self, message="审核通过的不能进行审核", caption="温馨提示", style=wx.OK | wx.ICON_INFORMATION)
                warn.ShowModal()  # 提示错误
                warn.Destroy()
            else:
                check_f = CheckApplicantFrame(self, "审核申请人窗口", selectId, self.dbhelper)
                check_f.Show(True)

    # 管理员查询用户信息总数
    def AdminGetCount(self, state=None, label_value=None, label_value2=None):
        sql = ""
        if state == 3:  # 管理员查询用户信息使用
            sql = "select count(*) from user_info"
        elif label_value2 == '身份证号':
            sql = "select count(*) from user_info where IDCard like CONCAT('%%',%s,'%%') "
        elif label_value2 == '姓名':
            sql = "select count(*) from user_info where TrueName like CONCAT('%%',%s,'%%')"
        elif label_value2 == '电话':
            sql = "select count(*) from user_info where Phone like CONCAT('%%',%s,'%%')"
        elif label_value2 == 'QQ':
            sql = "select count(*) from user_info where QQ like CONCAT('%%',%s,'%%')"
        try:
            if state == 3:
                param = ()
                datas = self.dbhelper.SelectRecord(sql, param)
            else:
                param = (label_value,)
                datas = self.dbhelper.SelectRecord(sql, param)
            return datas
        except Exception as e:
            print("查询记录失败:", e)

        # 管理员分页查询所有用户信息,不用输入关键字时使用
    def AdminPagingQueryUser(self, startRow, pageSize):
        sql = "select TrueName, IDCard, Gender,Birthday,job.JobName,school.SchoolName,degree.DegreeName,unit.UnitName,\
                          Title,Phone,QQ, Email,user_state.StateName \
                           from user_info \
                                    INNER JOIN job ON user_info.Job=job.id\
                                    INNER JOIN school ON user_info.School=school.id \
                                    INNER JOIN degree ON user_info.Degree=degree.id \
                                    INNER JOIN unit ON user_info.Unit=unit.id \
                                    INNER JOIN user_state ON user_info.UserStatus=user_state.id \
                                    limit %s,%s"
        try:
            param = (startRow, pageSize)
            datas = self.dbhelper.SelectRecord(sql, param)
            return datas
        except Exception as e:
            print("查询记录失败:", e)

    # 管理员通过输入关键字查询用户基本信息，还没有修改
    def AdmingetApplicantByValue(self, label_value, label_value2, startRow, pageSize):
        '''根据关键字来寻找申请人信息'''
        sql = ""
        if label_value2 == '身份证号':
            sql = "select TrueName, IDCard, Gender,Birthday,job.JobName,school.SchoolName,degree.DegreeName,unit.UnitName,\
                          Title,Phone,QQ, Email,user_state.StateName \
                           from user_info \
                                    INNER JOIN job ON user_info.Job=job.id\
                                    INNER JOIN school ON user_info.School=school.id \
                                    INNER JOIN degree ON user_info.Degree=degree.id \
                                    INNER JOIN unit ON user_info.Unit=unit.id \
                                    INNER JOIN user_state ON user_info.UserStatus=user_state.id \
                                    where IDCard like CONCAT('%%',%s,'%%') limit %s,%s"
        elif label_value2 == '电话':
            sql = "select TrueName, IDCard, Gender,Birthday,job.JobName,school.SchoolName,degree.DegreeName,unit.UnitName,\
                          Title,Phone,QQ, Email,user_state.StateName \
                           from user_info \
                                    INNER JOIN job ON user_info.Job=job.id\
                                    INNER JOIN school ON user_info.School=school.id \
                                    INNER JOIN degree ON user_info.Degree=degree.id \
                                    INNER JOIN unit ON user_info.Unit=unit.id \
                                    INNER JOIN user_state ON user_info.UserStatus=user_state.id \
                                    where Phone like CONCAT('%%',%s,'%%') limit %s,%s"
        elif label_value2 == '姓名':
            sql = "select TrueName, IDCard, Gender,Birthday,job.JobName,school.SchoolName,degree.DegreeName,unit.UnitName,\
                          Title,Phone,QQ, Email,user_state.StateName \
                           from user_info \
                                    INNER JOIN job ON user_info.Job=job.id\
                                    INNER JOIN school ON user_info.School=school.id \
                                    INNER JOIN degree ON user_info.Degree=degree.id \
                                    INNER JOIN unit ON user_info.Unit=unit.id \
                                    INNER JOIN user_state ON user_info.UserStatus=user_state.id \
                                    where TrueName like CONCAT('%%',%s,'%%') limit %s,%s"
        elif label_value2 == 'QQ':
            sql = "select TrueName, IDCard, Gender,Birthday,job.JobName,school.SchoolName,degree.DegreeName,unit.UnitName,\
                          Title,Phone,QQ, Email,user_state.StateName \
                           from user_info \
                                    INNER JOIN job ON user_info.Job=job.id\
                                    INNER JOIN school ON user_info.School=school.id \
                                    INNER JOIN degree ON user_info.Degree=degree.id \
                                    INNER JOIN unit ON user_info.Unit=unit.id \
                                    INNER JOIN user_state ON user_info.UserStatus=user_state.id \
                                    where QQ like CONCAT('%%',%s,'%%') limit %s,%s"
        try:
            param = (label_value, startRow, pageSize)  # 参数以元组形式给出
            datas = self.dbhelper.SelectRecord(sql, param)
            return datas  # 返回该专利信息
        except Exception as e:
            print("SQL执行错误，原因：", e)

    # 退出界面
    def CancelButton(self, event):
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
