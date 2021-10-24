import json
from pathlib import Path
import pandas as pd
import time
import utils


class Writer:
    def __init__(self, tweet_id: str, output_directory: str = "output") -> None:
        self.tweet_id = tweet_id

        path_str = "{output_directory}/{tweet_id}-{now}".format(
            output_directory=output_directory, now=utils.now(), tweet_id=tweet_id
        )
        self.output_base_path = Path(path_str).absolute()
        self.output_raw_data_path = self.output_base_path.joinpath("raw")

        # 出力先のディレクトリが存在しなければ作成する
        direcotries = [
            self.output_base_path,
            # self.output_reply_path,
            self.output_raw_data_path,
        ]
        for direcoty in direcotries:
            if not direcoty.exists():
                direcoty.mkdir()

    def save_raw(self, tweet_data: dict):
        tweet_id = tweet_data.get("id")
        filename = "{tweet_id}.json".format(tweet_id=tweet_id)
        filepath = self.output_raw_data_path.joinpath(filename)

        self.output_raw_data_path.joinpath(filename)
        with filepath.open(mode="w", encoding="utf-8") as file:
            file.write(json.dumps(tweet_data, sort_keys=False, ensure_ascii=False))
