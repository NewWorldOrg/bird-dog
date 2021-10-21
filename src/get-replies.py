from twarc.client2 import Twarc2
from twarc.expansions import ensure_flattened, flatten
import configparser

config = configparser.ConfigParser(interpolation=None)
config.read('./config.ini')

tw_config = config['Twitter']

tw_client = Twarc2(
    bearer_token=tw_config['BEARER_TOKEN']
)

def get_conversation_id(tweet_id: str):
    tweets = tw_client.tweet_lookup([tweet_id])
    target_tweet = next(tweets)
    conversation_id = target_tweet['data'][0]['conversation_id']
    return conversation_id

# conversation_idはtweetのidと同じなので別に取得する必要はなかった
conversation_id = get_conversation_id('1418567538753949700')
print(conversation_id)