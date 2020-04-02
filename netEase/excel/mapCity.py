import xlrd
import xlwt

city = ['南京',
        '北京',
        '西安',
        '济南',
        '天津',
        '郑州',
        '长春',
        '石家庄',
        '沈阳',
        '镇江',
        '武汉',
        '合肥',
        '成都',
        '长沙',
        '重庆']

# 打开文件，获取excel文件的workbook（工作簿）对象
# workbook = xlrd.open_workbook("C:/Users/lenovo/Desktop/demo.xlsx")
workbook = xlrd.open_workbook("E:/【汇总】汇总的2月计算明细表0331--ok.xlsx")

worksheet = workbook.sheet_by_index(0)
nrows = worksheet.nrows  # 获取该表总行数
# print(nrows)  # 32

ncols = worksheet.ncols  # 获取该表总列数
# print(ncols)  # 13

# for i in range(nrows):  # 循环打印每一行
#     print(worksheet.row_values(i))


# 创建一个sheet对象，一个sheet对象对应Excel文件中的一张表格。


for str in city:
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet('计算明细表', cell_overwrite_ok=True)
    w = 0
    for i in range(nrows):
        if i == 0:
            w += 1
            for j in range(ncols):
                sheet.write(i, j, worksheet.row_values(i)[j])
        else:
            if str == worksheet.row_values(i)[6]:
                for j in range(ncols):
                    sheet.write(w, j, worksheet.row_values(i)[j])
                w += 1
        if i % 1000 == 0:
            print("进度：" + (i / nrows*100).__str__()+"%")
        # print(worksheet.row_values(i))
        # s = worksheet.row_values(i)[0]
        # print(s)

    file = 'E:/excel/' + str + '.xls'
    print("完成" + file)
    book.save(file)
