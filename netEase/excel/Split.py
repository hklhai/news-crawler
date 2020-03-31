import xlrd

# 打开文件，获取excel文件的workbook（工作簿）对象
workbook = xlrd.open_workbook("C:/Users/lenovo/Desktop/河北建筑职业技术工程学院.xlsx")

worksheet = workbook.sheet_by_index(0)
nrows = worksheet.nrows  # 获取该表总行数
# print(nrows)  # 32

ncols = worksheet.ncols  # 获取该表总列数
# print(ncols)  # 13

for i in range(nrows):  # 循环打印每一行
    # print(worksheet.row_values(i))
    s = worksheet.row_values(i)[0].split("-")
    o = s[len(s) - 1]
    print(o)
