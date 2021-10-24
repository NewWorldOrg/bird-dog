import argparse
from twarc.client2 import Twarc2
from twarc.expansions import ensure_flattened
import configparser
from writer import Writer
import logging

logging.basicConfig(level=logging.INFO)

config = configparser.ConfigParser(interpolation=None)
config.read("./config.ini")

tw_config = config["Twitter"]

tw_client = Twarc2(
    consumer_key=tw_config["CONSUMER_KEY"], consumer_secret=tw_config["CONSUMER_SECRET"]
)


def make_query(conversation_id: str):
    return "conversation_id:{conversation_id}".format(conversation_id=conversation_id)


parser = argparse.ArgumentParser(
    "get replies", usage="python src/get-replies.py --conv-id 1418567538753949700"
)
parser.add_argument(
    "--conv-id",
    help="リプライを取得したツイートのID（ツイートのURLが「https://twitter.com/23_twt/status/1418567538753949700」の場合は「1418567538753949700」）",
    type=str,
    required=True,
)
args = parser.parse_args()

conversation_id = args.conv_id

writer = Writer(conversation_id)
query = make_query(conversation_id)

for page in tw_client.search_all(query=query):
    for tweet in ensure_flattened(page):
        writer.save_raw(tweet)
