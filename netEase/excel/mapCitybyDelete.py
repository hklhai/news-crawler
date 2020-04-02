from shutil import copyfile

import win32com.client
import xlrd

# city = [
#     '北京'
# ]

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
# source = 'C:/Users/lenovo/Desktop/demo.xlsx'
source = "E:/汇总的2月计算明细表0331.xlsx"

for str in city:
    copyfile(source, "E:/excel/" + str + ".xlsx")

cityMap = {}
workbook = xlrd.open_workbook(source)
worksheet = workbook.sheet_by_index(0)
nrows = worksheet.nrows  # 获取该表总行数
ncols = worksheet.ncols  # 获取该表总列数
for i in range(nrows):
    if i != 0:
        cityName = worksheet.row_values(i)[6]
        if cityMap.get(cityName) is None:
            cityMap[cityName] = [i]
        else:
            cityMap.get(cityName).append(i)

for str in city:
    try:
        xl = win32com.client.Dispatch('Excel.Application')
        wb = xl.Workbooks.Open("E:/excel/" + str + ".xlsx")
        sht = wb.Worksheets('Sheet1')
        list = cityMap.get(str)
        if list is None:
            continue
        else:
            for i in range(nrows - 1, -1, -1):
                if i == 0:
                    continue
                else:
                    if i in list:
                        continue
                    else:
                        sht.Rows(i + 1).Delete()
                        if i % 1000 == 0:
                            print(str + "-进度：" + ((nrows - i) / nrows * 100).__str__() + "%")
            wb.Close(True)
            print("完成: " + str)
    except Exception as e:
        print(e.message)
        if wb is not None:
            wb.Close(True)

if wb is not None:
    wb.Close(True)
