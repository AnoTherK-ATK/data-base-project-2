import sys
import mysql.connector as connector
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from getpass import getpass
import time
from tabulate import tabulate

# Check arguments
if len(sys.argv) < 6:
    print("Please provide enough argument")
    print("Argument format: python query-db.py <database> <schoolName> <year begin> <rank>")
    print("database: truonghoc1 (not creating index) or truonghoc2 (creating index)")
    print("schoolName: name of school include space in Vietnamese. For example: \"Trường THPT chuyên Lê Hồng Phong\"")
    print("year begin: year begin of school year 4 digits: 2019, 2020, ...")
    print("rank: rank of student in class (xs, g, k, tb, y) for (Xuất sắc, Giỏi, Khá, Trung bình, Yếu))")
    exit(1)

# Get arguments
dataBase = sys.argv[1]
schoolName = " ".join(sys.argv[2:-2])
year = int(sys.argv[-2])
rank = sys.argv[-1]
if(rank == "xs"):
    rank = "Xuất sắc"
elif(rank == "g"):
    rank = "Giỏi"
elif(rank == "k"):
    rank = "Khá"
elif(rank == "tb"):
    rank = "Trung bình"
else:
    rank = "Yếu"

# Connect to mySQL
username = input("Please enter your mySQL username: ")
password = getpass(prompt="Please enter your mySQL password: ")
cnx = connector.connect(user=username, password=password, host='localhost', database=dataBase)
cursor = cnx.cursor()

def query(q):
    start = time.perf_counter()
    cursor.execute(q)
    end = time.perf_counter()
    result = cursor.fetchall()
    
    table = tabulate(result, ["HoTen", "NTNS", "DiemTB", "XepLoai", "Kqua"], tablefmt="fancy_grid", stralign="center")
    print(table)
    print("Time to execute:", (end - start) * 1000, "ms")
    return result

SELECTquery = "SELECT DISTINCT CONCAT_WS(\" \", st.ho, st.ten) as ho_ten, st.ntns, stu.diemtb, stu.xeploai, stu.kqua"
FROMquery = "FROM hoc as stu, hs as st, truong as sc"
WHEREquery = "WHERE sc.tentr=\"{}\" AND sc.matr=stu.matr AND stu.namhoc=\"{}\" AND stu.xeploai=\"{}\" AND stu.mahs=st.mahs AND stu.matr=sc.matr".format(schoolName, str(year) + " - " + str(year + 1), rank)

result = query(SELECTquery + ' ' + FROMquery + ' ' + WHEREquery)

# Create XML tree structure
root = ET.Element("Results")
for row in result:
    student = ET.SubElement(root, "Student")
    ho_ten = ET.SubElement(student, "HoTen")
    ho_ten.text = row[0]
    ntns = ET.SubElement(student, "NTNS")
    ntns.text = str(row[1])
    diemtb = ET.SubElement(student, "DiemTB")
    diemtb.text = str(row[2])
    xeploai = ET.SubElement(student, "XepLoai")
    xeploai.text = row[3]
    kqua = ET.SubElement(student, "Kqua")
    kqua.text = row[4]

# Create XML tree
tree = ET.ElementTree(root)

# Save XML tree to a file
schoolName = schoolName.replace(' ', '')
rank = rank.replace(' ', '')
xml_file = "XML/{}-{}-{}-{}.xml".format(dataBase, schoolName, year, rank)
f = open(xml_file, "wb")
tree.write(xml_file, encoding="utf-8", xml_declaration=True)

# Beautify XML
dom = minidom.parse(xml_file)
beautified_xml = dom.toprettyxml(indent=' ', encoding="utf-8")
f.write(beautified_xml)


print("Query results saved to", xml_file)
