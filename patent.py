
class Patent:
    '''一个专利信息类，包括专利编号，名称，功能描述，基础类别，地域类别，功能类别，
        申请人身份证号，申请日期，通过日期，截止日期'''

    def __init__(self, Patentid="",PatentName="", PatentFunctional="", BaseClass="",
                 RegionalCategory="", FunctionCategory="", ApplicantName="",ApplicantID="",
                 ModifyTime="",SubmitTime="",AuditTime="",patentstate=""):
        self.PatentID = Patentid  # 专利编号
        self.PatentName = PatentName  # 专利名称
        self.PatentFunctional = PatentFunctional  # 功能描述
        self.BaseClass = BaseClass  # 基础类别
        self.RegionalCategory = RegionalCategory  # 地域类别
        self.FunctionCategory = FunctionCategory  # 功能类别
        self.ApplicantName = ApplicantName
        self.ApplicantID = ApplicantID  # 申请人身份证号
        self.ModifyTime = ModifyTime  # 修改时间
        self.SubmitTime = SubmitTime  # 提交时间
        self.AuditTime = AuditTime  # 审核时间
        self.patentstate = patentstate  # 专利状态

    def setPatentID(self, id):
        self.PatentID = id

    def getPatentID(self):
        return self.PatentID

    def setPatentName(self, Name):
        self.PatentName = Name

    def getPatentName(self):
        return self.PatentName

    def setPatentFunctional(self, fun):
        self.PatentFunctional = fun

    def getPatentFunctional(self):
        return self.PatentFunctional

    def setBaseClass(self, classes):
        self.BaseClass = classes

    def getBaseClass(self):
        return self.BaseClass

    def setRegionalCategory(self, category):
        self.RegionalCategory = category

    def getRegionalCategory(self):
        return self.RegionalCategory

    def setFunctionCategory(self, funcategory):
        self.FunctionCategory = funcategory

    def getFunctionCategory(self):
        return self.FunctionCategory

    def setApplicantName(self, appname):
        self.ApplicantName = appname

    def getApplicantName(self):
        return self.ApplicantName

    def setApplicantID(self, number):
        self.ApplicantID = number

    def getApplicantID(self):
        return self.ApplicantID

    def setApplicationDate(self, date):
        self.ModifyTime = date

    def getApplicationDate(self):
        return self.ModifyTime

    def setPassTime(self, passTime):
        self.SubmitTime = passTime

    def getPassTime(self):
        return self.SubmitTime

    def setDeadline(self, deadtime):
        self.AuditTime = deadtime

    def getDeadline(self):
        return self.AuditTime

    def setpatentstate(self, state):
        self.patentstate = state

    def getpatentstate(self):
        return self.patentstate


if __name__ == "__main__":
    patent = Patent()
