# pm4py-wrapper

CLI wrapper for pm4py.

## Installation

Install using [pip](https://pip.pypa.io/en/stable/installation/):

```shell
pip install pm4py-wrapper
```

## Usage

```
Usage: pm4py_wrapper [OPTIONS] COMMAND [ARGS]...

Options:
  -i, --input_log PATH   Path to the input event log.  [required]
  -o, --output_dir PATH  Path to the output directory.
  --help                 Show this message and exit.

Commands:
  csv-to-xes
  xes-to-csv

```

Examples:

```shell
$ pm4py_wrapper -i tests/assets/input/Production.xes -o tests/assets/output xes-to-csv
$ pm4py_wrapper -i tests/assets/input/Production.csv -o tests/assets/output csv-to-xes
```

## Links

- A helpful [answer](https://stackoverflow.com/questions/57628064/automating-python-package-release-process#answer-57676367) on StackOverflow on how to do CI/CD with Poetry.
