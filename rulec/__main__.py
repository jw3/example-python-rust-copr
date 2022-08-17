#!/usr/bin/env python3

import sys
import configargparse as argparse
import rulec.rust


def main(*argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("rules", type=str, help="file or dir containing rules")
    args = parser.parse_args(argv)
    try:
        rulec.rust.validate_rules_at(args.rules)
    except Exception as e:
        exit(1)


if __name__ == "__main__":
    main(*sys.argv[1:])
