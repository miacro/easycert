#!/usr/bin/env python

import argparse


def main():
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "easycert",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="easy cert")
    subparsers = parser.add_subparsers(
        title="subcommands",
        description="sub commands: []",
        help="sub commands")
    parser_key = subparsers.add_parser(
        "key",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="key")
    parser_cert = subparsers.add_parser(
        "cert",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="cert")
    parser_ca = subparsers.add_parser(
        "ca",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="ca")
    args = parser.parse_args()
    main()
