# DevTool Group 8

This tool creates bar graphs for code coverage. This tool parses an input file containing test coverage data generated 
by for example [lcov](http://ltp.sourceforge.net/coverage/lcov.php) and then creates a bar graph showing the code 
coverage ratio for each file in the data set.

The user can set various sorting options for the graph or create sub graphs for matching packages. See Options section
for available commands.

Example graph:
![See /example/coverage_graph.pngg](https://github.com/group8-dat265/DevTool/blob/master/example/coverage_graph.png)

## Installation
Install Python3

Install dependencies with the command ```pip install -r requirements.txt``` (could also be pip3).

Clone the repository from GitHub.

## How to use
To test the tool simply run ```python dev_tool.py -f example/coverage_table.txt```.

##### Run on another project
Generate a code coverage file with for example [lcov](http://ltp.sourceforge.net/coverage/lcov.php).

Run the DevTool with the command ```python dev_tool.py -f <generated_file_name.txt>``` (could also be python3).

See option chapter on how to change options like separator or number of rows to skip if the tool can't parse the input 
file.

## Options
```
optional arguments:
  -h, --help            show this help message and exit
  -f IN_FILE, --in_file IN_FILE
                        Input file, default "coverage_table.txt"
  -o OUT_FILE, --out_file OUT_FILE
                        Output file, default "coverage_graph.html" or ".png" if non interactive
  -r, --ratio           Sort x-axis by coverage ratio, default sort by x-label
  -d, --descending      Ascending sort, default ascending
  -ns, --no_sort        Skip sort (ignores other sort args), default False
  -cl, --centered_labels
                        Center labels, default False
  -ni, --non_interactive
                        Generate non interactive graph using pandas instead of pandas_bokeh, doesnt support package
                        graphs, default False
  -p PLOT_PACKAGE, --plot_package PLOT_PACKAGE
                        Plot given packages separated by "," , default plots everything in one graph
  -nc, --no_complete    No graph with ratio for all paths, default False
  -s SEPARATOR, --separator SEPARATOR
                        File column separator, default "|"
  -sr SKIP_ROWS, --skip_rows SKIP_ROWS
                        Lines to skip in file, default 1
```
<!-- [![Open in CodeLab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/group8-dat265/DevTool/blob/master/Dev_Tool.ipynb) -->
