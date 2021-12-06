# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Group 8 DevTool\nCreate a graph for code coverage from file')
parser.add_argument('-f', '--file', default='coverage_table.txt', help='Input file, default "coverage_table.txt"',
                    type=str, required=False)
parser.add_argument('-r', '--ratio', default=False, help='Sort x-axis by coverage ratio, default sort by x-label',
                    action='store_true', required=False)
parser.add_argument('-d', '--descending', default=False, help='Ascending sort, default ascending', action='store_true',
                    required=False)
parser.add_argument('-ns', '--no_sort', default=False, help='Skip sort (ignores other sort args), default False',
                    action='store_true', required=False)
parser.add_argument('-cl', '--centered_labels', default=False, help='Center labels, default False',
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
sort = not args['no_sort']
centered_labels = args['centered_labels']
separator = args['separator']
skip_rows = args['skip_rows']

data = pd.read_csv(filename, sep=separator, engine='python', skiprows=skip_rows)
data.columns = data.columns.str.strip()
# print(data.columns)

for c in data.columns[1:]:
    data[c] = data[c].str.lstrip()  # strip leading space from all column data
    data[c] = data[c].str.split(' ', 1, expand=False)  # Split Columns into two
data = data.dropna()
# print(data)

path = []
ratio = []
plotInput = {'Path': path, 'Ratio': ratio}
for n in range(3, len(data['Lines'])):
    ratio.append(float(data['Lines'][n][0].replace('%', '')))
    xData = data[''][n]
    if not centered_labels:
        xData = xData.strip()
    path.append(xData)

plotData = pd.DataFrame(plotInput)
plotData.set_index('Path', inplace=True)  # Set path as x-axis
# print(plotData)
# print(list(plotData))

if sort:
    if sort_by_ratio:
        plotData.sort_values(by='Ratio', inplace=True, ascending=ascending)  # Sort by ratio
    else:
        plotData.sort_index(key=lambda x: x.str.lower(), inplace=True, ascending=ascending)  # Sort by label

plotData.plot(kind='bar', figsize=(0.5 + len(path) / 3, 10), title='Code coverage ratio by file', xlabel='Path',
              ylabel='Ratio', legend=False)  # stacked=True
plt.show()
