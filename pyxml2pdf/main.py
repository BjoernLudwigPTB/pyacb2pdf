import argparse
import os
import sys
from typing import Dict

from pyxml2pdf.core.downloader import Downloader
from pyxml2pdf.core.initializer import Initializer


def _add_arguments() -> Dict[str, str]:
    # Execute pyxml2pdf with provided command line parameters.
    parser = argparse.ArgumentParser(
        description="A converter for XML data into nicely formatted tables in a PDF."
    )
    parser.add_argument(
        "local_file",
        nargs="+",
        type=str,
        default="input/kursdaten.xml",
        help="The local file path to the XML file. If this file is not present, "
        "the optional input parameter '--url' needs to be provided with the URL "
        "from which the file shall be downloaded.",
    )
    parser.add_argument(
        "-u",
        "--url",
        nargs=1,
        type=str,
        default="https://www.alpinclub-berlin.de/kv/kursdaten.xml",
        help="The URL from which the file shall be downloaded. This is only used, "
        "if the specified local file is not present. Defaults to "
        "'https://www.alpinclub-berlin.de/kv/kursdaten.xml'",
    )
    parser.add_argument(
        "-p",
        "--pdf",
        nargs=1,
        type=str,
        default="output/kursdaten.pdf",
        help="The file path to store the created PDF to. Defaults to "
        "'output/kursdaten.pdf'",
    )
    return vars(parser.parse_args())


def main():
    args = _add_arguments()
    validate_inputs(args)
    if not os.path.isfile(args["local_file"][0]):
        Downloader(args["url"][0], args["local_file"][0])
    Initializer(args["local_file"][0], args["pdf"][0])
    print("\n-------------------------------DONE-------------------------------")


def validate_inputs(args: Dict[str, str]):
    """Checks the provided parameters on validity

    :param Dict[str, str] args: the parsed parameter namespace
    """
    if "local_file" not in args:
        raise ValueError(
            f"We expected at least the local XML as input parameter, "
            f"but only {args} were given. Please specify the "
            f"local path and filename of a valid XML file."
        )


def init():
    if __name__ == "__main__":
        sys.exit(main())


init()