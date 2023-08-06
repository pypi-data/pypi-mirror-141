#!/usr/bin/env python3

#   -------------------------------------------------------------
#   Merge dictionaries
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Project:        Nasqueron
#   Description:    Merge dictionaries from various sources,
#                   mainly IDEs, and allow to propagate them.
#   License:        BSD-2-Clause
#   -------------------------------------------------------------


import argparse
import sys

from mergedictionaries.sources import jetbrains as jetbrains_source
from mergedictionaries.output import jetbrains as jetbrains_output
from mergedictionaries.write import jetbrains as jetbrains_write


#   -------------------------------------------------------------
#   Extract words
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def get_words_sources():
    return [
        jetbrains_source.extract_words_from_all_dictionaries,
    ]


def get_dictionary_formatters():
    return {
        "JetBrains": jetbrains_output.dump,
    }


def extract_all_words():
    return sorted([words for method in get_words_sources() for words in method()])


def run_extract_all_words(words_format):
    words = extract_all_words()

    # Trivial case
    if words_format == "text":
        for word in words:
            print(word)
        sys.exit(0)

    # We need a specific formatter
    formatters = get_dictionary_formatters()
    if words_format not in formatters:
        print(f"Unknown format: {words_format}", file=sys.stderr)
        sys.exit(2)

    print(formatters[words_format](words))
    sys.exit(0)


#   -------------------------------------------------------------
#   Merge all dictionaries
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def get_dictionary_writers():
    return [
        jetbrains_write.write,
    ]


def run_merge():
    words = extract_all_words()

    for method in get_dictionary_writers():
        method(words)


#   -------------------------------------------------------------
#   Application entry point
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def parse_arguments():
    parser = argparse.ArgumentParser(description="Merge dictionaries.")

    parser.add_argument(
        "--extract",
        action="store_const",
        dest="task",
        const="extract",
        help="Extract all words from found dictionaries",
    )
    parser.add_argument(
        "--format", action="store", help="Specifies the output format", default="text"
    )

    parser.add_argument(
        "--merge",
        action="store_const",
        dest="task",
        const="merge",
        help="Merge all found dictionaries",
    )

    return parser.parse_args()


def run():
    args = parse_arguments()

    if args.task is None:
        print("No task has been specified.", file=sys.stderr)
        sys.exit(1)

    if args.task == "extract":
        run_extract_all_words(args.format)
    elif args.task == "merge":
        run_merge()
