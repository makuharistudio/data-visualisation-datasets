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

keywords = ['Motorola']

# used for tweepy.Cursor(grocode = ) attribute, but doesn't seem to work?
# location_sydney = '-33.873096543580196,151.20617788258537,100km'
# location_melbourne = "-37.81490819853495, 144.96653337745843, 100 km"
# location_brisbane = "-27.468271432591763, 153.02391617667723, 100 km"
# location_adelaide = "-34.92569023935819, 138.60021764297156, 100 km"
# location_perth = "-31.951321104026484, 115.84754509331489, 100 km"
# location_hobart = "-42.885225001894575, 147.3302667870665, 100 km"
# location_canberra = "-35.30675753401795, 149.12496928371215, 100 km"
# limit=450

limit=900
tweets = tweepy.Cursor(api.search_tweets, q=keywords, lang='en', result_type='recent').items(limit)

columns = ['TweetDateTime', 
           'UserID',
           'UserName',
           'UserScreenName',
           'UserDescription',
           'UserCreatedDateTime',
           'UserVerified',
           'UserLocation',
           'UserFollowers',
           'TweetContent',
           'TweetFavourites',
           'TweetRetweets']
data = []
for tweet in tweets:
    data.append([tweet.created_at,
                 tweet.user.id, 
                 tweet.user.name.replace('\n', ' ').replace(',',' '),
                 tweet.user.screen_name.replace('\n', ' ').replace(',',' '),
                 tweet.user.description.replace('\n', ' ').replace(',',' '),
                 tweet.user.created_at,
                 tweet.user.verified,
                 tweet.user.location.replace('\n', ' ').replace(',',' '),
                 tweet.user.followers_count,
                 tweet.text.replace('\n', ' ').replace(',',' '),
                 tweet.favorite_count,
                 tweet.retweet_count])
df = pd.DataFrame(data, columns=columns)
df.to_csv('tweets.csv')