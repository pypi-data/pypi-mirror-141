import sys
import re


if __name__ == '__main__':
    r = re.compile(r"__@MATCH#@REGEX#__")
    match = ""
    with open(sys.argv[1], 'r') as f:
        for line in f:
            content = r.match(line)
            if content:
                match = content.group(1)
    
    print(match, flush=True)