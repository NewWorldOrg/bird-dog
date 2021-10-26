import json
import argparse
from twarc.client2 import Twarc2
from twarc.expansions import ensure_flattened
import configparser
import logging
import time
from pathlib import Path

# ログの設定
logger = logging.getLogger("get-replies")
logging.basicConfig(level=logging.INFO)

# twitterクライアントの設定
config = configparser.ConfigParser(interpolation=None)
config.read("./config.ini")

tw_config = config["Twitter"]

tw_client = Twarc2(
    consumer_key=tw_config["CONSUMER_KEY"], consumer_secret=tw_config["CONSUMER_SECRET"]
)
# コマンドライン引数の設定と取得
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

# 出力先のディレクトリの設定
now = time.strftime("%Y%m%d%H%M%S")

path_str = "{output_directory}/{conversation_id}-{now}".format(
    output_directory="output",
    now=now,
    conversation_id=conversation_id,
)
output_path = Path(path_str).resolve()
output_rawdata_path = output_path.joinpath("raw")

# 出力先のディレクトリが存在しない場合は作成する
direcotries = [output_path, output_rawdata_path]
for direcoty in direcotries:
    if not direcoty.exists():
        direcoty.mkdir(parents=True)

# リプライの取得と保存
query = "conversation_id:{conversation_id}".format(conversation_id=conversation_id)

for page in tw_client.search_all(query=query):
    for tweet in ensure_flattened(page):
        tweet_id = tweet.get("id")
        filename = "{tweet_id}.json".format(tweet_id=tweet_id)
        filepath = output_rawdata_path.joinpath(filename)

        with filepath.open(mode="w", encoding="utf-8") as file:
            file.write(json.dumps(tweet, sort_keys=False, ensure_ascii=False))

logger.info("取得完了しました {filepath}".format(filepath=output_path))
