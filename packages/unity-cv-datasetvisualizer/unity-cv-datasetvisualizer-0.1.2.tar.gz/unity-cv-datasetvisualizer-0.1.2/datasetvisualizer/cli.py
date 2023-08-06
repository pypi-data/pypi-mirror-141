import argparse
import os

import streamlit.bootstrap

cli = argparse.ArgumentParser()
cli.add_argument('--data', type=str,
                 help='path to dataset', default="")


def preview(args):
    """Previews the dataset in a streamlit app."""
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "preview.py")
    args = [args.data]
    streamlit.bootstrap.run(filename, "", args, None)


def main():
    preview(cli.parse_args())


if __name__ == "__main__":
    main()
