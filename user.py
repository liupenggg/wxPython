class UserInfo:
    '''一个申请人信息类，包括申请人身份证号，姓名，性别，出生日期，职业，毕业学校，
        学历/学位，单位，职称，手机号，QQ号，电子邮箱'''

    def __init__(self, UserName="", password="", ApplicantName="", ApplicantID="", gender="", birthday="", profession="",
                 graduationschool="", degree="", department="", zhicheng="", CellPhoneNumber="", QQ="", email=""):
        self.UserName = UserName  # 用户名
        self.password = password  # 登录密码
        self.ApplicantName = ApplicantName  # 姓名
        self.ApplicantID = ApplicantID  # 身份证号
        self.gender = gender  # 性别
        self.birthday = birthday  # 出生日期
        self.profession = profession  # 职业
        self.graduationschool = graduationschool  # 毕业学校
        self.degree = degree  # 学历/学位
        self.department = department  # 单位
        self.zhicheng = zhicheng  # 职称
        self.Phone = CellPhoneNumber  # 手机号
        self.QQ = QQ  # QQ号
        self.email = email  # 电子邮箱

    def setusername(self, userName):
        self.UserName = userName

    def getusername(self):
        return self.UserName

    def setPassword(self, password):
        self.password = password

    def getpassword(self):
        return self.password

    def setApplicantID(self, ID):
        self.ApplicantID = ID

    def getApplicantID(self):
        return self.ApplicantID

    def setApplicantName(self, name):
        self.ApplicantName = name

    def getApplicantName(self):
        return self.ApplicantName

    def setgender(self, sex):
        self.gender = sex

    def getgender(self):
        return self.gender

    def setbirthday(self, birth):
        self.birthday = birth

    def getbirthday(self):
        return self.birthday

    def setprofession(self, job):
        self.profession = job

    def getprofession(self):
        return self.profession

    def setgraduationschool(self, school):
        self.graduationschool = school

    def getgraduationschool(self):
        return self.graduationschool

    def setdegree(self, xuewei):
        self.degree = xuewei

    def getdegree(self):
        return self.degree

    def setdepartment(self, depart):
        self.department = depart

    def getdepartment(self):
        return self.department

    def setzhicheng(self, title):
        self.zhicheng = title

    def getzhicheng(self):
        return self.zhicheng

    def setCellPhoneNumber(self, phonenumber):
        self.Phone = phonenumber

    def getCellPhoneNumber(self):
        return self.Phone

    def setQQ(self, qq):
        self.QQ = qq

    def getQQ(self):
        return self.QQ

    def setemail(self, youxiang):
        self.email = youxiang

    def getemail(self):
        return self.email


if __name__ == "__main__":
    personer = UserInfo()
