import wx
import wx.adv
import time
#
from patent import Patent


# 专利添加窗口页面总布局
class AddPatentFrame(wx.Frame):
    def __init__(self, parent, id, name, title, dbhelper):

        # 用来调用父窗口,便于更新
        self.eid = id
        self.mainframe = parent
        # 生成一个600*700的窗口
        wx.Frame.__init__(self, parent, title=title, size=(600, 700),
                          style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX))
        # 需要用到的数据库接口
        self.dbhelper = dbhelper
        self.name = name
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
        # Wx.FlexiGridSizer(rows, cols, vgap, hgap)  # 11行,2列,垂直间距,水平间距
        fgs = wx.FlexGridSizer(11, 2, 10, 10)
        # 十一个编辑框,分别用来编辑专利编号,专利名称,功能描述,基础类别,地域类别,功能类别相关信息
        patentName_tip = wx.StaticText(self.panel, label="专利名称:")
        fun_info_tip = wx.StaticText(self.panel, label="功能描述:")
        baseclass_tip = wx.StaticText(self.panel, label="基础类别:")
        areaclass_tip = wx.StaticText(self.panel, label="地域类别:")
        funclass_tip = wx.StaticText(self.panel, label="专利类型:")
        appName_tip = wx.StaticText(self.panel, label="申请人姓名:")
        appID_tip = wx.StaticText(self.panel, label="申请人身份证号:")
        #
        patentName_text = wx.TextCtrl(self.panel)
        fun_info_text = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE)
        baseclass_text = wx.ComboBox(self.panel, -1, choices=self.mainframe.data_translate((), 1), style=wx.CB_READONLY)
        areaclass_text = wx.ComboBox(self.panel, -1, choices=self.mainframe.data_translate((), 2), style=wx.CB_READONLY)
        funclass_text = wx.ComboBox(self.panel, -1, choices=self.mainframe.data_translate((), 3), style=wx.CB_READONLY)
        appName_text = wx.TextCtrl(self.panel, -1, value=self.name)
        appID_text = wx.TextCtrl(self.panel, -1, value=self.eid)
        appName_text.SetEditable(False)
        appID_text.SetEditable(False)
        #
        self.PatentName = patentName_text
        self.PatentFunctional = fun_info_text
        self.BaseClass = baseclass_text
        self.RegionalCategory = areaclass_text
        self.FunctionCategory = funclass_text
        self.ApplicantName = appName_text
        self.ApplicantID = appID_text
        #
        fgs.AddMany([(patentName_tip), (patentName_text, 1, wx.EXPAND),
                     (fun_info_tip, 1, wx.EXPAND), (fun_info_text, 1, wx.EXPAND),
                     (baseclass_tip), (baseclass_text, 1, wx.EXPAND),
                     (areaclass_tip), (areaclass_text, 1, wx.EXPAND),
                     (funclass_tip), (funclass_text, 1, wx.EXPAND),
                     (appName_tip), (appName_text, 1, wx.EXPAND),
                     (appID_tip), (appID_text, 1, wx.EXPAND),
                     ])
        fgs.AddGrowableRow(1, 1)  # 控制第三行的proportion增长
        fgs.AddGrowableCol(1, 1)  # 控制第二列的proportion增长
        #
        hbox.Add(fgs, proportion=2, flag=wx.ALL | wx.EXPAND, border=10)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        # 设置按钮
        save_button = wx.Button(self.panel, label="保  存", size=(100, 40))
        cancel_button = wx.Button(self.panel, label="取  消", size=(100, 40))
        # 绑定单击事件
        self.Bind(wx.EVT_BUTTON, self.savePatent, save_button)
        self.Bind(wx.EVT_BUTTON, self.CancelButton, cancel_button)
        hbox1.Add(save_button, flag=wx.ALL, border=10)
        hbox1.Add(cancel_button, flag=wx.ALL, border=10)

        #
        self.vbox.Add(hbox, proportion=1, flag=wx.ALL | wx.EXPAND)
        self.vbox.Add(hbox1, flag=wx.ALL | wx.CENTER)
        self.panel.SetSizer(self.vbox)

    def savePatent(self, evt):
        '''第一步：获取text中文本；第二步，连接数据库；第三步插入并获得主键；第四步添加到ListCtrl中'''
        patentName = self.PatentName.GetValue()
        fun_info = self.PatentFunctional.GetValue()
        baseclass = self.mainframe.data_translate(self.BaseClass.GetValue(), 1)
        areaclass = self.mainframe.data_translate(self.RegionalCategory.GetValue(), 2)
        funclass = self.mainframe.data_translate(self.FunctionCategory.GetValue(), 3)
        appName = self.ApplicantName.GetValue()
        appID = self.ApplicantID.GetValue()
        # 获取当前时间
        appdate = self.datetime_to_str(time.time())

        print("专利名称:" + str(patentName))
        if patentName == "" or fun_info == "" or baseclass == None or areaclass == None or funclass == None:
            # 消息对话框
            warn = wx.MessageDialog(self, message="所有信息不能为空！！！", caption="温馨提示", style=wx.OK | wx.ICON_INFORMATION)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return
        elif len(fun_info) > 500:
            # 消息对话框
            warn = wx.MessageDialog(self, message="功能描述超出字数范围，请把字数控制在255字以内", caption="温馨提示",
                                    style=wx.OK | wx.ICON_INFORMATION)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
        else:
            # 对Patent进行实例化
            patent = Patent('', patentName, fun_info, baseclass, areaclass, funclass, appName, appID,
                            appdate, '', '', '1')
            # 判断专利名称是否重复
            try:
                param_1 = (patentName,)
                sql_1 = "select PatentName from patent_info where PatentName=%s"
                i = self.dbhelper.SelectRecord(sql_1, param_1)
                if i != ():
                    if i[0][0] == patentName:
                        warn = wx.MessageDialog(self, message="专利名称已存在，请重新输入", caption="温馨提示",
                                                style=wx.OK | wx.ICON_INFORMATION)
                        warn.ShowModal()  # 提示
                        warn.Destroy()
                else:
                    # 进行数据库添加
                    try:
                        param_2 = (patent.getPatentName(), patent.getPatentFunctional(),
                                   patent.getBaseClass(), patent.getRegionalCategory(), patent.getFunctionCategory(),
                                   patent.getApplicantID(), patent.getApplicationDate(), patent.getpatentstate())
                        sql_2 = "insert into patent_info(PatentName, PatentFunction, BaseCategory, RegionCategory, FunctionCategory,\
                                       IDCard, ModifyDate, PatentStatus) values(%s,%s,%s,%s,%s,%s,%s,%s)"
                        self.dbhelper.AddRecord(sql_2, param_2)
                        # 通过新添加的专利名称得到专利编号
                        param_3 = (patentName,)
                        sql_3 = "select PatentID from patent_info where PatentName=%s"
                        patentid = self.dbhelper.SelectRecord(sql_3, param_3)[0][0]
                        # 再进行列表添加
                        self.addToList(patentid, '保存')  # 加一个专利状态变量，设为保存，修改这个函数
                        warn = wx.MessageDialog(self, message="专利添加成功", caption="温馨提示",
                                                style=wx.OK | wx.ICON_INFORMATION)
                        warn.ShowModal()  # 提示
                        warn.Destroy()
                        self.Destroy()  # 销毁隐藏Dialog
                    except Exception as e:
                        print("添加记录失败:", e)
            except Exception as e:
                print("查询记录失败:", e)

    # 向列表插入新添加的专利信息
    def addToList(self, patentid, patentstate):
        index = self.mainframe.list.InsertItem(self.mainframe.list.GetItemCount(), str(patentid))
        self.mainframe.list.SetItem(index, 1, str(self.PatentName.GetValue()))
        self.mainframe.list.SetItem(index, 2, str(self.BaseClass.GetValue()))
        self.mainframe.list.SetItem(index, 3, str(self.RegionalCategory.GetValue()))
        self.mainframe.list.SetItem(index, 4, str(self.FunctionCategory.GetValue()))
        self.mainframe.list.SetItem(index, 5, str(self.ApplicantName.GetValue()))
        self.mainframe.list.SetItem(index, 6, '')
        self.mainframe.list.SetItem(index, 7, patentstate)

    # 时间格式转换
    def datetime_to_str(self, dateTime):
        nowTime = time.strftime('%Y-%m-%d', time.localtime(dateTime))
        return nowTime

    # 取消按钮
    def CancelButton(self, event):
        self.Destroy()  # 销毁隐藏Dialog


# 修改专利信息界面
class UpdatePatentFrame(wx.Frame):
    # 进行初始化
    def __init__(self, parent, title, select_id, dbhelper):
        # 用来调用父frame,便于更新
        self.mainframe = parent
        # 生成一个600*700的框
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
        changedate_tip = wx.StaticText(self.panel, label="上一次修改日期:")
        patentstatus_tip = wx.StaticText(self.panel, label="专利状态:")
        #
        patentID_text = wx.TextCtrl(self.panel)
        patentName_text = wx.TextCtrl(self.panel)
        fun_info_text = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE)
        baseclass_text = wx.ComboBox(self.panel, -1, choices=self.mainframe.data_translate((), 1), style=wx.CB_READONLY)
        areaclass_text = wx.ComboBox(self.panel, -1, choices=self.mainframe.data_translate((), 2), style=wx.CB_READONLY)
        funclass_text = wx.ComboBox(self.panel, -1, choices=self.mainframe.data_translate((), 3), style=wx.CB_READONLY)
        appName_text = wx.TextCtrl(self.panel)
        appID_text = wx.TextCtrl(self.panel)
        changedate_text = wx.TextCtrl(self.panel)
        patentstatus_text = wx.ComboBox(self.panel, -1, choices=[u'保存', u'已提交', u'审核未通过'], style=wx.CB_READONLY)
        #
        patentID_text.SetEditable(False)
        appName_text.SetEditable(False)
        appID_text.SetEditable(False)
        changedate_text.SetEditable(False)
        #
        self.PatentID = patentID_text
        self.PatentName = patentName_text
        self.PatentFunctional = fun_info_text
        self.BaseClass = baseclass_text
        self.RegionalCategory = areaclass_text
        self.FunctionCategory = funclass_text
        self.ApplicantName = appName_text
        self.ApplicantID = appID_text
        self.ChangeDate = changedate_text
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
                     (changedate_tip), (changedate_text, 1, wx.EXPAND),
                     (patentstatus_tip), (patentstatus_text, 1, wx.EXPAND)])
        fgs.AddGrowableRow(2, 1)  # 控制第三行的proportion增长
        fgs.AddGrowableCol(1, 1)  # 控制第二列的proportion增长
        #
        hbox.Add(fgs, proportion=2, flag=wx.ALL | wx.EXPAND, border=10)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        # 设置按钮
        save_button = wx.Button(self.panel, label="确  定", size=(100, 40))
        cancel_button = wx.Button(self.panel, label="取  消", size=(100, 40))
        # 绑定事件
        self.Bind(wx.EVT_BUTTON, self.saveUpdate, save_button)
        self.Bind(wx.EVT_BUTTON, self.CancelButton, cancel_button)
        hbox1.Add(save_button, flag=wx.ALL, border=10)
        hbox1.Add(cancel_button, flag=wx.ALL, border=10)
        #
        self.vbox.Add(hbox, proportion=1, flag=wx.ALL | wx.EXPAND)
        self.vbox.Add(hbox1, flag=wx.ALL | wx.CENTER)

        self.panel.SetSizer(self.vbox)

        # 选中的id和patentid
        self.select_id = select_id
        # 通过行号获取第0列的值,就是专利编号
        self.patentid = self.mainframe.list.GetItem(select_id, 0).Text

        self.showAllText()  # 展现所有的text原来取值

    def showAllText(self):
        '''显示专利原始信息'''
        data = self.getPatentInfo(self.patentid)  # 通过专利id获取专利信息

        self.PatentID.SetValue(str(data[0][0]))  # 设置值
        self.PatentName.SetValue(str(data[0][1]))  # 设置值
        self.PatentFunctional.SetValue(str(data[0][2]))
        self.BaseClass.SetValue(str(data[0][3]))
        self.RegionalCategory.SetValue(str(data[0][4]))
        self.FunctionCategory.SetValue(str(data[0][5]))
        self.ApplicantName.SetValue(str(data[0][6]))
        self.ApplicantID.SetValue(str(data[0][7]))
        self.ChangeDate.SetValue(str(data[0][8]))  # 设置日期
        self.patentstatus.SetValue(str(data[0][9]))

    # 修改专利信息并保存
    def saveUpdate(self, evt):
        '''保存修改后的值'''
        patentID = self.PatentID.GetValue()  # 获得修改后的值
        patentName = self.PatentName.GetValue()  # 获得修改后的值
        fun_info = self.PatentFunctional.GetValue()
        baseclass = self.mainframe.data_translate(self.BaseClass.GetValue(), 1)
        areaclass = self.mainframe.data_translate(self.RegionalCategory.GetValue(), 2)
        funclass = self.mainframe.data_translate(self.FunctionCategory.GetValue(), 3)
        appName = self.ApplicantName.GetValue()
        appID = self.ApplicantID.GetValue()
        #
        patentstate = self.mainframe.data_translate(self.patentstatus.GetValue(), 4)
        if patentstate == '2':
            self.submit_date = self.datetime_to_str(time.time())
        else:
            self.submit_date = None
        self.change_date = self.datetime_to_str(time.time())
        print("专利名称:" + str(patentName))
        if patentName == "" or fun_info == "" or baseclass == "" or areaclass == "" or funclass == "" or patentstate == "":
            warn = wx.MessageDialog(self, message="所有信息不能为空！！！", caption="温馨提示", style=wx.OK | wx.ICON_INFORMATION)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return
        elif len(fun_info) > 500:
            # 消息对话框
            warn = wx.MessageDialog(self, message="功能描述超出字数范围，请把字数控制在500字以内", caption="温馨提示",
                                    style=wx.OK | wx.ICON_INFORMATION)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return
        else:
            print("开始将修改后的数据保存到数据库中")
            patent = Patent(patentID, patentName, fun_info, baseclass, areaclass, funclass, appName, appID,
                            self.change_date, self.submit_date, '', patentstate)  # 将数据封装到patent对象中
            try:
                param = (patent.getPatentName(), patent.getPatentFunctional(),
                         patent.getBaseClass(), patent.getRegionalCategory(), patent.getFunctionCategory(),
                         patent.getApplicationDate(), patent.getPassTime(), patent.getpatentstate(),
                         self.patentid)
                sql_2 = "update patent_info set PatentName=%s, PatentFunction=%s, BaseCategory=%s, RegionCategory=%s, FunctionCategory=%s,\
                               ModifyDate=%s, SubmitDate=%s, PatentStatus=%s where patent_info.PatentID=%s"
                self.dbhelper.UpdateData(sql_2, param)

                # 将修改后的数据保存到页面列表
                # 通过专利号进行数据的修改,至于要添多少个数据,就由你的控件由多少列决定了
                self.mainframe.list.SetItem(self.select_id, 0, patentID)
                self.mainframe.list.SetItem(self.select_id, 1, patentName)
                self.mainframe.list.SetItem(self.select_id, 2, self.BaseClass.GetValue())
                self.mainframe.list.SetItem(self.select_id, 3, self.RegionalCategory.GetValue())
                self.mainframe.list.SetItem(self.select_id, 4, self.FunctionCategory.GetValue())
                self.mainframe.list.SetItem(self.select_id, 5, appName)
                self.mainframe.list.SetItem(self.select_id, 7, self.patentstatus.GetValue())
                #
                warn = wx.MessageDialog(self, message="专利修改成功", caption="温馨提示",
                                        style=wx.OK | wx.ICON_INFORMATION)
                warn.ShowModal()  # 提示
                warn.Destroy()
                self.CancelButton(0)
            except Exception as e:
                print("修改记录失败:", e)

    # 时间格式转换
    def datetime_to_str(self, dateTime):
        nowTime = time.strftime('%Y-%m-%d', time.localtime(dateTime))
        return nowTime

    def getPatentInfo(self, patentid):
        param = (patentid,)
        sql_1 = "select PatentID, PatentName, PatentFunction, base_category.BaseName, region_category.RegionName, function_category.FunctionName,\
                                                 user_info.TrueName, patent_info.IDCard, ModifyDate, patent_state.StateName \
                                          from patent_info \
                                               INNER JOIN patent_state ON patent_info.PatentStatus=patent_state.id\
                                               INNER JOIN user_info ON patent_info.IDCard=user_info.IDCard \
                                               INNER JOIN base_category ON patent_info.BaseCategory=base_category.id \
                                               INNER JOIN region_category ON patent_info.RegionCategory=region_category.id \
                                               INNER JOIN function_category ON patent_info.FunctionCategory=function_category.id \
                                               where patent_info.PatentID=%s"
        try:
            data = self.dbhelper.SelectRecord(sql_1, param)  # 通过专利id获取专利信息
            return data
        except Exception as e:
            print("查询记录失败:", e)

    # 取消按钮
    def CancelButton(self, event):
        self.Destroy()  # 销毁隐藏Dialog


# 个人专利信息界面
class OneManPatent(wx.Panel):
    def __init__(self, notebook, parent, user_state, true_name, eid, dbhelper):

        wx.Panel.__init__(self, notebook)
        # 需要用到的数据库接口
        self.dbhelper = dbhelper
        # 用来调用父frame,便于更新
        self.parent = parent
        self.panel = self
        # 得到身份证号和真实姓名
        self.Eid = eid
        self.userstate = user_state
        self.name = true_name
        font1 = wx.Font(pointSize=14, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL, underline=False)
        # 组合框设计
        self.label = wx.StaticText(self.panel, label="类型:", pos=(125, 35), size=(30, 25))
        languages = ['未选择', '专利名称', '专利类型', '基础类别', '地域类别', '专利状态']
        self.combo = wx.ComboBox(self.panel, value='未选择', choices=languages, pos=(180, 35), size=(150, 35), style=wx.CB_READONLY)
        # 输入框设计
        self.label1 = wx.StaticText(self.panel, label="关键字:", pos=(370, 35), size=(50, 25))
        self.label_text = wx.TextCtrl(self.panel, pos=(440, 35), size=(150, 25))
        # 申请时间
        self.label2 = wx.StaticText(self.panel, label="起始日期:", pos=(90, 65), size=(60, 25))
        self.label_text1 = wx.adv.DatePickerCtrl(self.panel, -1, pos=(180, 65), size=(150, 25),
                                                 style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY | wx.adv.DP_ALLOWNONE)
        # 截止时间
        self.label3 = wx.StaticText(self.panel, label="截止日期:", pos=(350, 65), size=(60, 25))
        self.label_text2 = wx.adv.DatePickerCtrl(self.panel, -1, pos=(440, 65), size=(150, 25),
                                                 style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY | wx.adv.DP_ALLOWNONE)
        # 查询按钮
        query_button = wx.Button(self.panel, label="查  询", pos=(640, 35), size=(100, 40), style=wx.BORDER_MASK)
        # 为按钮绑定相应事件函数
        self.Bind(wx.EVT_BUTTON, self.queryPatent, query_button)
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
        self.list.SetColumnWidth(4, 200)
        self.list.SetColumnWidth(5, 100)
        self.list.SetColumnWidth(6, 150)
        self.list.SetColumnWidth(7, 150)
        #  设置字体
        font2 = wx.Font(pointSize=13, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL, underline=False)
        self.list.SetFont(font2)
        # 定义一组按钮
        add_button = wx.Button(self.panel, label="添  加", pos=(150, 500), size=(100, 35), style=wx.BORDER_MASK)
        del_button = wx.Button(self.panel, label="删  除", pos=(300, 500), size=(100, 35), style=wx.BORDER_MASK)
        update_button = wx.Button(self.panel, label="修  改", pos=(450, 500), size=(100, 35), style=wx.BORDER_MASK)
        cancel_button = wx.Button(self.panel, label="退  出", pos=(1000, 500), size=(100, 35), style=wx.BORDER_MASK)
        #
        self.label.SetFont(font1)
        self.label1.SetFont(font1)
        self.label2.SetFont(font1)
        self.label3.SetFont(font1)
        query_button.SetFont(font1)
        add_button.SetFont(font1)
        cancel_button.SetFont(font1)
        del_button.SetFont(font1)
        update_button.SetFont(font1)
        # 为按钮绑定相应事件函数,第一个参数为默认参数,指明为按钮类事件,第二个为事件函数名,第三个为按钮名
        self.Bind(wx.EVT_BUTTON, self.addPatent, add_button)
        self.Bind(wx.EVT_BUTTON, self.delPatent, del_button)
        self.Bind(wx.EVT_BUTTON, self.updatePatent, update_button)
        self.Bind(wx.EVT_BUTTON, self.CancelButton, cancel_button)
        # 显示个人专利信息
        self.showPatent()

    def showPatent(self, label_value='', label_value3='', label_value1='', label_value2=''):
        # label_value:关键字，label_value1:起始申请日，label_value2:截止申请日，label_value3:类型
        '''显示原始信息'''
        if label_value == '' and label_value3 == '':
            datas = self.getAllPatentByeID()
        else:
            # 先清空列表
            for i in range(30):
                self.list.DeleteItem(0)
            # 通过输入的关键字和下拉框中的值来查询专利信息
            datas = self.UserGetPatentByValue(label_value, label_value3, label_value1, label_value2, self.Eid)

            if datas == ():
                warn = wx.MessageDialog(self, message="对不起，暂时没有查询到你想要的结果", caption="温馨提示",
                                        style=wx.OK | wx.ICON_INFORMATION)
                warn.ShowModal()  # 提示
                warn.Destroy()
        for data in datas:
            index = self.list.InsertItem(self.list.GetItemCount(), str(data[0]))
            self.list.SetItem(index, 1, str(data[1]))
            self.list.SetItem(index, 2, str(data[2]))
            self.list.SetItem(index, 3, str(data[3]))
            self.list.SetItem(index, 4, str(data[4]))
            self.list.SetItem(index, 5, str(data[5]))
            self.list.SetItem(index, 6, str(data[6]))
            self.list.SetItem(index, 7, str(data[7]))

    def addPatent(self, evt):
        '''添加专利按钮，弹出添加专利框'''
        if self.userstate == '待审核':
            warn = wx.MessageDialog(self, message="用户信息还在审核中，请耐心等待，由此给您造成的不便，请见谅", caption="温馨提示",
                                    style=wx.OK | wx.ICON_INFORMATION)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
        elif self.userstate == '审核未通过':
            warn = wx.MessageDialog(self, message="用户信息审核未通过，请完善您的用户信息", caption="温馨提示",
                                    style=wx.OK | wx.ICON_INFORMATION)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
        else:
            add_f = AddPatentFrame(self, self.Eid, self.name, "添加专利信息窗口", self.dbhelper)
            add_f.Show(True)

    def delPatent(self, evt):
        '''删除专利信息按钮，先选中,然后删除'''
        selectId = self.list.GetFirstSelected()  # 得到选中的行的id

        if selectId == -1:
            warn = wx.MessageDialog(self, message="未选中任何条目！！！", caption="温馨提示", style=wx.OK | wx.ICON_INFORMATION)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
        else:
            patentid = self.list.GetItem(selectId, 0).Text
            patentstate = self.list.GetItem(selectId, 7).Text
            if patentstate == "审核未通过" or patentstate == "保存":
                self.list.DeleteItem(selectId)  # 先在listctrl中删除选中行
                try:
                    param = (patentid,)
                    sql = "delete from patent_info where PatentID = %s"
                    self.dbhelper.DeleteRecord(sql, param)  # 然后再从数据库中删除
                    warn = wx.MessageDialog(self, message="编号为:" + str(patentid) + "专利信息删除成功", caption="温馨提示",
                                            style=wx.OK | wx.ICON_INFORMATION)
                    warn.ShowModal()  # 提示错误
                    warn.Destroy()
                except Exception as e:
                    print("查询记录失败:", e)
            else:
                warn = wx.MessageDialog(self, message="不能进行删除", caption="温馨提示", style=wx.OK | wx.ICON_INFORMATION)
                warn.ShowModal()  # 提示错误
                warn.Destroy()

    def updatePatent(self, evt):
        '''修改按钮响应事件，点击修改按钮，弹出修改框'''
        selectId = self.list.GetFirstSelected()  # 得到选中的行数
        if selectId == -1:
            warn = wx.MessageDialog(self, message="未选中任何条目！！！", caption="温馨提示", style=wx.OK | wx.ICON_INFORMATION)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
        elif selectId != -1:
            patentstate = self.list.GetItem(selectId, 7).Text
            if patentstate == '审核通过':
                dlg = wx.MessageDialog(self, message="审核通过的专利不能修改", caption="温馨提示", style=wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()  # 提示错误
            else:
                update_f = UpdatePatentFrame(self, "修改专利窗口", selectId, self.dbhelper)
                update_f.Show(True)

    # 查询专利信息
    def queryPatent(self, evt):
        '''查看按钮响应事件'''
        # 获取输入的值
        label_value = self.label_text.GetValue()
        label_value1 = self.label_text1.GetValue()  # 获取申请日期
        label_value2 = self.label_text2.GetValue()  # 获取截止日期
        label_value3 = self.combo.GetValue()
        if str(label_value1) != 'INVALID DateTime' and str(label_value2) != 'INVALID DateTime':
            # 时间格式转换
            start_time = self.datetime_to_str(str(label_value1))
            deadline = self.datetime_to_str(str(label_value2))
        else:
            start_time = None
            deadline = None
        # 判断
        if label_value3 != '未选择':
            if label_value == '' and start_time ==None and deadline == None:
                warn = wx.MessageDialog(self, message="未输入关键词！！！", caption="温馨提示", style=wx.OK | wx.ICON_INFORMATION)
                warn.ShowModal()  # 提示错误
                warn.Destroy()
            elif label_value == '' and start_time !=None and deadline != None:
                warn = wx.MessageDialog(self, message="未输入关键词！！！", caption="温馨提示", style=wx.OK | wx.ICON_INFORMATION)
                warn.ShowModal()  # 提示错误
                warn.Destroy()
            elif label_value != '' and start_time ==None and deadline == None:
                self.showPatent(label_value, label_value3, start_time, deadline)
            elif label_value != '' and start_time !=None and deadline != None:
                self.showPatent(label_value, label_value3, start_time, deadline)
        elif label_value3 == '未选择':
            if label_value != '' and start_time !=None and deadline != None:
                warn = wx.MessageDialog(self, message="请先进行类型选择！！！", caption="温馨提示", style=wx.OK | wx.ICON_INFORMATION)
                warn.ShowModal()  # 提示错误
                warn.Destroy()
            elif label_value != '' and start_time ==None and deadline == None:
                warn = wx.MessageDialog(self, message="请先进行类型选择！！！", caption="温馨提示", style=wx.OK | wx.ICON_INFORMATION)
                warn.ShowModal()  # 提示错误
                warn.Destroy()
            elif label_value == '' and start_time ==None and deadline == None:
                warn = wx.MessageDialog(self, message="请输入完整时间！！！", caption="温馨提示", style=wx.OK | wx.ICON_INFORMATION)
                warn.ShowModal()  # 提示错误
                warn.Destroy()
            elif label_value == '' and start_time !=None and deadline != None:
                self.showPatent(label_value, label_value3, start_time, deadline)

    # 时间格式转换
    def datetime_to_str(self, dateTime):
        # Python time strptime() 函数根据指定的格式把一个时间字符串解析为时间元组。
        tempTime = time.strptime(dateTime, '%a %b %d %H:%M:%S %Y')
        # Python time strftime() 函数接收以时间元组，并返回以可读字符串表示的当地时间，格式由参数format决定。
        resTime = time.strftime('%Y-%m-%d', tempTime)
        return resTime

    # 把字符串转换为数字
    def data_translate(self, data, i):
        param = (data,)
        data_list = []
        sql = ""
        sql_2 = ""
        if i == 1:
            sql = "select id from base_category where BaseName=%s"
            sql_2 = "select BaseName from base_category"
        elif i == 2:
            sql = "select id from region_category where RegionName=%s"
            sql_2 = "select RegionName from region_category"
        elif i == 3:
            sql = "select id from function_category where FunctionName=%s"
            sql_2 = "select FunctionName from function_category"
        elif i == 4:
            sql = "select id from patent_state where StateName=%s"
        try:
            if param[0] == ():
                param = ()
                net = self.dbhelper.SelectRecord(sql_2, param)
                for j in net:
                    data_list.append(j[0])
                return data_list
            else:
                net = self.dbhelper.SelectRecord(sql, param)
                return net[0][0]
        except Exception as e:
            print("转换数据失败:", e)

    # 用户查询自己的专利信息
    def UserGetPatentByValue(self, label_value, label_value2, label_value3, label_value4, eid):
        # 定义SQL语句
        sql = ""
        if label_value2 == '专利名称':
            if label_value3 == None:
                sql = "select PatentID, PatentName, base_category.BaseName, region_category.RegionName, function_category.FunctionName,\
                                  user_info.TrueName, AuditDate, patent_state.StateName \
                           from patent_info \
                                INNER JOIN patent_state ON patent_info.PatentStatus=patent_state.id\
                                INNER JOIN user_info ON patent_info.IDCard=user_info.IDCard \
                                INNER JOIN base_category ON patent_info.BaseCategory=base_category.id \
                                INNER JOIN region_category ON patent_info.RegionCategory=region_category.id \
                                INNER JOIN function_category ON patent_info.FunctionCategory=function_category.id \
                                where patent_info.PatentName like CONCAT('%%',%s,'%%') and patent_info.IDCard=%s or (AuditDate between %s and %s)"
            else:
                sql = "select PatentID, PatentName, base_category.BaseName, region_category.RegionName, function_category.FunctionName,\
                                  user_info.TrueName, AuditDate, patent_state.StateName \
                           from patent_info \
                                INNER JOIN patent_state ON patent_info.PatentStatus=patent_state.id\
                                INNER JOIN user_info ON patent_info.IDCard=user_info.IDCard \
                                INNER JOIN base_category ON patent_info.BaseCategory=base_category.id \
                                INNER JOIN region_category ON patent_info.RegionCategory=region_category.id \
                                INNER JOIN function_category ON patent_info.FunctionCategory=function_category.id \
                                where patent_info.PatentName like CONCAT('%%',%s,'%%') and patent_info.IDCard=%s and (AuditDate between %s and %s)"
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
                                where region_category.RegionName like CONCAT('%%',%s,'%%') and patent_info.IDCard=%s or (AuditDate between %s and %s)"
            else:
                sql = "select PatentID, PatentName, base_category.BaseName, region_category.RegionName, function_category.FunctionName,\
                                  user_info.TrueName, AuditDate, patent_state.StateName \
                           from patent_info \
                                INNER JOIN patent_state ON patent_info.PatentStatus=patent_state.id\
                                INNER JOIN user_info ON patent_info.IDCard=user_info.IDCard \
                                INNER JOIN base_category ON patent_info.BaseCategory=base_category.id \
                                INNER JOIN region_category ON patent_info.RegionCategory=region_category.id \
                                INNER JOIN function_category ON patent_info.FunctionCategory=function_category.id \
                                where region_category.RegionName like CONCAT('%%',%s,'%%') and patent_info.IDCard=%s and (AuditDate between %s and %s)"
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
                                where function_category.FunctionName like CONCAT('%%',%s,'%%') and patent_info.IDCard=%s or (AuditDate between %s and %s)"
            else:
                sql = "select PatentID, PatentName, base_category.BaseName, region_category.RegionName, function_category.FunctionName,\
                                  user_info.TrueName, AuditDate, patent_state.StateName \
                           from patent_info \
                                INNER JOIN patent_state ON patent_info.PatentStatus=patent_state.id\
                                INNER JOIN user_info ON patent_info.IDCard=user_info.IDCard \
                                INNER JOIN base_category ON patent_info.BaseCategory=base_category.id \
                                INNER JOIN region_category ON patent_info.RegionCategory=region_category.id \
                                INNER JOIN function_category ON patent_info.FunctionCategory=function_category.id \
                                where function_category.FunctionName like CONCAT('%%',%s,'%%') and patent_info.IDCard=%s and (AuditDate between %s and %s)"
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
                                where base_category.BaseName like CONCAT('%%',%s,'%%') and patent_info.IDCard=%s or (AuditDate between %s and %s)"
            else:
                sql = "select PatentID, PatentName, base_category.BaseName, region_category.RegionName, function_category.FunctionName,\
                                  user_info.TrueName, AuditDate, patent_state.StateName \
                           from patent_info \
                                INNER JOIN patent_state ON patent_info.PatentStatus=patent_state.id\
                                INNER JOIN user_info ON patent_info.IDCard=user_info.IDCard \
                                INNER JOIN base_category ON patent_info.BaseCategory=base_category.id \
                                INNER JOIN region_category ON patent_info.RegionCategory=region_category.id \
                                INNER JOIN function_category ON patent_info.FunctionCategory=function_category.id \
                                where base_category.BaseName like CONCAT('%%',%s,'%%') and patent_info.IDCard=%s and (AuditDate between %s and %s)"
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
                                where patent_state.StateName like CONCAT('%%',%s,'%%') and patent_info.IDCard=%s or (AuditDate between %s and %s)"
            else:
                sql = "select PatentID, PatentName, base_category.BaseName, region_category.RegionName, function_category.FunctionName,\
                                  user_info.TrueName, AuditDate, patent_state.StateName \
                           from patent_info \
                                INNER JOIN patent_state ON patent_info.PatentStatus=patent_state.id\
                                INNER JOIN user_info ON patent_info.IDCard=user_info.IDCard \
                                INNER JOIN base_category ON patent_info.BaseCategory=base_category.id \
                                INNER JOIN region_category ON patent_info.RegionCategory=region_category.id \
                                INNER JOIN function_category ON patent_info.FunctionCategory=function_category.id \
                                where patent_state.StateName like CONCAT('%%',%s,'%%') and patent_info.IDCard=%s and (AuditDate between %s and %s)"
        elif label_value2 == '未选择':
            sql = "select PatentID, PatentName, base_category.BaseName, region_category.RegionName, function_category.FunctionName,\
                              user_info.TrueName, AuditDate, patent_state.StateName \
                       from patent_info \
                            INNER JOIN patent_state ON patent_info.PatentStatus=patent_state.id\
                            INNER JOIN user_info ON patent_info.IDCard=user_info.IDCard \
                            INNER JOIN base_category ON patent_info.BaseCategory=base_category.id \
                            INNER JOIN region_category ON patent_info.RegionCategory=region_category.id \
                            INNER JOIN function_category ON patent_info.FunctionCategory=function_category.id \
                            where patent_state.StateName like CONCAT('%%',%s,'%%') and patent_info.IDCard=%s and (AuditDate between %s and %s)"
        try:
            param = (label_value, eid, label_value3, label_value4)
            datas = self.dbhelper.SelectRecord(sql, param)
            return datas
        except Exception as e:
            print("查询记录失败:", e)

    # 得到用户个人所有专利信息
    def getAllPatentByeID(self):
        sql = "select PatentID, PatentName, base_category.BaseName, region_category.RegionName, function_category.FunctionName,\
                                                      user_info.TrueName, AuditDate, patent_state.StateName \
                                               from patent_info \
                                                    INNER JOIN patent_state ON patent_info.PatentStatus=patent_state.id\
                                                    INNER JOIN user_info ON patent_info.IDCard=user_info.IDCard \
                                                    INNER JOIN base_category ON patent_info.BaseCategory=base_category.id \
                                                    INNER JOIN region_category ON patent_info.RegionCategory=region_category.id \
                                                    INNER JOIN function_category ON patent_info.FunctionCategory=function_category.id \
                                                    where patent_info.IDCard=%s"
        try:
            param = (self.Eid,)
            datas = self.dbhelper.SelectRecord(sql, param)
            return datas
        except Exception as e:
            print("查询记录失败:", e)

    # 退出此界面
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
