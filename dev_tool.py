# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Group 8 DevTool\nCreate a graph for code coverage from file')
parser.add_argument('-f', '--file', default='coverage_table.txt', help='Input file, default "coverage_table.txt"',
                    type=str, required=False)
parser.add_argument('-r', '--ratio', default=False, help='Sort xAxis by coverage ratio, default false',
                    action='store_true', required=False)
parser.add_argument('-d', '--descending', default=False, help='Ascending sort, default ascending', action='store_true',
                    required=False)
parser.add_argument('-ns', '--no_sort', default=False, help='Skip sort (ignores other sort args), default False',
                    action='store_true', required=False)
parser.add_argument('-s', '--separator', default='|', help='File column separator, default "|"', type=str,
                    required=False)  # Untested
parser.add_argument('-sr', '--skip_rows', default=1, help='Lines to skip in file, default 1', type=int,
                    required=False)  # Untested
args = vars(parser.parse_args())
filename = args['file']
# filename = 'coverage_table - Large.txt'
sort_by_ratio = args['ratio']
ascending = not args['descending']
separator = args['separator']
skip_rows = args['skip_rows']
no_sort = args['no_sort']

data = pd.read_csv(filename, sep=separator, engine='python', skiprows=skip_rows)
data.columns = data.columns.str.strip()
# print(data.columns)

for c in data.columns[1:]:
    data[c] = data[c].str.lstrip()  # strip leading space from all column data
    data[c] = data[c].str.split(' ', 1, expand=False)  # Split Columns into two
data = data.dropna()
# print(data)

xAxis = []
yAxis = []
for n in range(3, len(data['Lines'])):
    yAxis.append(float(data['Lines'][n][0].replace('%', '')))
    xAxis.append(data[''][n].strip())  # Remove strip to center all labels
# print(xAxis)
# print(yAxis)

plotData = pd.DataFrame(yAxis, index=xAxis)
# print(plotData)
# print(list(plotData))
# print(plotData[0])

if not no_sort:
    if sort_by_ratio:
        plotData.sort_values(by=0, inplace=True, ascending=ascending)  # Sort by ratio
    else:
        plotData.sort_index(key=lambda x: x.str.lower(), inplace=True, ascending=ascending)  # Sort by file name

plotData.plot(kind='bar', figsize=(len(xAxis)/3, 10), title='Code coverage ratio by file', xlabel='File',
              ylabel='Ratio', legend=False)  # stacked=True
plt.show()
