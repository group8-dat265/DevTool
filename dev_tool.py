# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
import pandas_bokeh as pb
import numpy as np
import argparse


def create_argument_parser():
    """
    Create argument parser from the input arguments provided by the caller of the script.
    :return: Resulting argument parser.
    """
    parser = argparse.ArgumentParser(description='Group 8 DevTool\nCreate a graph for code coverage from file')
    parser.add_argument('-f', '--in_file', default='coverage_table.txt', type=str, required=False,
                        help='Input file, default "coverage_table.txt"')
    parser.add_argument('-o', '--out_file', type=str, required=False,
                        help='Output file, default "coverage_graph.html" or ".png" if non interactive')
    parser.add_argument('-r', '--ratio', default=False, action='store_true', required=False,
                        help='Sort x-axis by coverage ratio, default sort by x-label')
    parser.add_argument('-d', '--descending', default=False, action='store_true', required=False,
                        help='Ascending sort, default ascending')
    parser.add_argument('-ns', '--no_sort', default=False, action='store_true', required=False,
                        help='Skip sort (ignores other sort args), default False')
    parser.add_argument('-cl', '--centered_labels', default=False, action='store_true', required=False,
                        help='Center labels, default False')
    parser.add_argument('-ni', '--non_interactive', default=False, action='store_true', required=False,
                        help='Generate non interactive graph using pandas instead of pandas_bokeh, doesnt support '
                             'package graphs, default False')
    parser.add_argument('-p', '--plot_package', type=str, required=False,
                        help='Plot given packages separated by "," , default plots everything in one graph')
    parser.add_argument('-nc', '--no_complete', default=False, required=False, action='store_true',
                        help='No graph with ratio for all paths, default False')
    parser.add_argument('-s', '--separator', default='|', type=str, required=False,
                        help='File column separator, default "|"')  # Experimental
    parser.add_argument('-sr', '--skip_rows', default=1, type=int, required=False,
                        help='Lines to skip in file, default 1')  # Experimental
    return parser


def strip_and_split_data(data: pd.DataFrame):
    """
    Remove garbage from input data.
    :param data: Data to be cleaned up.
    :return: Cleaned up data frame.
    """

    data.columns = data.columns.str.strip()
    for c in data.columns[1:]:
        data[c] = data[c].str.lstrip()  # strip leading space from all column data
        data[c] = data[c].str.split(' ', 1, expand=False)  # Split Columns into two
    return data.dropna()


def parse_data(data: pd.DataFrame, match_packages: list, centered_labels: bool):
    """
    Parse input data and convert into a dict.
    :param data: Input data to be parsed
    :param match_packages: List of packages to be matched if flag set.
    :param centered_labels: Keep centered labels.
    :return: Dict containing parsed data.
    """
    path = []
    ratio = []
    plot_input = {'Path': path, 'Ratio': ratio}
    if match_packages:
        matching_package = []
        plot_input['Matching Package'] = matching_package
    for n in range(3, len(data['Lines'])):
        ratio.append(float(data['Lines'][n][0].replace('%', '')))
        x_data = data[''][n]
        if not centered_labels:
            x_data = x_data.strip()
        path.append(x_data)
        if match_packages:
            matches = []
            for match_package in match_packages:
                result = x_data.find(match_package)
                if result >= 0:
                    matches.append(x_data[:result] + match_package)
                    break  # TODO Remove once we can support multiple matches for the same path
            if matches:
                matching_package.append(matches[0])
                # package.append(matches)  # TODO Restore once we support multiple matches, can't add list as value
            else:
                matching_package.append(np.nan)
    return plot_input


def sub_graphs(plot_data: pd.DataFrame, match_packages: list):
    """
    Create sub graphs for the different packages.
    :param plot_data: Plot data to parse.
    :param match_packages: List of packages to create graphs for.
    :return: List containing the sub graphs.
    """
    print(type(plot_data))
    plot_datas = []
    plot_data_grouped = plot_data.groupby('Matching Package')
    for group in match_packages:
        if group in plot_data_grouped.groups:
            package_data = plot_data_grouped.get_group(group)
            package_data.set_index('Path', inplace=True)
            plot_datas.append(package_data)
    return plot_datas


def create_plots(plot_datas: list, sort: bool, sort_by_ratio: bool, ascending: bool, non_interactive: bool,
                 out_filename: str, complete: bool):
    """
    Create plots for given plot datas.
    :param plot_datas: Plot datas to create plots for.
    :param sort: Should the plots be sorted.
    :param sort_by_ratio: Should the plots be sorted by ratio (default sorted by path).
    :param ascending: Should the graphs be sorted as ascending.
    :param non_interactive: Should the graphs be non interactive (using panda plot instead of plot bokeh).
    :param out_filename: Output file name.
    :param complete: Should graph for complete plot data set be generated.
    :return: Generated plots.
    """
    plots = []
    for i, plot_data in enumerate(plot_datas):
        if sort:
            if sort_by_ratio:
                plot_data.sort_values(by='Ratio', inplace=True, ascending=ascending)  # Sort by ratio
            else:
                plot_data.sort_index(key=lambda x: x.str.lower(), inplace=True, ascending=ascending)  # Sort by label

        if non_interactive:
            plot = plot_data.plot(kind='bar', figsize=(int(0.5 + len(plot_data.index) / 3), 10),
                                  title='Code coverage ratio by file',
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
                title = 'Code coverage for "{}" package'.format(plot_data.iloc[0]['Matching Package'])
            plots.append(
                plot_data.plot_bokeh(kind='bar', figsize=(50 + len(plot_data.index) * 25, 700), title=title,
                                     xlabel='Path', ylabel='Ratio', legend=False, vertical_xlabel=True,
                                     fontsize_label=15, fontsize_ticks=10, show_figure=False))
    return plots


def create_grid(plots, complete: bool):
    """
    Create grid containing the plots.
    :param plots: PLots to be contained within the grid
    :param complete: Show complete plot
    :return: Grid containing the plots with complete plot at top if set.
    """
    if complete:
        grid = [
            [plots[0]], # Put complete graph on first row and rest below
            [plot for plot in plots[1:]]
        ]
    else:
        grid = [[plot for plot in plots]]
    return grid


def main():
    """
    Group 8 DevTool.
    This tool creates bar graphs for code coverage. This tool parses an input file containing test coverage data
    generated by for example lcov and then creates a bar graph showing the code coverage ratio for each file in the
    data set.

    The user can set various sorting options for the graph or create sub graphs for matching packages. See Options
    sections for available commands.

    """
    args = create_argument_parser().parse_args()
    in_filename = args.in_file
    non_interactive = args.non_interactive
    if args.out_file:
        out_filename = args.out_file
    elif non_interactive:
        out_filename = 'coverage_graph.png'
    else:
        out_filename = 'coverage_graph.html'
    sort_by_ratio = args.ratio
    ascending = not args.descending
    sort = not args.no_sort
    centered_labels = args.centered_labels
    separator = args.separator
    skip_rows = args.skip_rows
    match_packages = []
    if args.plot_package is not None:
        match_packages = [x.strip() for x in args.plot_package.split(',')]
    complete = not args.no_complete

    if not non_interactive:
        # pb.output_notebook()  # For embedding plots in Jupyter Notebooks.
        pb.output_file(out_filename)  # Remove for Jupyter Notebooks.

    data = pd.read_csv(in_filename, sep=separator, engine='python', skiprows=skip_rows)
    data = strip_and_split_data(data)

    plot_input = parse_data(data, match_packages, centered_labels)
    plot_data = pd.DataFrame(plot_input)

    plot_datas = []
    if match_packages:
        plot_datas = sub_graphs(plot_data, match_packages)
    if complete:
        plot_data.set_index('Path', inplace=True)  # Set path as x-axis
        plot_datas.insert(0, plot_data)

    plots = create_plots(plot_datas, sort, sort_by_ratio, ascending, non_interactive, out_filename, complete)

    grid = create_grid(plots, complete)
    pb.plot_grid(grid)


if __name__ == "__main__":
    main()
