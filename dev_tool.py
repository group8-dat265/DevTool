# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
import pandas_bokeh as pb
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Group 8 DevTool\nCreate a graph for code coverage from file')
parser.add_argument('-f', '--in_file', default='coverage_table.txt', help='Input file, default "coverage_table.txt"',
                    type=str, required=False)
parser.add_argument('-o', '--out_file', help='Output file, default "coverage_graph.html" or ".png" if non interactive',
                    type=str, required=False)
parser.add_argument('-r', '--ratio', default=False, help='Sort x-axis by coverage ratio, default sort by x-label',
                    action='store_true', required=False)
parser.add_argument('-d', '--descending', default=False, help='Ascending sort, default ascending', action='store_true',
                    required=False)
parser.add_argument('-ns', '--no_sort', default=False, help='Skip sort (ignores other sort args), default False',
                    action='store_true', required=False)
parser.add_argument('-cl', '--centered_labels', default=False, help='Center labels, default False',
                    action='store_true', required=False)
parser.add_argument('-ni', '--non_interactive', default=False,
                    help='Generate non interactive graph using pandas instead of pandas_bokeh, doesnt support package'
                         ' graphs, default False', action='store_true', required=False)
parser.add_argument('-p', '--plot_package', type=str, required=False,
                    help='Plot given packages separated by "," , default plots everything in one graph')
parser.add_argument('-nc', '--no_complete', default=False, help='No graph with ratio for all paths, default False',
                    required=False, action='store_true')
parser.add_argument('-s', '--separator', default='|', help='File column separator, default "|"', type=str,
                    required=False)  # Untested
parser.add_argument('-sr', '--skip_rows', default=1, help='Lines to skip in file, default 1', type=int,
                    required=False)  # Untested
args = vars(parser.parse_args())
in_filename = args['in_file']
non_interactive = args['non_interactive']
if args['out_file']:
    out_filename = args['out_file']
elif non_interactive:
    out_filename = 'coverage_graph.png'
else:
    out_filename = 'coverage_graph.html'
sort_by_ratio = args['ratio']
ascending = not args['descending']
sort = not args['no_sort']
centered_labels = args['centered_labels']
separator = args['separator']
skip_rows = args['skip_rows']
match_packages = []
if args['plot_package'] is not None:
    match_packages = [x.strip() for x in args['plot_package'].split(',')]
complete = not args['no_complete']

# pb.output_notebook()  # For embedding plots in Jupyter Notebooks.
if not non_interactive:
    pb.output_file(out_filename)  # Remove for Jupyter Notebooks.
data = pd.read_csv(in_filename, sep=separator, engine='python', skiprows=skip_rows)
data.columns = data.columns.str.strip()

for c in data.columns[1:]:
    data[c] = data[c].str.lstrip()  # strip leading space from all column data
    data[c] = data[c].str.split(' ', 1, expand=False)  # Split Columns into two
data = data.dropna()

path = []
ratio = []
plotInput = {'Path': path, 'Ratio': ratio}
if match_packages:
    matching_package = []
    plotInput['Matching Package'] = matching_package
for n in range(3, len(data['Lines'])):
    ratio.append(float(data['Lines'][n][0].replace('%', '')))
    xData = data[''][n]
    if not centered_labels:
        xData = xData.strip()
    path.append(xData)
    if match_packages:
        matches = []
        for match_package in match_packages:
            result = xData.find(match_package)
            if result >= 0:
                matches.append(xData[:result] + match_package)
                break  # TODO Remove once we can support multiple matches
        if matches:
            matching_package.append(matches[0])
            # package.append(matches)  # TODO Restore once we support multiple matches, can't add list as value
        else:
            matching_package.append(np.nan)

plotData = pd.DataFrame(plotInput)
print(plotData)

plotDatas = []
if match_packages:
    plotDataGrouped = plotData.groupby('Matching Package')
    for group in match_packages:
        if group in plotDataGrouped.groups:
            packageData = plotDataGrouped.get_group(group)
            packageData.set_index('Path', inplace=True)
            plotDatas.append(packageData)
            print(plotDatas)
if complete:
    plotData.set_index('Path', inplace=True)  # Set path as x-axis
    plotDatas.insert(0, plotData)

plots = []
for i, plotData in enumerate(plotDatas):
    if sort:
        if sort_by_ratio:
            plotData.sort_values(by='Ratio', inplace=True, ascending=ascending)  # Sort by ratio
        else:
            plotData.sort_index(key=lambda x: x.str.lower(), inplace=True, ascending=ascending)  # Sort by label

    if non_interactive:
        plot = plotData.plot(kind='bar', figsize=(int(0.5 + len(path) / 3), 10), title='Code coverage ratio by file',
                             xlabel='Path', ylabel='Ratio', legend=False)  # stacked=True
        figure = plot.figure
        figure.set_tight_layout(True)
        figure.savefig(out_filename)
        plt.show()
        break
    else:
        if complete and i == 0:
            title = 'Code coverage ratio by file'
        else:
            title = 'Code coverage for "{}" package'.format(plotData.iloc[0]['Matching Package'])
        plots.append(
            plotData.plot_bokeh(kind='bar', figsize=(50 + len(path) * 25, 700), title=title,
                                xlabel='Path', ylabel='Ratio', legend=False, vertical_xlabel=True, fontsize_label=15,
                                fontsize_ticks=10, show_figure=False))

if complete:
    grid = [
        [plots[0]],
        [plot for plot in plots[1:]]
    ]
else:
    grid = [[plot for plot in plots]]
pb.plot_grid(grid)
