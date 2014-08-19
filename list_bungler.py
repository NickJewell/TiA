import urllib, json
import sys
import tweepy
from tweepy import OAuthHandler
import requests
from textblob import TextBlob
from bs4 import BeautifulSoup
import csv
import datetime
import math
import time
import re
import sqlite3 as lite
import pprint
#from __future__ import absolute_import
#from __future__ import division, print_function, unicode_literals
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


def twitter_fetch():
	consumer_key = ''
	consumer_secret = ''
	access_token = ''
	access_token_secret = ''
	auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
	auth.set_access_token(access_token,access_token_secret)
	api  = tweepy.API(auth)

	LANGUAGE = "english"
	SENTENCES_COUNT = 5
	
	#Connect to SQLite
	con = lite.connect('./test.db')
	cur = con.cursor()  
	#Clear the Results table down
	cur.execute("DELETE FROM Results")
	con.commit()
	
	
	current_dt = datetime.datetime.now()
	counter = 1
	
	
	# ARGUMENTS SUPPLIED AT RUN TIME:
	list_owner = sys.argv[1]
	list_name   = sys.argv[2]
	importance_limit = float(sys.argv[3])
	age = int(sys.argv[4])
	outfile = list_owner + "_" + list_name + "_" + str(current_dt.year) + "_" + str(current_dt.month) + "_" + str(current_dt.day) + ".csv"
	
	result = open(outfile, "wb")
	writer = csv.writer(result, dialect = 'excel')
	
	# some lists to try: NickJewell bigdata-analytics  or lissted big-data-influencers   or NickJewell follow5 (small)
	
	# importance threshold of 50 seems to bring back a reasonable list
	

    #print api.me().name
    #api.update_status('Hello -tweepy + oauth!')lissted/big-data-influencers/
	
	looper = 1
    # Iterate through all members of the owner's list
	for member in tweepy.Cursor(api.list_members, list_owner, list_name).items():
		list_member =  member.screen_name
		print "**************************************"
		print "Processing: %i. %s "%(looper, list_member)
		looper = looper + 1
		#Don't hit the rate limit
		time.sleep(10)
		for status in tweepy.Cursor(api.user_timeline,id=list_member).items(25):
			all_list = []
			sumr = []
			tweet_dt = status.created_at
			tweet_age_days = (current_dt-tweet_dt).days
			
			text1 = re.sub(r'^https?:\/\/.*[\r\n]*', '', status.text, flags=re.MULTILINE)
			cleantext = re.sub(r"(?:\@|https?\://)\S+", "", text1)
			#print "%s\t%d"%(status.created_at, tweet_age_days)
			# Don't extract if tweet is older than 24 hours
			# Calculate importance using the formula below:
			rt_factor = 1.25
			fav_factor = 1.75
			imp_threshold = float(importance_limit)
			rt_score = status.retweet_count * rt_factor
			fav_score = status.favorite_count * fav_factor
			
			#Only save important tweets
			importance = rt_score * fav_score
			# Usually set to 1 for recent news filtering
			date_threshold = age
			#print importance, tweet_age_days
			
			if importance >= imp_threshold:
				if int(tweet_age_days) <= date_threshold:
				
			 
		             #blob_list = []
		             #print status.expanded_url
		             #for ht in status.entities['hashtags']:
		                 #ht_list.append(ht['text'])
		                 #all_list.append(ht['text'])
				 	all_list.append(cleantext.encode('utf-8'))
					for url in status.entities['urls']:
						expanded_url=url['expanded_url']
						
						try:
							  

								parser = HtmlParser.from_url(expanded_url, Tokenizer(LANGUAGE))
						    # or for plain text files
						    # parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))
								stemmer = Stemmer(LANGUAGE)

								summarizer = Summarizer(stemmer)
								summarizer.stop_words = get_stop_words(LANGUAGE)
							#print "****************GENERAL GIST******************************"
								for sentence in summarizer(parser.document, SENTENCES_COUNT):
								#all_list.append(sentence)
									test = tryit(sentence)
									sumr.append(test)
								#print test
								fix3 = ''.join(sumr)
								fix2 = fix3.replace('\'', '')
								fix1 = fix2.replace('\"', '')
								fix = strip_non_ascii(fix1)
								r= requests.head(expanded_url)
								if r.status_code in range (200,300):
								 #print "%s\t\t%i\n%s\n%s"%(list_member,importance, cleantext, format(r.url))
									all_list.append(list_member)
								 	all_list.append(status.retweet_count)
									all_list.append(status.favorite_count)
									all_list.append(importance)
									all_list.append(status.created_at)
									all_list.append(format(r.url))
								 
									inject = [counter, format(r.url), list_member, status.retweet_count, status.favorite_count, importance, status.created_at, fix]
									cur.execute("INSERT INTO Results VALUES(?,?,?,?,?,?,?,?)",inject)
									con.commit()
		                         #print format(r.url)
							 	elif r.status_code in range (300,400):
								 #print "%s\t\t%i\n%s\n%s"%(list_member,importance, cleantext, r.headers['location'])
								 	all_list.append(list_member)
								 	all_list.append(status.retweet_count)
								 	all_list.append(status.favorite_count)
								 	all_list.append(importance)
								 	all_list.append(status.created_at)
								 	all_list.append(r.headers['location'])
								 	inject = [counter, r.headers['location'], list_member, status.retweet_count, status.favorite_count, importance, status.created_at, fix]
								 	cur.execute("INSERT INTO Results VALUES(?,?,?,?,?,?,?,?)",inject)
								 	con.commit()
							 	else:
								 #print "%s\t\t%i\n%s\n%s"%(list_member,importance, cleantext, format(r.status_code))
								 all_list.append(list_member)
								 all_list.append(status.retweet_count)
								 all_list.append(status.favorite_count)
								 all_list.append(importance)
								 all_list.append(status.created_at)
								 all_list.append(format(r.status_code))
								 inject = [counter, format(r.status_code), list_member, status.retweet_count, status.favorite_count, importance, status.created_at, fix]
								 cur.execute("INSERT INTO Results VALUES(?,?,?,?,?,?,?,?)",inject)
								 con.commit()

		                         #print format(r.status_code)
								 continue

						except:
							e = sys.exc_info()[0]
							print "Error: %s\n"%(e)
							continue
						for ht in status.entities['hashtags']:
		                 #ht_list.append(ht['text'])
						 	all_list.append(ht['text'])
						#all_list.append(sumr)
					
						writer.writerow(all_list)
						counter = counter + 1
	con.close()
	
	# Now retrieve Results and order by Importance (with pretty print)
	print "\nHere's the Daily Buzz (in order of Importance):\n"
	con = lite.connect('./test.db')
	cursor = con.cursor()
	cursor.execute("select * from Results order by Imp Desc")
	
	for record in cursor.fetchall():
		print "Importance: %.2f\t%s"%(record[5], record[2])
		print "URL: %s"%(record[1])
		print "Highlights:\n%s\n\n"%(record[7])

             

   
def tryit(sentence):
	value = str(sentence)
	return value
	
def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)


if __name__ == '__main__':

	twitter_fetch()
	
	
	