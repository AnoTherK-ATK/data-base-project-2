import pandas as pd
import random as rd
from git import Repo
import os
import shutil
import stat
from subprocess import call, run
import json
from getpass import getpass

# Function for delete folder
def on_rm_error(func, path, exc_info):
    # Is the error an access error?
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise
    
# List to save some data for table hoc
schoolId = []
studentID = {}

# Generate school
def generateSchool(s1, s2):
    with pd.ExcelFile("resources/school.xlsx") as xlsx:
        df = pd.read_excel("resources/school.xlsx")
    
        # Shuffle data in excel file
        for col in df.columns:
            df[col] = df[col].sample(frac=1).reset_index(drop=True)
        
        # Write query
        for index, row in df.iterrows():
            schoolId.append(row["ma_truong"])
            s1.write("INSERT INTO truong VALUES (\"{}\", \"{}\", \"{}\");\n".format(row["ma_truong"], row["ten_truong"], row["dia_chi"]))
            s2.write("INSERT INTO truong VALUES (\"{}\", \"{}\", \"{}\");\n".format(row["ma_truong"], row["ten_truong"], row["dia_chi"]))
            
def maxDayMonth(n, y):
    a = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if(n != 2):
        return a[n - 1]
    else:
        if (y % 4 == 0) and (y % 100):
            return 29
        elif(y % 400 == 0):
            return 29
        else:
            return 28
        
        
def generateStudent(s1, s2):
    boy = []
    girl = []
    sur = []
    district = []
    ward = []
    street = []
    with open("resources/boy.txt", "r", encoding = "utf-8") as b, open("resources/girl.txt", "r", encoding = "utf-8") as g, open("resources/surnames.txt", "r", encoding = "utf-8") as su:
        # Read data from file to random later
        s = b.read()
        boy = [ss for ss in s.split()]
        s = g.read()
        girl = [ss for ss in s.split()]
        s = su.read()
        sur = [ss for ss in s.split()]
    with open("resources/address.json", "r", encoding = "utf-8") as f:
        data = json.load(f)
        for ds in data["district"]:
            district.append((ds["pre"] + ' ' + ds["name"]).strip())
            for ws in ds["ward"]:
                ward.append(ws["pre"] + ' ' + ws["name"])
            for st in ds["street"]:
                street.append(st)
    
    # Shuffle data
    rd.shuffle(boy)
    rd.shuffle(girl)
    rd.shuffle(sur)
    rd.shuffle(district)
    rd.shuffle(ward)
    rd.shuffle(street)
    IDList = {}
    
    # write query
    for batch in range(10):
        print(batch)
        hsQuery = "INSERT INTO hs VALUES"
        hocQuery = "INSERT INTO hoc VALUES"
        for i in range(10):
            if(i != 0):
                hsQuery += ", "
                hocQuery += ", "
            
            # Name
            familyName = rd.choice(sur)
            gender = 0
            if(i % 2 == 0):
                firstName = rd.choice(boy)
                gender = 2
            else:
                firstName = rd.choice(girl)
                gender = 3
                
            # Date of birth
            year = rd.randint(2000, 2008)
            month = rd.randint(1, 12)
            day = rd.randint(1, maxDayMonth(month, year))
            date = str(year) + '-' + str(month).zfill(2) + '-' + str(day).zfill(2)
            
            # Citizen ID
            cccd = "NULL"
            if(2023 - year >= 15):
                cccdPrefix = str(rd.randint(1,99)).zfill(3) + str(gender) + str(year % 100).zfill(2)
                if(cccdPrefix not in IDList):
                    IDList[cccdPrefix] = 0
                IDList[cccdPrefix] += 1
                cccd = cccdPrefix + str(IDList[cccdPrefix]).zfill(6)
                
            #Student ID
            schId = rd.randint(0, len(schoolId) - 1)
            mahsPrefix = str((year % 100 + 15)) + str(schId).zfill(3)
            if(mahsPrefix not in studentID):
                studentID[mahsPrefix] = 0
            studentID[mahsPrefix] += 1
            mahs = mahsPrefix + str(studentID[mahsPrefix]).zfill(7)
            
            #Address
            numberAdrress = ""
            for j in range(rd.randint(0, 2)):
                if(j == 1):
                    numberAdrress += '/'
                numberAdrress += str(rd.randint(1, 1000))
                             
            address = numberAdrress + ' ' + rd.choice(street) + ' ' + rd.choice(ward) + ' ' + rd.choice(district) + " Thành phố Hồ Chí Minh"
                
            # HS(MAHS, HO, TEN, CCCD, NTNS, DCHI_HS)
            if(2023 - year >= 15):
                hsQuery += "(\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\")".format(mahs, familyName, firstName, cccd, date, address)
            else:
                hsQuery += "(\"{}\", \"{}\", \"{}\", NULL, \"{}\", \"{}\");\n".format(mahs, familyName, firstName, date, address)
            
            countHoc = rd.randint(1, min(3, max(1, 2023 - (year + 15))))
            for j in range(countHoc):
                if(j != 0):
                    hocQuery += ", "
                #Score and etc.
                score = rd.random() * 10
                if(score < 6):
                    score += rd.random() * 4
                #score = 6
                # HOC(MATR, MAHS, NAMHOC, DIEMTB, XEPLOAI, KQUA)
                hocQuery += "(\"{}\", \"{}\", \"{}\", {:.2f}, NULL, NULL)".format(schoolId[schId], mahs, str(year + 15 + j) + " - " + str(year + 16 + j), score)

        # Write to .sql file
        s1.write(hsQuery + ";\n")
        s1.write(hocQuery + ";\n")
        s2.write(hsQuery + ";\n")
        s2.write(hocQuery + ";\n")
#delete Resources folder
def deleteGit(dir):
    for i in os.listdir(dir):
        if i.endswith('git'):
            tmp = os.path.join(dir, i)
            # We want to unhide the .git folder before unlinking it.
            while True:
                call(['attrib', '-H', tmp])
                break
            shutil.rmtree(tmp, onerror=on_rm_error)


# Download resources
if os.path.exists("resources"):
    resourcesPath = os.path.join(os.getcwd() ,"resources")
    deleteGit(resourcesPath)
    shutil.rmtree(resourcesPath, onerror = on_rm_error)
Repo.clone_from("https://github.com/AnoTherK-ATK/database-project-resources.git", "resources")

# Write query to .sql file
if not os.path.exists("result"):
    os.makedirs("result")

# Generate school to table truong
with open("result/truonghoc1.sql", "w", encoding = "utf-8") as s1, open("result/truonghoc2.sql", "w", encoding = "utf-8") as s2:
    s1.write("USE truonghoc1;\n")
    s2.write("USE truonghoc2;\n")
    generateSchool(s1, s2)

# Generate student to table hs
with open("result/hoc1.sql", "w", encoding = "utf-8") as s1, open("result/hoc2.sql", "w", encoding = "utf-8") as s2:
    s1.write("USE truonghoc1;\n")
    s2.write("USE truonghoc2;\n")
    generateStudent(s1, s2)

# Run commands
username = input("Please enter your mySQL username: ")
password = getpass(prompt="Please enter your mySQL password: ")
run(['mysql', '-u' + username, '-p' + password + '<' + os.getcwd().replace('\\', '/') + '/result/truonghoc1.sql'], shell=True)
run(['mysql', '-u' + username, '-p' + password + '<' + os.getcwd().replace('\\', '/') + '/result/truonghoc2.sql'], shell=True)
run(['mysql', '-u' + username, '-p' + password + '<' + os.getcwd().replace('\\', '/') + '/result/hoc1.sql'], shell=True)
run(['mysql', '-u' + username, '-p' + password + '<' + os.getcwd().replace('\\', '/') + '/result/hoc2.sql'], shell=True)
