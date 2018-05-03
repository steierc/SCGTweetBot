import tweepy
import datetime

from random import randint
from time import sleep

# --------------- Twitter AUTH KEYS CARL --------------------------
# consumer_key = 'XZeZ1sSperKHeVZDaiPCcNGZd'
# consumer_secret = 'iaeN6vlkOuRyLrtKY2L1Djaz1b0AEf8k9oDqQToIGB0xVFAco6'
# access_token = '394330749-53oY3T27nYsJ4UJLtbaJCKWpFx63Bf8cByrVPVIf'
# access_token_secret = '23gHC5R27q87nEgt7fKd2MH5R0UPo4xfVj3Q835Yln8UY'
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
# api = tweepy.API(auth)


# ----------------------------------------------------------

consumer_key = '5CFs9vudSev0fIxOt8p2Q1QfM'
consumer_secret = 'wIYuEps6zNYSizA0r4VsWmsHegwQfMC7YnbZ7M9PQXIToW9rbt'
access_token = '2978112797-mNDVROv6k2CvmiQHIzDPqPFOKO8xqluvSCodYLq'
access_token_secret = 'CM4sJWeWu0gmiUpdOGELW5IgcInQGlemRTQrLXwMVZDLn'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# ----------- Other  Vars -------------
do_not_rt_list = ['@specutainment', '@prescottmsport', '@synergy72', '@taindogg', '@dailysportscar', '@dsceditor',
                  '@sportscar365', '@sc365live']
fiawec_handle = ["@fiawec", "@europeanlms", '@toyota_hybrid', '@bykolles', '@protonracing', '@gdrive_racing',
                 '@afcorse', '@tdsacing_live', '@amr_official', '@rebellionracing', '@circuitspa', '@jotasport',
                 '@oliverjameswebb', '@officialtfsport', '@porscheraces', '@fordperformance', '@racingteamnl', '@ginettacars']
search_query = "#WEC OR #FIAWEC OR #6hspa"
languages_to_rt_from = ['en', 'nl', 'de', 'fr']
minutes_to_wait_between_searches = 15


# ---------------------------

# # ----------- Get Tweets ------------
#
# # tweets = tweepy.Cursor(api.user_timeline, id="fiawec").items(10)
# # tweets = tweepy.Cursor(api.search, q='#WEC', since=last60search).items(100)
# tweets = tweepy.Cursor(api.search, q="#WEC OR #FIAWEC OR #6hspa", since=last60search).items(100)
# TWEETLIST=list(tweets)
# # for tweet in tweets:
#


def get_tweets(time_from):
    tweets = tweepy.Cursor(api.search, q="#WEC OR #FIAWEC OR #6hspa", since=time_from).items(100)
    TWEETLIST = list(tweets)
    return TWEETLIST


def sort_tweets(tweet_list, search_from):
    a_retweet = False
    sorted_tweet_list = []
    sorted_tweettext_list = []
    for tweet in tweet_list:
        a_retweet = False
        if tweet.created_at > search_from:
            try:
                if tweet.retweeted_status:
                    # print("Is RT??")
                    a_retweet = True
            except AttributeError:
                a_retweet = False
                # print("NOT RT")

            if tweet.text.lower().startswith("rt"):
                # print("STARTS WITH RT")
                a_retweet = True

            if not a_retweet:
                if tweet.text not in sorted_tweettext_list:
                    userhandle = "@%s" % tweet.user.screen_name

                    if userhandle.lower() not in do_not_rt_list and tweet.user.lang.lower() in languages_to_rt_from:
                        # print("UserHandle:[%s] Not Blacklisted" % userhandle)
                        # print('\tTweet by: @ %s [%s]' % (tweet.user.screen_name, tweet.created_at))
                        # print("\tLanguage=[%s]" % tweet.user.lang)
                        # print('\t[%s]\n\n---------------\n' % tweet.text)
                        sorted_tweettext_list.append(tweet.text)
                        sorted_tweet_list.append(tweet)
                    # need to add  count rt no more than 5 tweets in a 10 minute period
    return sorted_tweet_list


def retweet_or_fav(tweets_to_be_tweeted):
    tweets_found = len(tweets_to_be_tweeted)
    print("Valid Tweets Found: %s" % tweets_found)
    number_of_tweets_to_retweet = 10

    if number_of_tweets_to_retweet > tweets_found:
        number_of_tweets_to_retweet = tweets_found
    print("Going to RT %s" % number_of_tweets_to_retweet)
    counter = 0
    while counter <= number_of_tweets_to_retweet:
        if not tweets_to_be_tweeted:
            counter += 1
            print ("No Tweets Left Incrementing Counter")
        for tweet in tweets_to_be_tweeted:
            print "---------------------"
            print("Counter: %s" % counter)
            userhandle = "@%s" % tweet.user.screen_name
            if userhandle.lower() in fiawec_handle:
                print("*MUST RT ALL FIAWEC TWEETS*")
                print('\nReTweeting Tweet by: @ %s [%s]' % (tweet.user.screen_name, tweet.created_at))
                print("\tLanguage=[%s]" % tweet.user.lang)
                print('\t[%s]\n' % tweet.text)
                try:

                    tweet.favorite()
                    sleep(randint(2, 10))
                    tweet.retweet()
                    sleep(randint(1, 15))
                    tweets_to_be_tweeted.remove(tweet)
                except tweepy.TweepError as e:
                    print (" ALREADY RETWEETED ")
                    print("\tReason: [%s]" % e.reason.decode())
                    tweets_to_be_tweeted.remove(tweet)

                except StopIteration:
                    break
                # continue
            else:
                print('\nFavouriting Tweet by: @ %s [%s]' % (tweet.user.screen_name, tweet.created_at))
                print("\tLanguage=[%s]" % tweet.user.lang)
                print('\t[%s]\n\n' % tweet.text)

                try:

                    tweet.favorite()
                    sleep(randint(1, 5))
                    tweets_to_be_tweeted.remove(tweet)
                    # tweet.retweet()
                except tweepy.TweepError as e:
                    print (" ALREADY RETWEETED OR FAVED ")
                    print("\tReason: [%s]" % e.reason.decode())
                    tweets_to_be_tweeted.remove(tweet)

                except StopIteration:
                    break
                # continue

                counter += 1
            if counter >= number_of_tweets_to_retweet:
                print("Should I Break")
                break
        else:
            # counter += 1
            continue
        break

        # print("Counter: %s" % counter)


def main():
    tweetlist = list()
    tweetlist_text = list()

    # ------Time Stamp Setups -----
    # Get time now and format it
    now = datetime.datetime.utcnow()
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
    print ("Getting Tweets Between\n\t- %s" % formatted_now)

    # sixty_mins_ago = now + datetime.timedelta(minutes=-15)
    # generating time stamp to search from
    time_from = now + datetime.timedelta(minutes=-minutes_to_wait_between_searches)
    formatted_time_from = time_from.strftime("%Y-%m-%d %H:%M:%S")
    time_from_search = time_from.strftime("%Y-%m-%d")
    new_formatted_time_from = datetime.datetime.strptime(formatted_time_from, "%Y-%m-%d %H:%M:%S")
    print ("\t- %s" % formatted_time_from)

    while True:
        # Get a List of tweets from between now and time_from
        tweet_list = get_tweets(time_from=time_from_search)

        sorted_tweet_list = sort_tweets(tweet_list, new_formatted_time_from)
        # print("%s" % sorted_tweet_list)
        retweet_or_fav(sorted_tweet_list)
        print("Waiting 15 mins before going again...")
        sleep(900)


if __name__ == '__main__':
    main()
