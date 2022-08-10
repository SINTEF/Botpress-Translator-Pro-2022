# Python Script to manage translation of botpress chatbots

# Arguments:
# 2 modes, either extract or pack
# Takes a botpress chatbot path argument (.tgz file)
# Extract mode: Generate an excel file with all the translations needed
# Pack mode: Generate a new botpress chatbot from an excel file and the original chatbot
# Source language: The language of the original chatbot, default to english
# Target language: The language of the new chatbot, default to french

import argparse
from distutils.util import strtobool
import glob
from extract import extract
from pack import pack

args = argparse.ArgumentParser()
args.add_argument(
    "-m",
    "--mode",
    help="Mode of operation",
    choices=["extract", "pack"],
    default="extract",
)
args.add_argument(
    "-b",
    "--bot",
    help="Path to the botpress chatbot to extract or pack",
    default="*.tgz",
)
args.add_argument(
    "-e",
    "--excel",
    help="Path to the excel file to extract or pack",
    default="translations.xlsx",
)
args.add_argument(
    "-s",
    "--source",
    help="Source language of the chatbot, default to english",
    default="en",
)
args.add_argument(
    "-t",
    "--target",
    help="Target language of the chatbot, default to french",
    default="fr",
)

args.add_argument(
    '-n',
    '--new',
    help='Path to the new chatbot',
    default='new.tgz'
)

args.add_argument(
    '-g',
    '--google',
    help='Should the file be translated using google translate',
    default=True,
)

if __name__ == "__main__":
    args = args.parse_args()

    # If the bot path contains an star, find the first file that matches the pattern
    bot_path = args.bot
    if "*" in bot_path:
        bot_path = glob.glob(bot_path)[0]
        if not bot_path:
            print("No bot found for path " + bot_path)
            exit(1)

    if args.mode == "extract":
        google = strtobool(args.google)
        extract(bot_path, args.excel, args.source, args.target, google)
    elif args.mode == "pack":
        pack(bot_path, args.excel, args.new)
