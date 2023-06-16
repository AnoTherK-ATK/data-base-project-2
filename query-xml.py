import sys
import xml.etree.ElementTree as ET

tree = ET.parse(sys.argv[1])
lower_bound = float(sys.argv[2])
upper_bound = float(sys.argv[3])

xpath_expr = f".//Student"

matching_students = tree.findall(xpath_expr)

for student in matching_students:
    if (
        float(student.find("DiemTB").text) >= lower_bound
        and float(student.find("DiemTB").text) <= upper_bound
    ):
        print(student.find("HoTen").text)
        print(student.find("NTNS").text)
        print(student.find("DiemTB").text)
        print(student.find("XepLoai").text)
        print(student.find("Kqua").text)
        print()
