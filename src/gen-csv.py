import argparse
import json
from pathlib import Path
from typing import List
import pandas as pd
import logging

# ログの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("gen-csv")

# コマンドライン引数の設定と取得
parser = argparse.ArgumentParser(
    "gen csv",
    usage="python src/gen-csv.py --target output/1418567538753949700-20211024183641",
)
parser.add_argument("--target", type=str, required=True)
args = parser.parse_args()
target = args.target

# 取得したリプライデータを読み出し
target_path = Path(target).resolve()

tweets: List[dict] = []

if target_path.exists():
    raw_filepath = target_path.joinpath("raw").resolve()
    filepaths = list(raw_filepath.iterdir())
    size = len(filepaths)
    filepath_with_index = enumerate(filepaths)
    for index, filepath in filepath_with_index:
        with filepath.open("r") as file:
            tweet = json.loads(file.read())
            tweets.append(tweet)
        logger.info(
            "読み込み完了({index}/{size}) {filepath}".format(
                index=index + 1,
                size=size,
                filepath=filepath,
            )
        )
else:
    logger.error("ファイルが存在しません")


# CSVデータの書き出し
columns = ["user_id", "username", "name", "description", "text"]


def to_row(tweet: dict):
    author: dict = tweet.get("author")
    return [
        author.get("id"),
        author.get("username"),
        author.get("name"),
        author.get("description"),
        tweet.get("text"),
    ]


df = pd.DataFrame(
    data=map(to_row, tweets),
    columns=columns,
)

result_filepath = target_path.joinpath("result.csv")
df.to_csv(result_filepath)
logger.info("出力完了 {result_filepath}".format(result_filepath=result_filepath))
