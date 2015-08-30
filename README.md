# TransAsia

This is a Python code for checking TransAisa Airways' passenger ticket available.

## Requirement

1. Python 2.7
2. Requests
3. lxml

## Usage

```
usage: tna.py [-h] [-d {TPE,KIX}] -a {TPE,KIX} -t DATE

optional arguments:
  -h, --help            show this help message and exit
  -d {TPE,KIX}, --departure {TPE,KIX}
                        Departure Station Code
  -a {TPE,KIX}, --arrival {TPE,KIX}
                        Arrival Station Code
  -t DATE, --date DATE  Departure Date (YYYY/MM/DD)
```
