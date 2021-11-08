import argparse
import configparser
import logging

from twarc.client2 import Twarc2
from twarc.expansions import ensure_flattened


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
target_user = None

# ユーザーIDの取得
for page in tw_client.user_lookup([screen_name], usernames=True):
    # 普通は1件
    for user in ensure_flattened(page):
        target_user = user

if target_user is not None:
    # フォロワー取得
    for page in tw_client.followers(target_user.get("id")):
        for user in ensure_flattened(page):
            pass

    # フォロー取得
    for page in tw_client.following(target_user):
        for user in ensure_flattened(page):
            pass
else:
    logger.error("@{screen_name}は存在しません".format(screen_name=screen_name))
