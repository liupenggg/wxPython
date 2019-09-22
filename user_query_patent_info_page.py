import wx
import wx.adv
import time


# 左键双击查询专利详细信息
class DclickQueryPatent(wx.Frame):
    # 进行初始化
    def __init__(self, parent, title, select_id, dbhelper):
        # 用来调用父frame,便于更新
        self.mainframe = parent
        # 生成一个500*500的框
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
        # 创建垂直方向box布局管理器
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        # 设置水平布局
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        # Wx.FlexiGridSizer(rows, cols, vgap, hgap)  # 行,列,垂直间距,水平间距
        fgs = wx.FlexGridSizer(10, 2, 10, 10)
        # 十一个编辑框,分别用来编辑专利编号,专利名称,功能描述,基础类别,地域类别,功能类别相关信息
        patentID_tip = wx.StaticText(self.panel, label="专利编号:")
        patentName_tip = wx.StaticText(self.panel, label="专利名称:")
        fun_info_tip = wx.StaticText(self.panel, label="功能描述:")
        baseclass_tip = wx.StaticText(self.panel, label="基础类别:")
        areaclass_tip = wx.StaticText(self.panel, label="地域类别:")
        funclass_tip = wx.StaticText(self.panel, label="专利类型:")
        appName_tip = wx.StaticText(self.panel, label="申请人姓名:")
        appID_tip = wx.StaticText(self.panel, label="身份证号:")
        auditdate_tip = wx.StaticText(self.panel, label="审核日期:")
        patentstatus_tip = wx.StaticText(self.panel, label="专利状态:")
        #
        patentID_text = wx.TextCtrl(self.panel)
        patentName_text = wx.TextCtrl(self.panel)
        fun_info_text = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE)
        baseclass_text = wx.TextCtrl(self.panel)
        areaclass_text = wx.TextCtrl(self.panel)
        funclass_text = wx.TextCtrl(self.panel)
        appName_text = wx.TextCtrl(self.panel)
        appID_text = wx.TextCtrl(self.panel)
        auditdate_text = wx.TextCtrl(self.panel)
        patentstatus_text = wx.TextCtrl(self.panel)
        #
        patentID_text.SetEditable(False)
        appName_text.SetEditable(False)
        appID_text.SetEditable(False)
        patentName_text.SetEditable(False)
        fun_info_text.SetEditable(False)
        baseclass_text.SetEditable(False)
        areaclass_text.SetEditable(False)
        funclass_text.SetEditable(False)
        appID_text.SetEditable(False)
        auditdate_text.SetEditable(False)
        patentstatus_text.SetEditable(False)
        #
        self.PatentID = patentID_text
        self.PatentName = patentName_text
        self.PatentFunctional = fun_info_text
        self.BaseClass = baseclass_text
        self.RegionalCategory = areaclass_text
        self.FunctionCategory = funclass_text
        self.ApplicantName = appName_text
        self.ApplicantID = appID_text
        self.AuditDate = auditdate_text
        self.patentstatus = patentstatus_text
        #
        fgs.AddMany([(patentID_tip), (patentID_text, 1, wx.EXPAND),
                     (patentName_tip), (patentName_text, 1, wx.EXPAND),
                     (fun_info_tip, 1, wx.EXPAND), (fun_info_text, 1, wx.EXPAND),
                     (baseclass_tip), (baseclass_text, 1, wx.EXPAND),
                     (areaclass_tip), (areaclass_text, 1, wx.EXPAND),
                     (funclass_tip), (funclass_text, 1, wx.EXPAND),
                     (appName_tip), (appName_text, 1, wx.EXPAND),
                     (appID_tip), (appID_text, 1, wx.EXPAND),
                     (auditdate_tip), (auditdate_text, 1, wx.EXPAND),
                     (patentstatus_tip, 0, wx.EXPAND), (patentstatus_text, 0, wx.EXPAND)])
        fgs.AddGrowableRow(2, 1)  # 控制第三行的proportion增长
        fgs.AddGrowableCol(1, 1)  # 控制第二列的proportion增长
        #
        hbox.Add(fgs, proportion=2, flag=wx.ALL | wx.EXPAND, border=10)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        # 设置按钮
        cancel_button = wx.Button(self.panel, label="取  消", size=(100, 40))
        self.Bind(wx.EVT_BUTTON, self.CancelButton, cancel_button)
        hbox1.Add(cancel_button, flag=wx.ALL, border=10)
        #
        self.vbox.Add(hbox, proportion=1, flag=wx.ALL | wx.EXPAND)
        self.vbox.Add(hbox1, flag=wx.ALL | wx.CENTER)

        self.panel.SetSizer(self.vbox)

        # 选中的id和patentid
        self.select_id = select_id
        # 通过行号获取第0列的值,就是专利编号
        self.patentid = self.mainframe.list.GetItem(select_id, 0).Text
        print(select_id, "专利编号:", self.patentid)

        self.showAllText()  # 展现所有的text原来取值

    def showAllText(self):
        '''显示专利原始信息'''
        data = self.UserQuerygetPatentById(self.patentid)  # 通过专利id获取专利信息

        self.PatentID.SetValue(str(data[0][0]))  # 设置值
        self.PatentName.SetValue(str(data[0][1]))  # 设置值
        self.PatentFunctional.SetValue(str(data[0][2]))
        self.BaseClass.SetValue(str(data[0][3]))
        self.RegionalCategory.SetValue(str(data[0][4]))
        self.FunctionCategory.SetValue(str(data[0][5]))
        self.ApplicantName.SetValue(str(data[0][6]))
        self.ApplicantID.SetValue('******************')
        self.AuditDate.SetValue(str(data[0][8]))  # 设置日期
        self.patentstatus.SetValue(str(data[0][9]))  # 设置日期

    # 在用户双击查询审核通过专利时使用，用来显示专利原始信息,修改完成
    def UserQuerygetPatentById(self, patentid):
        '''根据申请人id值来寻找专利信息'''
        # 定义SQL语句
        sql = "select PatentID, PatentName, PatentFunction, base_category.BaseName, region_category.RegionName, function_category.FunctionName,\
                                      user_info.TrueName, patent_info.IDCard, AuditDate, patent_state.StateName \
                               from patent_info \
                                    INNER JOIN patent_state ON patent_info.PatentStatus=patent_state.id\
                                    INNER JOIN user_info ON patent_info.IDCard=user_info.IDCard \
                                    INNER JOIN base_category ON patent_info.BaseCategory=base_category.id \
                                    INNER JOIN region_category ON patent_info.RegionCategory=region_category.id \
                                    INNER JOIN function_category ON patent_info.FunctionCategory=function_category.id \
                                    where patent_info.PatentID=%s"
        try:
            param = (patentid,)
            datas = self.dbhelper.SelectRecord(sql, param)
            return datas
        except Exception as e:
            print("查询记录失败:", e)

    # 取消按钮
    def CancelButton(self, event):
        self.Destroy()  # 销毁隐藏Dialog


# 查询专利信息界面
class UserQueryPatent(wx.Panel):
    def __init__(self, notebook, parent, dbhelper):
        wx.Panel.__init__(self, notebook)
        # 需要用到的数据库接口
        self.dbhelper = dbhelper
        #
        self.parent = parent
        self.panel = self
        self.value = None
        self.value1 = None
        self.value2 = None
        self.value3 = None
        # 初始化分页参数
        self.startRow = 0
        self.curPage = 1  # 设置当前页为1
        self.pageSize = 15  # 每页显示数量
        font1 = wx.Font(pointSize=14, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL, underline=False)

        # 组合框设计
        self.label = wx.StaticText(self.panel, label="类型:", pos=(160, 35), size=(30, 25))
        languages = ['未选择', '申请人姓名', '专利名称', '专利类型', '基础类别', '地域类别', '专利状态']
        self.combo = wx.ComboBox(self.panel, value='未选择', choices=languages, pos=(220, 35), size=(150, 35), style=wx.CB_READONLY)
        # 输入框设计
        self.label1 = wx.StaticText(self.panel, label="关键字:", pos=(430, 35), size=(50, 25))
        self.label_text = wx.TextCtrl(self.panel, pos=(510, 35), size=(150, 25))
        # 申请时间
        self.label2 = wx.StaticText(self.panel, label="起始审核日期:", pos=(90, 65), size=(60, 25))
        self.label_text1 = wx.adv.DatePickerCtrl(self, -1, pos=(220, 65), size=(150, 25),
                                                 style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY | wx.adv.DP_ALLOWNONE)
        # 截止时间
        self.label3 = wx.StaticText(self.panel, label="截止审核日期:", pos=(380, 65), size=(60, 25))
        self.label_text2 = wx.adv.DatePickerCtrl(self, -1, pos=(510, 65), size=(150, 25),
                                                 style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY | wx.adv.DP_ALLOWNONE)
        # 查询按钮设计
        query_button = wx.Button(self.panel, label="查  询", pos=(680, 35), size=(80, 35), style=wx.BORDER_MASK)

        # 首页按钮
        first_page_button = wx.Button(self.panel, label="首  页", pos=(300, 500), size=(80, 35), style=wx.BORDER_MASK)
        # 查询上一页按钮
        previous_page_button = wx.Button(self.panel, label="上一页", pos=(400, 500), size=(80, 35), style=wx.BORDER_MASK)
        # 页码按钮
        one_page_button = wx.Button(self.panel, label="1", pos=(490, 500), size=(30, 35))
        two_page_button = wx.Button(self.panel, label="2", pos=(530, 500), size=(30, 35))
        three_page_button = wx.Button(self.panel, label="3", pos=(570, 500), size=(30, 35))
        four_page_button = wx.Button(self.panel, label="4", pos=(610, 500), size=(30, 35))
        five_page_button = wx.Button(self.panel, label="5", pos=(650, 500), size=(30, 35))
        # 查询下一页按钮
        next_page_button = wx.Button(self.panel, label="下一页", pos=(690, 500), size=(80, 35), style=wx.BORDER_MASK)
        # 尾页按钮
        end_page_button = wx.Button(self.panel, label="尾  页", pos=(790, 500), size=(80, 35), style=wx.BORDER_MASK)
        # 退出按钮设计
        cancel_button = wx.Button(self.panel, label="退  出", pos=(1000, 500), size=(80, 35), style=wx.BORDER_MASK)
        #
        self.label.SetFont(font1)
        self.label1.SetFont(font1)
        self.label2.SetFont(font1)
        self.label3.SetFont(font1)
        query_button.SetFont(font1)
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
        self.Bind(wx.EVT_BUTTON, self.queryPatent, query_button)
        self.Bind(wx.EVT_BUTTON, self.CancelButton, cancel_button)
        # 首页，尾页
        self.Bind(wx.EVT_BUTTON, self.PagingQuery, first_page_button)
        self.Bind(wx.EVT_BUTTON, self.PagingQuery, end_page_button)
        # 1,2,3,4,5页
        self.Bind(wx.EVT_BUTTON, self.PagingQuery, one_page_button)
        self.Bind(wx.EVT_BUTTON, self.PagingQuery, two_page_button)
        self.Bind(wx.EVT_BUTTON, self.PagingQuery, three_page_button)
        self.Bind(wx.EVT_BUTTON, self.PagingQuery, four_page_button)
        self.Bind(wx.EVT_BUTTON, self.PagingQuery, five_page_button)
        #
        self.Bind(wx.EVT_BUTTON, self.PagingQuery, previous_page_button)
        self.Bind(wx.EVT_BUTTON, self.PagingQuery, next_page_button)

        # 生成一个列表
        self.list = wx.ListCtrl(self.panel, -1, size=(1200, 340), pos=(0, 110),
                                style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        # 列表有散列，分别是专利ID,专利名，功能描述
        self.list.InsertColumn(0, "专利编号")
        self.list.InsertColumn(1, "专利名称")
        self.list.InsertColumn(2, "基础类别")
        self.list.InsertColumn(3, "地域类别")
        self.list.InsertColumn(4, "专利类型")
        self.list.InsertColumn(5, "申请人")
        self.list.InsertColumn(6, "审核日期")
        self.list.InsertColumn(7, "专利状态")

        # 设置各列的宽度
        self.list.SetColumnWidth(0, 100)  # 设置每一列的宽度
        self.list.SetColumnWidth(1, 300)
        self.list.SetColumnWidth(2, 100)
        self.list.SetColumnWidth(3, 100)
        self.list.SetColumnWidth(4, 100)
        self.list.SetColumnWidth(5, 100)
        self.list.SetColumnWidth(6, 200)
        self.list.SetColumnWidth(7, 200)
        #  设置字体
        font2 = wx.Font(pointSize=13, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL, underline=False)
        self.list.SetFont(font2)
        # 给列表增加左键双击
        self.list.Bind(wx.EVT_LEFT_DCLICK, self.OnFrameLeftDclick)
        self.list.SetToolTip(wx.ToolTip('左键双击查询专利详细信息'))

    def showPatent(self, label_value='', label_value3='', label_value1='', label_value2='', datas=None):
        # label_value:关键字，label_value1:起始申请日，label_value2:截止申请日，label_value3:类型
        '''显示原始信息'''
        # 只通过时间查询
        if label_value == '' and label_value3 == '未选择':
            # 先清空列表
            for i in range(30):
                self.list.DeleteItem(0)
            self.value1 = label_value3
            self.value2 = label_value1
            self.value3 = label_value2
            # 初始化分页参数
            self.curPage = 1  # 设置当前页为1
            count = self.UserGetCount(state=2, label_value=label_value, label_value2=label_value3,
                                      label_value3=label_value1, label_value4=label_value2)  # 记录数
            if count[0][0] != 0:
                # 计算总页数
                self.totalPage = int(count[0][0] / self.pageSize)
                if count[0][0] % self.pageSize == 0:
                    self.totalPage = int(count[0][0] / self.pageSize)
                else:
                    self.totalPage += 1
                # 只能找到审核通过的所有专利信息
                wx.StaticText(self, label="第" + str(self.curPage) + "页" + "/共" + str(self.totalPage) + "页",
                              pos=(180, 510), size=(100, 25))
                self.startRow = (self.curPage - 1) * self.pageSize  # 起始索引
                datas = self.UserPagingQuery(label_value1, label_value2, self.startRow, self.pageSize)
            elif count[0][0] == 0:
                warn = wx.MessageDialog(self, message="对不起，暂时没有查询到你想要的结果", caption="温馨提示",
                                        style=wx.OK | wx.ICON_INFORMATION)
                warn.ShowModal()  # 提示
                warn.Destroy()
        # 通过关键字和时间联合查询
        elif label_value != '' and label_value3 != '':
            # 先清空列表
            for i in range(30):
                self.list.DeleteItem(0)
            # 通过输入的关键字和下拉框中的值来查询专利信息
            self.value = label_value
            self.value1 = label_value3
            self.value2 = label_value1
            self.value3 = label_value2
            # 初始化分页参数
            self.curPage = 1  # 设置当前页为1
            count = self.UserGetCount(state=2, label_value=label_value, label_value2=label_value3,
                                               label_value3=label_value1, label_value4=label_value2)  # 记录数
            if count[0][0] != 0:
                # 计算总页数
                self.totalPage = int(count[0][0] / self.pageSize)
                if count[0][0] % self.pageSize == 0:
                    self.totalPage = int(count[0][0] / self.pageSize)
                else:
                    self.totalPage += 1
                page_num = wx.StaticText(self, label="第" + str(self.curPage) + "页" + "/共" + str(self.totalPage) + "页",
                              pos=(180, 510), size=(100, 25))
                self.P_N = page_num.GetLabel()[1]
                self.startRow = (self.curPage - 1) * self.pageSize  # 起始索引
                datas = self.UserQueryPatentByValue(label_value, label_value3, label_value1, label_value2,
                                                    self.startRow, self.pageSize)
            # 如果查询不到专利，执行下面代码
            elif count[0][0] == 0:
                datas = None
                warn = wx.MessageDialog(self, message="对不起，暂时没有查询到你想要的结果", caption="温馨提示",
                                        style=wx.OK | wx.ICON_INFORMATION)
                warn.ShowModal()  # 提示
                warn.Destroy()
        else:
            # 先清空列表
            for i in range(30):
                self.list.DeleteItem(0)
        if datas != None:
            for data in datas:
                index = self.list.InsertItem(self.list.GetItemCount(), str(data[0]))
                self.list.SetItem(index, 1, str(data[1]))
                self.list.SetItem(index, 2, str(data[2]))
                self.list.SetItem(index, 3, str(data[3]))
                self.list.SetItem(index, 4, str(data[4]))
                self.list.SetItem(index, 5, str(data[5]))
                self.list.SetItem(index, 6, str(data[6]))
                self.list.SetItem(index, 7, str(data[7]))

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
                page_num = wx.StaticText(self, label="第" + str(self.curPage) + "页" + "/共" + str(self.totalPage) + "页",
                              pos=(180, 510), size=(100, 25))
                self.P_N = page_num.GetLabel()[1]
                self.startRow = (self.curPage - 1) * self.pageSize  # 起始索引
                if self.value1 != '未选择':
                    ret = self.UserQueryPatentByValue(self.value, self.value1, self.value2, self.value3,
                                                      self.startRow,
                                                      self.pageSize)
                else:
                    ret = self.UserPagingQuery(self.value2, self.value3, self.startRow, self.pageSize)
                self.showPatent(label_value='1', label_value3='', label_value1='', label_value2='', datas=ret)
        elif val == "首  页":
            self.curPage = 1
            self.P_N = '1'
            wx.StaticText(self, label="第" + str(self.curPage) + "页" + "/共" + str(self.totalPage) + "页",
                          pos=(180, 510), size=(100, 25))

            self.startRow = (self.curPage - 1) * self.pageSize  # 起始索引
            if self.value1 != '未选择':
                ret = self.UserQueryPatentByValue(self.value, self.value1, self.value2, self.value3,
                                                  self.startRow,
                                                  self.pageSize)
            else:
                ret = self.UserPagingQuery(self.value2, self.value3, self.startRow, self.pageSize)
            self.showPatent(label_value='1', label_value3='', label_value1='', label_value2='', datas=ret)
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
                wx.StaticText(self, label="第" + str(self.curPage) + "页" + "/共" + str(self.totalPage) + "页",
                              pos=(180, 510), size=(100, 25))
                self.startRow = (self.curPage - 1) * self.pageSize  # 起始索引
                if self.value1 != '未选择':
                    ret = self.UserQueryPatentByValue(self.value, self.value1, self.value2, self.value3,
                                                      self.startRow,
                                                      self.pageSize)
                else:
                    ret = self.UserPagingQuery(self.value2, self.value3, self.startRow, self.pageSize)
                self.showPatent(label_value='1', label_value3='', label_value1='', label_value2='', datas=ret)
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
                wx.StaticText(self, label="第" + str(self.curPage) + "页" + "/共" + str(self.totalPage) + "页",
                              pos=(180, 510), size=(100, 25))
                self.startRow = (self.curPage - 1) * self.pageSize  # 起始索引
                if self.value1 != '未选择':
                    ret = self.UserQueryPatentByValue(self.value, self.value1, self.value2, self.value3,
                                                      self.startRow,
                                                      self.pageSize)
                else:
                    ret = self.UserPagingQuery(self.value2, self.value3, self.startRow, self.pageSize)
                self.showPatent(label_value='1', label_value3='', label_value1='', label_value2='', datas=ret)
        elif val == "尾  页":
            self.curPage = self.totalPage
            self.P_N = str(self.totalPage)
            wx.StaticText(self, label="第" + str(self.curPage) + "页" + "/共" + str(self.totalPage) + "页",
                          pos=(180, 510), size=(100, 25))
            self.startRow = (self.curPage - 1) * self.pageSize  # 起始索引
            if self.value1 != '未选择':
                ret = self.UserQueryPatentByValue(self.value, self.value1, self.value2, self.value3,
                                                  self.startRow,
                                                  self.pageSize)
            else:
                ret = self.UserPagingQuery(self.value2, self.value3, self.startRow, self.pageSize)
            self.showPatent(label_value='1', label_value3='', label_value1='', label_value2='', datas=ret)

    # 左键双击查询专利详细信息
    def OnFrameLeftDclick(self, event):
        lc = event.GetEventObject()
        item, flags = lc.HitTest(event.GetPosition())
        if item == -1:
            warn = wx.MessageDialog(self, message="未选中任何条目！！！", caption="温馨提示", style=wx.OK | wx.ICON_INFORMATION)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
        else:
            Dclick_f = DclickQueryPatent(self, "专利详细信息", item, self.dbhelper)
            Dclick_f.Show(True)
            event.Skip()

    # 查询专利信息
    def queryPatent(self, evt):
        '''查看按钮响应事件'''
        # 获取输入的值
        label_value = self.label_text.GetValue()  # 关键字
        label_value1 = self.label_text1.GetValue()  # 起始申请日
        label_value2 = self.label_text2.GetValue()  # 截止申请日
        label_value3 = self.combo.GetValue()  # 类型
        if str(label_value1) != 'INVALID DateTime' and str(label_value2) != 'INVALID DateTime':
            # 时间格式转换
            start_time = self.datetime_to_str(str(label_value1))
            deadline = self.datetime_to_str(str(label_value2))
        else:
            start_time = None
            deadline = None
        # 判断
        if label_value3 != '未选择':
            if label_value == '' and start_time == None and deadline == None:
                warn = wx.MessageDialog(self, message="未输入关键词！！！", caption="温馨提示",
                                        style=wx.OK | wx.ICON_INFORMATION)
                warn.ShowModal()  # 提示错误
                warn.Destroy()
            elif label_value == '' and start_time !=None and deadline != None:
                warn = wx.MessageDialog(self, message="未输入关键词！！！", caption="温馨提示", style=wx.OK | wx.ICON_INFORMATION)
                warn.ShowModal()  # 提示错误
                warn.Destroy()
            elif label_value != '' and start_time == None and deadline == None:
                self.showPatent(label_value, label_value3, start_time, deadline)
            elif label_value != '' and start_time != None and deadline != None:
                self.showPatent(label_value, label_value3, start_time, deadline)
        elif label_value3 == '未选择':
            if label_value != '' and start_time != None and deadline != None:
                warn = wx.MessageDialog(self, message="请先进行类型选择！！！", caption="温馨提示",
                                        style=wx.OK | wx.ICON_INFORMATION)
                warn.ShowModal()  # 提示错误
                warn.Destroy()
            elif label_value != '' and start_time ==None and deadline == None:
                warn = wx.MessageDialog(self, message="请先进行类型选择！！！", caption="温馨提示", style=wx.OK | wx.ICON_INFORMATION)
                warn.ShowModal()  # 提示错误
                warn.Destroy()
            elif label_value == '' and start_time == None and deadline == None:
                warn = wx.MessageDialog(self, message="请输入完整时间！！！", caption="温馨提示",
                                        style=wx.OK | wx.ICON_INFORMATION)
                warn.ShowModal()  # 提示错误
                warn.Destroy()
            elif label_value == '' and start_time != None and deadline != None:
                self.showPatent(label_value, label_value3, start_time, deadline)

    # 时间格式转换
    def datetime_to_str(self, dateTime):
        # Python time strptime() 函数根据指定的格式把一个时间字符串解析为时间元组。
        tempTime = time.strptime(dateTime, '%a %b %d %H:%M:%S %Y')
        # Python time strftime() 函数接收以时间元组，并返回以可读字符串表示的当地时间，格式由参数format决定。
        resTime = time.strftime('%Y-%m-%d', tempTime)
        return resTime

    # 用户通过日期分页查询所有审核通过的专利信息
    def UserPagingQuery(self, start_time, end_time, startRow, pageSize):
        sql_1 = "select PatentID, PatentName, base_category.BaseName, region_category.RegionName, function_category.FunctionName,\
                                  user_info.TrueName, AuditDate, patent_state.StateName \
                           from patent_info \
                                INNER JOIN patent_state ON patent_info.PatentStatus=patent_state.id\
                                INNER JOIN user_info ON patent_info.IDCard=user_info.IDCard \
                                INNER JOIN base_category ON patent_info.BaseCategory=base_category.id \
                                INNER JOIN region_category ON patent_info.RegionCategory=region_category.id \
                                INNER JOIN function_category ON patent_info.FunctionCategory=function_category.id \
                                where patent_info.PatentStatus='4' and patent_state.id='4' and (AuditDate between %s and %s) limit %s,%s"
        try:
            param = (start_time, end_time, startRow, pageSize)
            datas = self.dbhelper.SelectRecord(sql_1, param)
            return datas
        except Exception as e:
            print("查询记录失败:", e)

    # 用户通过关键字进行分页查询
    def UserQueryPatentByValue(self, label_value, label_value2, label_value3, label_value4, startRow, pageSize):
        # 定义SQL语句
        sql = ""
        if label_value2 == '申请人姓名':
            if label_value3 == None:
                sql = "select PatentID, PatentName, base_category.BaseName, region_category.RegionName, function_category.FunctionName,\
                                  user_info.TrueName, AuditDate, patent_state.StateName \
                           from patent_info \
                                INNER JOIN patent_state ON patent_info.PatentStatus=patent_state.id\
                                INNER JOIN user_info ON patent_info.IDCard=user_info.IDCard \
                                INNER JOIN base_category ON patent_info.BaseCategory=base_category.id \
                                INNER JOIN region_category ON patent_info.RegionCategory=region_category.id \
                                INNER JOIN function_category ON patent_info.FunctionCategory=function_category.id \
                                where patent_info.PatentStatus='4' and patent_state.id='4' and user_info.TrueName like CONCAT('%%',%s,'%%')\
                                     or (AuditDate between %s and %s) limit %s,%s"
            else:
                sql = "select PatentID, PatentName, base_category.BaseName, region_category.RegionName, function_category.FunctionName,\
                                  user_info.TrueName, AuditDate, patent_state.StateName \
                           from patent_info \
                                INNER JOIN patent_state ON patent_info.PatentStatus=patent_state.id\
                                INNER JOIN user_info ON patent_info.IDCard=user_info.IDCard \
                                INNER JOIN base_category ON patent_info.BaseCategory=base_category.id \
                                INNER JOIN region_category ON patent_info.RegionCategory=region_category.id \
                                INNER JOIN function_category ON patent_info.FunctionCategory=function_category.id \
                                where patent_info.PatentStatus='4' and patent_state.id='4' and user_info.TrueName like CONCAT('%%',%s,'%%')\
                                     and (AuditDate between %s and %s) limit %s,%s"
        elif label_value2 == '专利名称':
            if label_value3 == None:
                sql = "select PatentID, PatentName, base_category.BaseName, region_category.RegionName, function_category.FunctionName,\
                                  user_info.TrueName, AuditDate, patent_state.StateName \
                           from patent_info \
                                INNER JOIN patent_state ON patent_info.PatentStatus=patent_state.id\
                                INNER JOIN user_info ON patent_info.IDCard=user_info.IDCard \
                                INNER JOIN base_category ON patent_info.BaseCategory=base_category.id \
                                INNER JOIN region_category ON patent_info.RegionCategory=region_category.id \
                                INNER JOIN function_category ON patent_info.FunctionCategory=function_category.id \
                                where patent_info.PatentStatus='4' and patent_state.id='4' and patent_info.PatentName like CONCAT('%%',%s,'%%')\
                                     or (AuditDate between %s and %s) limit %s,%s"
            else:
                sql = "select PatentID, PatentName, base_category.BaseName, region_category.RegionName, function_category.FunctionName,\
                                  user_info.TrueName, AuditDate, patent_state.StateName \
                           from patent_info \
                                INNER JOIN patent_state ON patent_info.PatentStatus=patent_state.id\
                                INNER JOIN user_info ON patent_info.IDCard=user_info.IDCard \
                                INNER JOIN base_category ON patent_info.BaseCategory=base_category.id \
                                INNER JOIN region_category ON patent_info.RegionCategory=region_category.id \
                                INNER JOIN function_category ON patent_info.FunctionCategory=function_category.id \
                                where patent_info.PatentStatus='4' and patent_state.id='4' and patent_info.PatentName like CONCAT('%%',%s,'%%')\
                                     and (AuditDate between %s and %s) limit %s,%s"
        elif label_value2 == '地域类别':
            if label_value3 == None:
                sql = "select PatentID, PatentName, base_category.BaseName, region_category.RegionName, function_category.FunctionName,\
                                  user_info.TrueName, AuditDate, patent_state.StateName \
                           from patent_info \
                                INNER JOIN patent_state ON patent_info.PatentStatus=patent_state.id\
                                INNER JOIN user_info ON patent_info.IDCard=user_info.IDCard \
                                INNER JOIN base_category ON patent_info.BaseCategory=base_category.id \
                                INNER JOIN region_category ON patent_info.RegionCategory=region_category.id \
                                INNER JOIN function_category ON patent_info.FunctionCategory=function_category.id \
                                where patent_info.PatentStatus='4' and patent_state.id='4' and region_category.RegionName like CONCAT('%%',%s,'%%')\
                                     or (AuditDate between %s and %s) limit %s,%s"
            else:
                sql = "select PatentID, PatentName, base_category.BaseName, region_category.RegionName, function_category.FunctionName,\
                                  user_info.TrueName, AuditDate, patent_state.StateName \
                           from patent_info \
                                INNER JOIN patent_state ON patent_info.PatentStatus=patent_state.id\
                                INNER JOIN user_info ON patent_info.IDCard=user_info.IDCard \
                                INNER JOIN base_category ON patent_info.BaseCategory=base_category.id \
                                INNER JOIN region_category ON patent_info.RegionCategory=region_category.id \
                                INNER JOIN function_category ON patent_info.FunctionCategory=function_category.id \
                                where patent_info.PatentStatus='4' and patent_state.id='4' and region_category.RegionName like CONCAT('%%',%s,'%%')\
                                     and (AuditDate between %s and %s) limit %s,%s"
        elif label_value2 == '专利类型':
            if label_value3 == None:
                sql = "select PatentID, PatentName, base_category.BaseName, region_category.RegionName, function_category.FunctionName,\
                                  user_info.TrueName, AuditDate, patent_state.StateName \
                           from patent_info \
                                INNER JOIN patent_state ON patent_info.PatentStatus=patent_state.id\
                                INNER JOIN user_info ON patent_info.IDCard=user_info.IDCard \
                                INNER JOIN base_category ON patent_info.BaseCategory=base_category.id \
                                INNER JOIN region_category ON patent_info.RegionCategory=region_category.id \
                                INNER JOIN function_category ON patent_info.FunctionCategory=function_category.id \
                                where patent_info.PatentStatus='4' and patent_state.id='4' and function_category.FunctionName like CONCAT('%%',%s,'%%')\
                                     or (AuditDate between %s and %s) limit %s,%s"
            else:
                sql = "select PatentID, PatentName, base_category.BaseName, region_category.RegionName, function_category.FunctionName,\
                                  user_info.TrueName, AuditDate, patent_state.StateName \
                           from patent_info \
                                INNER JOIN patent_state ON patent_info.PatentStatus=patent_state.id\
                                INNER JOIN user_info ON patent_info.IDCard=user_info.IDCard \
                                INNER JOIN base_category ON patent_info.BaseCategory=base_category.id \
                                INNER JOIN region_category ON patent_info.RegionCategory=region_category.id \
                                INNER JOIN function_category ON patent_info.FunctionCategory=function_category.id \
                                where patent_info.PatentStatus='4' and patent_state.id='4' and function_category.FunctionName like CONCAT('%%',%s,'%%') \
                                   and (AuditDate between %s and %s) limit %s,%s"
        elif label_value2 == '基础类别':
            if label_value3 == None:
                sql = "select PatentID, PatentName, base_category.BaseName, region_category.RegionName, function_category.FunctionName,\
                                  user_info.TrueName, AuditDate, patent_state.StateName \
                           from patent_info \
                                INNER JOIN patent_state ON patent_info.PatentStatus=patent_state.id\
                                INNER JOIN user_info ON patent_info.IDCard=user_info.IDCard \
                                INNER JOIN base_category ON patent_info.BaseCategory=base_category.id \
                                INNER JOIN region_category ON patent_info.RegionCategory=region_category.id \
                                INNER JOIN function_category ON patent_info.FunctionCategory=function_category.id \
                                where patent_info.PatentStatus='4' and patent_state.id='4' and base_category.BaseName like CONCAT('%%',%s,'%%') \
                                   or (AuditDate between %s and %s) limit %s,%s"
            else:
                sql = "select PatentID, PatentName, base_category.BaseName, region_category.RegionName, function_category.FunctionName,\
                                  user_info.TrueName, AuditDate, patent_state.StateName \
                           from patent_info \
                                INNER JOIN patent_state ON patent_info.PatentStatus=patent_state.id\
                                INNER JOIN user_info ON patent_info.IDCard=user_info.IDCard \
                                INNER JOIN base_category ON patent_info.BaseCategory=base_category.id \
                                INNER JOIN region_category ON patent_info.RegionCategory=region_category.id \
                                INNER JOIN function_category ON patent_info.FunctionCategory=function_category.id \
                                where patent_info.PatentStatus='4' and patent_state.id='4' and base_category.BaseName like CONCAT('%%',%s,'%%') \
                                   and (AuditDate between %s and %s) limit %s,%s"
        elif label_value2 == '专利状态':
            if label_value3 == None:
                sql = "select PatentID, PatentName, base_category.BaseName, region_category.RegionName, function_category.FunctionName,\
                                  user_info.TrueName, AuditDate, patent_state.StateName \
                           from patent_info \
                                INNER JOIN patent_state ON patent_info.PatentStatus=patent_state.id\
                                INNER JOIN user_info ON patent_info.IDCard=user_info.IDCard \
                                INNER JOIN base_category ON patent_info.BaseCategory=base_category.id \
                                INNER JOIN region_category ON patent_info.RegionCategory=region_category.id \
                                INNER JOIN function_category ON patent_info.FunctionCategory=function_category.id \
                                where patent_info.PatentStatus='4' and patent_state.id='4' and patent_state.StateName like CONCAT('%%',%s,'%%') \
                                   or (AuditDate between %s and %s) limit %s,%s"
            else:
                sql = "select PatentID, PatentName, base_category.BaseName, region_category.RegionName, function_category.FunctionName,\
                                  user_info.TrueName, AuditDate, patent_state.StateName \
                           from patent_info \
                                INNER JOIN patent_state ON patent_info.PatentStatus=patent_state.id\
                                INNER JOIN user_info ON patent_info.IDCard=user_info.IDCard \
                                INNER JOIN base_category ON patent_info.BaseCategory=base_category.id \
                                INNER JOIN region_category ON patent_info.RegionCategory=region_category.id \
                                INNER JOIN function_category ON patent_info.FunctionCategory=function_category.id \
                                where patent_info.PatentStatus='4' and patent_state.id='4' and patent_state.StateName like CONCAT('%%',%s,'%%') \
                                   and (AuditDate between %s and %s) limit %s,%s"
        try:
            param = (label_value, label_value3, label_value4, startRow, pageSize)
            datas = self.dbhelper.SelectRecord(sql, param)
            return datas
        except Exception as e:
            print("查询记录失败:", e)

    # 用户分页查询专利信息使用
    def UserGetCount(self, state=1, label_value=None, label_value2=None, label_value3=None, label_value4=None):
        sql = ""
        if state == 1:  # 用户查询专利信息使用
            sql = "select count(*) from patent_info INNER JOIN patent_state ON patent_info.PatentStatus=patent_state.id \
                       where patent_state.id='4'"
        elif label_value2 == '申请人姓名':
            if label_value3 == None:
                sql = "select count(*) from patent_info INNER JOIN user_info ON patent_info.IDCard=user_info.IDCard where user_info.TrueName like CONCAT('%%',%s,'%%') and PatentStatus='4' or (AuditDate between %s and %s)"
            else:
                sql = "select count(*) from patent_info INNER JOIN user_info ON patent_info.IDCard=user_info.IDCard where user_info.TrueName like CONCAT('%%',%s,'%%') and PatentStatus='4' and (AuditDate between %s and %s)"
        elif label_value2 == '专利名称':
            if label_value3 == None:
                sql = "select count(*) from patent_info where PatentName like CONCAT('%%',%s,'%%') and PatentStatus='4' or (AuditDate between %s and %s)"
            else:
                sql = "select count(*) from patent_info where PatentName like CONCAT('%%',%s,'%%') and PatentStatus='4' and (AuditDate between %s and %s)"
        elif label_value2 == '地域类别':
            if label_value3 == None:
                sql = "select count(*) from patent_info INNER JOIN region_category ON patent_info.RegionCategory=region_category.id \
                           where region_category.RegionName like CONCAT('%%',%s,'%%') and patent_info.PatentStatus='4' or (AuditDate between %s and %s) "
            else:
                sql = "select count(*) from patent_info INNER JOIN region_category ON patent_info.RegionCategory=region_category.id \
                           where region_category.RegionName like CONCAT('%%',%s,'%%') and patent_info.PatentStatus='4' and (AuditDate between %s and %s) "
        elif label_value2 == '专利类型':
            if label_value3 == None:
                sql = "select count(*) from patent_info INNER JOIN function_category ON patent_info.FunctionCategory=function_category.id \
                           where function_category.FunctionName like CONCAT('%%',%s,'%%') and patent_info.PatentStatus='4' or (AuditDate between %s and %s) "
            else:
                sql = "select count(*) from patent_info INNER JOIN function_category ON patent_info.FunctionCategory=function_category.id \
                           where function_category.FunctionName like CONCAT('%%',%s,'%%') and patent_info.PatentStatus='4' and (AuditDate between %s and %s)"
        elif label_value2 == '基础类别':
            if label_value3 == None:
                sql = "select count(*) from patent_info INNER JOIN base_category ON patent_info.BaseCategory=base_category.id \
                           where base_category.BaseName like CONCAT('%%',%s,'%%') and patent_info.PatentStatus='4' or (AuditDate between %s and %s)"
            else:
                sql = "select count(*) from patent_info INNER JOIN base_category ON patent_info.BaseCategory=base_category.id \
                           where base_category.BaseName like CONCAT('%%',%s,'%%') and patent_info.PatentStatus='4' and (AuditDate between %s and %s)"
        elif label_value2 == '专利状态':
            if label_value3 == None:
                sql = "select count(*) from patent_info INNER JOIN patent_state ON patent_info.PatentStatus=patent_state.id \
                          where patent_state.StateName like CONCAT('%%',%s,'%%') and patent_info.PatentStatus='4' or (AuditDate between %s and %s)"
            else:
                sql = "select count(*) from patent_info INNER JOIN patent_state ON patent_info.PatentStatus=patent_state.id \
                          where patent_state.StateName like CONCAT('%%',%s,'%%') and patent_info.PatentStatus='4' and (AuditDate between %s and %s)"
        elif label_value2 == '未选择':
            sql = "select count(*) from patent_info INNER JOIN patent_state ON patent_info.PatentStatus=patent_state.id \
                      where patent_info.PatentStatus='4' and (AuditDate between %s and %s)"
        try:
            if state == 1:
                param = ()
                datas = self.dbhelper.SelectRecord(sql, param)
            elif label_value2 == '未选择':
                param = (label_value3, label_value4)
                datas = self.dbhelper.SelectRecord(sql, param)
            else:
                param = (label_value, label_value3, label_value4)
                datas = self.dbhelper.SelectRecord(sql, param)
            return datas
        except Exception as e:
            print("查询记录失败:", e)

    # 退出
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
