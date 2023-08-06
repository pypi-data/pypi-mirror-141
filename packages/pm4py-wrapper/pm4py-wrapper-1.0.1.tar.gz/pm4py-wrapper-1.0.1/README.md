# pm4py-wrapper

CLI wrapper for pm4py. 

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
