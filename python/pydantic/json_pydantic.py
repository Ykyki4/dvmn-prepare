import argparse
import json

from pydantic import ValidationError
from pydantic.json import pydantic_encoder

from models import User, Product, Cart, Users


def arg_parser():
    parser = argparse.ArgumentParser(description='Import json to pydantic')
    parser.add_argument('input_file', type=str, help='json input file')
    parser.add_argument('output_file', type=str, help='json output file')
    return parser


if __name__ == '__main__':
    parser = arg_parser()
    args = parser.parse_args()
    try:
        with open(args.input_file) as file:
            content = json.load(file)
            users = Users(**content)

        with open(args.output_file, 'w') as file:
            file.write(users.json())
    except ValidationError as e:
        print(e)
