# bird-dog

# ポート番号のメモ

| サービス名 | ポート番号 |
| :- | :- |
| Elasticsearch | 9100 |
| Kibana | 5601 |

# 初期設定

```bash
# 依存関係の解決
pipenv sync

pipenv shell

python src/init-elasticsearch.py
```