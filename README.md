# bird-dog

# 初期設定

config.sample.iniをconfig.iniという名前でコピーする。  
config.iniに各種鍵を設定する。  

```bash
# 依存関係の解決
pipenv sync

pipenv shell
```

# リプライの取得からCSVの出力まで

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

python src/gen-csv.py --target 1452231609965371393-20211024223924

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
