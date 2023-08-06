import logging
import os
from argparse import ArgumentParser


# Set up arguments
parser = ArgumentParser(description='An OpenContest server written in Python')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='Enable verbose logging')
parser.add_argument('-p', '--port', default=9534,
                    help='Port to run the server on', type=int)
parser.add_argument('-d', '--data-dir', default=os.path.join(os.getcwd(), 'data'),
                    help='Data directory', type=str)
parser.add_argument('-c', '--contests-dir', default=os.path.join(os.getcwd(), 'contests'),
                    help='Contests directory', type=str)
args = parser.parse_args()


# Verbose logging
if args.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


# Make sure directories exist
os.makedirs(args.data_dir, exist_ok=True)
os.makedirs(args.contests_dir, exist_ok=True)
