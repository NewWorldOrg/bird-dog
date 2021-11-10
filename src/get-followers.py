import argparse
import configparser
import logging
from pathlib import Path
from typing import List
import sys
import time
import json

from twarc.client2 import Twarc2
from twarc.expansions import ensure_flattened
import pandas as pd

# ログの設定
logger = logging.getLogger("get-followers")
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
    "get followers", usage="python src/get-followers.py --screen-name AbeShinzo"
)
parser.add_argument(
    "--screen-name",
    help="フォロワーを取得したいユーザーのスクリーンネーム",
    type=str,
    required=True,
)
args = parser.parse_args()

screen_name = args.screen_name

# 出力先のディレクトリの設定
now = time.strftime("%Y%m%d%H%M%S")

path_str = "{output_directory}/{screen_name}-{now}".format(
    output_directory="output",
    screen_name=screen_name,
    now=now,
)
output_path = Path(path_str).resolve()
output_rawdata_path = output_path.joinpath("raw")
output_rawdata_follower = output_rawdata_path.joinpath("follower")
output_rawdata_following = output_rawdata_path.joinpath("following")

# 出力先のディレクトリが存在しない場合は作成する（基本的には存在しない）
directories = [
    output_path,  # /output
    output_rawdata_path,  # /output/raw
    output_rawdata_follower,  # /output/raw/follower
    output_rawdata_following,  # /output/raw/following
]
for directory in directories:
    if not directory.exists():
        directory.mkdir(parents=True)

target_user = None
followers: List[dict] = []
following: List[dict] = []

# ユーザーIDの取得
for page in tw_client.user_lookup([screen_name], usernames=True):
    # 普通は1件
    for user in ensure_flattened(page):
        target_user = user

if target_user is None:
    logger.error("@{screen_name}は存在しません".format(screen_name=screen_name))
    sys.exit(1)


# ファイル名を返す
def filename_from_user(user: dict):
    user_id = user.get("id")
    filename = "{user_id}.json".format(user_id=user_id)
    return filename


# JSONとして保存
def save_user(user: dict, filepath: Path):
    with filepath.open(mode="w", encoding="utf-8") as file:
        file.write(json.dumps(user, sort_keys=False, ensure_ascii=False))


# フォロワー取得
logger.info("フォロワーの取得を開始します。")

for page in tw_client.followers(target_user.get("id")):
    for user in ensure_flattened(page):
        filename = filename_from_user(user)
        filepath = output_rawdata_follower.joinpath(filename)
        save_user(user, filepath)
        followers.append(user)

logger.info("フォロワーの取得が完了しました。")

# フォロー取得
logger.info("フォローの取得を開始します。")

for page in tw_client.following(target_user.get("id")):
    for user in ensure_flattened(page):
        filename = filename_from_user(user)
        filepath = output_rawdata_following.joinpath(filename)
        save_user(user, filepath)
        following.append(user)

logger.info("フォローの取得が完了しました。")

# CSVの出力
logger.info("CSVの出力を開始します。")

# 列情報
columns = [
    "name",
    "screen_name",
    "description",
    "following_count",
    "followers_count",
    "tweet_count",
    "created_at",
]

# 行データを返す
def to_row(user: dict):
    metrics: dict = user.get("public_metrics")
    return [
        user.get("name"),
        user.get("username"),
        user.get("description"),
        metrics.get("following_count"),
        metrics.get("followers_count"),
        metrics.get("tweet_count"),
        user.get("created_at"),
    ]


# gen follower.csv
df_follower = pd.DataFrame(data=map(to_row, followers), columns=columns)
follower_csv_filepath = output_path.joinpath("follower.csv")
df_follower.to_csv(follower_csv_filepath)

# following.csv
df_following = pd.DataFrame(data=map(to_row, following), columns=columns)
following_csv_filepath = output_path.joinpath("following.csv")
df_following.to_csv(following_csv_filepath)

logger.info("CSVの出力が完了しました。")

# TODO CSVの出力のみを行えるようにする
