import argparse
from pprint import pprint as pp
from . import CarbuAPI


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--codprov", required=False)
    args = parser.parse_args()

    api = CarbuAPI()
    pp(api.query(codprov=args.codprov))


if __name__ == "__main__":
    main()
