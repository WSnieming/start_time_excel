from openpyxl.chart import Reference, BarChart
from openpyxl.workbook import Workbook

wb = Workbook()
ws = wb.active

# 写入一列数数据
for i in range(10):
    ws.append([i])

print(ws)
exit()
values = Reference(ws, min_col=1, min_row=1, max_col=1, max_row=10)  # 选择图表的数据源
chart = BarChart()  # 创建一个BarChart对象
chart.add_data(values)  # 给BarChart对象添加数据源
ws.add_chart(chart, "E15")  # 在工作表上添加图表，并指定图表左上角锚定的单元格。
wb.save('result/实例.xlsx') # 保存工作薄
