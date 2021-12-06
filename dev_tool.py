# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd

filename = 'coverage_table.txt'
# filename = 'coverage_table - Large.txt'

data = pd.read_csv(filename,
                   sep="|",
                   engine='python',
                   skiprows=1)
data.columns = data.columns.str.strip()
print(data.columns)

for c in data.columns[1:]:
    data[c] = data[c].str.lstrip()  # strip leading space from all column data
    data[c] = data[c].str.split(' ', 1, expand=False)  # Split Columns into two

data = data.dropna()
print(data)

xAxis = []
yAxis = []
for n in range(3, len(data['Lines'])):
    yValue = float(data['Lines'][n][0].replace('%', ''))
    xValue = data[''][n].strip()
    yAxis.append(yValue)
    xAxis.append(xValue)


print("-------------------------------")
print(xAxis)
print(yAxis)

plotData = pd.DataFrame(yAxis, index=xAxis)
print(plotData)
print(list(plotData))

plotData.plot(kind='bar', figsize=(len(xAxis)/3, 10), title="Code coverage ratio by file", xlabel="File",
              ylabel="Ratio", legend=False)  # stacked=True
plt.show()
