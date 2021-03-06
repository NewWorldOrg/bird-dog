# bird-dog

特定のツイートにぶら下がっているリプライを取得します。  
アカデミック版のtwitter api(v2)のキーが必要です。  
取得したリプライをcsvに書き出すツールも付属してます。  

# 前提条件

アプリを実行するマシンに以下のソフトウェアがインストールされていること

- git
- docker
- docker-compose

# アプリをローカルに落とす方法

任意のディレクトリで以下のコマンドを実行

```shell
git clone https://github.com/NewWorldOrg/bird-dog
```

無事に `bird-dog` が存在されている事を確認できたら以下のコマンドで落としてきたアプリのディレクトリに入る

```shell
cd bird-dog
```

# 初期設定

## docker環境の構築手順

### 1.docker-compose.ymlを作る

```shell
cp docker-compose-example.yml docker-compose.yml
```

- **※ 必要なら適宜docker-compose.ymlを書き換える**

### 2.docker環境をビルドする

```shell
docker-compose build
```

- ビルドが乾燥したら次のステップへ

### 3.docker環境の起動

```shell
docker-compose up -d
```

# 設定ファイルの構築
config.sample.iniをconfig.iniという名前でコピーする。

```shell
cp config.sample.ini config.init
```

コピーで作成された、config.iniを書き換えて各種鍵を設定する。

# 使い方

dockerで構築したコンテナに入る

```shell
docker-compose exec app bash
```

無事コンテナに入れたら以下のコマンドを実行してpipenvの環境を構築して入る

```bash
# 依存関係の解決
pipenv sync

# pipenvで作られた仮想環境へ入る
pipenv shell
```

# 使い方

## 例: リプライの取得からCSVの出力まで

- `pipenv shell` で仮想環境に入れば以下の手順でツイートの解析を出力ができるようになる

データの取得とCSVの出力のプログラムは別々にしてあります。  

試しに以下のツイートでやってみます。  
https://twitter.com/nomorehole2/status/1452231609965371393  

```bash
python src/get-replies.py --conv-id 1452231609965371393

# ログ出力例
INFO:twarc:creating app auth client via OAuth2
INFO:twarc:getting ('https://api.twitter.com/2/tweets/search/all',) {'params': {'expansions': 'author_id,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id,entities.mentions.username,attachments.poll_ids,attachments.media_keys,geo.place_id', 'user.fields': 'created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld', 'tweet.fields': 'attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,public_metrics,text,possibly_sensitive,referenced_tweets,reply_settings,source,withheld', 'media.fields': 'alt_text,duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics', 'poll.fields': 'duration_minutes,end_datetime,id,options,voting_status', 'place.fields': 'contained_within,country,country_code,full_name,geo,id,name,place_type', 'query': 'conversation_id:1452231609965371393', 'max_results': 100, 'start_time': '2006-03-21T00:00:00+00:00'}}
INFO:twarc:No more results for search conversation_id:1452231609965371393.
INFO:get-replies:取得完了しました /home/user/dev/personal/bird-dog/output/1452231609965371393-20211024223924

python src/gen-csv.py --target ./output/1452231609965371393-20211024223924/

# ログ出力例
INFO:gen-csv:読み込み完了(1/12) /home/user/dev/personal/bird-dog/output/1452231609965371393-20211024223924/raw/1452250363080306692.json
INFO:gen-csv:読み込み完了(2/12) /home/user/dev/personal/bird-dog/output/1452231609965371393-20211024223924/raw/1452266117003571208.json
INFO:gen-csv:読み込み完了(3/12) /home/user/dev/personal/bird-dog/output/1452231609965371393-20211024223924/raw/1452237723025117188.json
INFO:gen-csv:読み込み完了(4/12) /home/user/dev/personal/bird-dog/output/1452231609965371393-20211024223924/raw/1452233960377913351.json
INFO:gen-csv:読み込み完了(5/12) /home/user/dev/personal/bird-dog/output/1452231609965371393-20211024223924/raw/1452237485237424130.json
INFO:gen-csv:読み込み完了(6/12) /home/user/dev/personal/bird-dog/output/1452231609965371393-20211024223924/raw/1452244701218701316.json
INFO:gen-csv:読み込み完了(7/12) /home/user/dev/personal/bird-dog/output/1452231609965371393-20211024223924/raw/1452260062739591174.json
INFO:gen-csv:読み込み完了(8/12) /home/user/dev/personal/bird-dog/output/1452231609965371393-20211024223924/raw/1452251997994770436.json
INFO:gen-csv:読み込み完了(9/12) /home/user/dev/personal/bird-dog/output/1452231609965371393-20211024223924/raw/1452237272120651780.json
INFO:gen-csv:読み込み完了(10/12) /home/user/dev/personal/bird-dog/output/1452231609965371393-20211024223924/raw/1452266556893790215.json
INFO:gen-csv:読み込み完了(11/12) /home/user/dev/personal/bird-dog/output/1452231609965371393-20211024223924/raw/1452234341161988097.json
INFO:gen-csv:読み込み完了(12/12) /home/user/dev/personal/bird-dog/output/1452231609965371393-20211024223924/raw/1452236379920814081.json
INFO:gen-csv:出力完了 /home/user/dev/personal/bird-dog/output/1452231609965371393-20211024223924/result.csv

```

## 特定ユーザーのフォローとフォロワーを取得しCSVで出力する

データ量が多かった場合（100万件とか）の動作確認をしていないため落ちるかもしれないです。

```bash
# 「@」は含めない点に注意する
python src/get-followers.py --screen-name AbeShinzo
```

# コラム

鳥猟犬とは - コトバンク : https://kotobank.jp/word/%E9%B3%A5%E7%8C%9F%E7%8A%AC-1368471  

> 狩猟に使役するイヌ。鳥や獣を見つけ出し，追いかけ，つかまえることが得意な種類のイヌをいい，一般に獣猟に使う猟犬を獣猟犬，鳥猟に使う猟犬を鳥猟犬と呼ぶ。古くから獣猟にはイヌが大きな役割を果たし，その特性は現在の獣猟犬にも受けつがれている。
