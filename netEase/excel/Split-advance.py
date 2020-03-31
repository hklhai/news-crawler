import xlrd

workbook = xlrd.open_workbook("C:/Users/lenovo/Desktop/河北建筑职业技术工程学院.xlsx")
worksheet = workbook.sheet_by_index(0)
for i in range(worksheet.nrows):  # 循环打印每一行
    s = worksheet.row_values(i)[0].split("-")
    print(s[len(s) - 1])
