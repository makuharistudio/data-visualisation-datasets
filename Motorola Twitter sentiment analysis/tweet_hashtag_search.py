import tweepy
import configparser
import pandas as pd

config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

auth = tweepy.OAuthHandler(api_key,api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

keywords = '#motorola'
location_sydney = "-33.873096543580196, 151.20617788258537, 100 km"
location_melbourne = "-37.81490819853495, 144.96653337745843, 100 km"
location_brisbane = "-27.468271432591763, 153.02391617667723, 100 km"
location_adelaide = "-34.92569023935819, 138.60021764297156, 100 km"
location_perth = "-31.951321104026484, 115.84754509331489, 100 km"
location_hobart = "-42.885225001894575, 147.3302667870665, 100 km"
location_canberra = "-35.30675753401795, 149.12496928371215, 100 km"
# limit=400
limit=10
tweets = tweepy.Cursor(api.search_tweets, q=keywords, lang='en', result_type='recent', geocode=location_sydney).items(limit)

columns = ['Time', 'User', 'Tweet']
data = []
for tweet in tweets:
    data.append([tweet.created_at, tweet.user.screen_name, tweet.text.replace('\n', ' ')])
df = pd.DataFrame(data, columns=columns)
df.to_csv('tweets.csv')