import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
import time


# Stream Listener API
class MyListener(StreamListener):

    def on_data(self, data):
        try:
            print(data)
            saveFile = open('EventData.csv', 'a')
            saveFile.write(data)
            saveFile.write('\n')
            saveFile.close()
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)

    def on_error(self, status):
        print(status)
        return True


# Authenticate to Twitter
auth = tweepy.OAuthHandler("GPSToP17pDPGHOlYUi7APfa10",
                           "iwGBgu8rO3jjSyeDptQ7qtsyXX4LEzAEPseMvt9HyK6N6C6juW")
auth.set_access_token("2953659962-cMbfZLRsnn9zXm5QQx5FJ9e1YA864JX5Y8MKtus",
                      "MQ8eebRo9t8yD2xNOklERXA7epTgEahfbL38Sm5BsnIw4")

api = tweepy.API(auth)

eventList = ["event", "events", "sports", "sport", "politics", "political", "art", "arts", "entertainment", "food",
             "tasting", "books", "book", "book reading", "show", "fun"]

twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['events', 'event'])

# Cursor to fetch User Details
for tweet in api.search(q="Python", lang="en", rpp=10, geocode="39°50′N 98°35′W"):
    print(f"{tweet.user.name}:{tweet.text}")

places = api.geo_search(query="USA", granularity="country")
place_id = places[0].id

tweets = api.search(q="place:%s" % place_id, limit=1000, lang="en")
for tweet in tweets:
    print(f"{tweet.text} : {tweet.place.name}")
