#!/usr/bin/env python

import feedparser
import psycopg2

with psycopg2.connect("dbname ='feedparser' user ='admin' password= 'admin' host = 'localhost' ") as dbconnect:
	cur = dbconnect.cursor()

	url = ('http://www.news9.com/category/211667/news9com-news-rss?clienttype=rss',
			'http://www.koco.com/9844956?format=rss_2.0&view=feed',
			'http://www.kswo.com/category/216452/kpho-newstream?clienttype=rss'
			'http://ktul.membercenter.worldnow.com/global/category.asp?C=189710&clienttype=rss',
			'http://www.newson6.com/category/208401/newson6com-news-rss?clienttype=rss',
			'http://www.fox23.com/feeds/rssFeed?obfType=RSS_DETAIL&siteId=600013&categoryId=500001',
			'http://www.krmg.com/list/rss/news/local/top-local-stories/aPM/',
			'http://publicradiotulsa.org/feeds/term/49/rss.xml',   
			'http://www.choctawnation.com/rss',
			'http://www.tulsaworld.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss', 
			'http://www.baptistmessenger.com/feed/',
			'http://okmulgeenews.net/local-news?format=feed',
			'http://swoknews.com/rss.xml',
			'http://www.woodwardnews.net/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local_news,news/local_news/*&f=rss',
			'http://www.miamiok.com/news?template=rss&mime=xml',
			'http://www.ardmoreite.com/news?template=rss&mime=xml',
			'http://examiner-enterprise.com/news/local-news/feed',
			'http://www.ocolly.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.oudaily.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/state*&f=rss',
			'http://www.news-star.com/news?template=rss&mime=xml'

			)

	for link in url:
		d = feedparser.parse(link)

		for data in d.entries:


			title = data.title
			link = data.link
			time = data.published
			try: 
				imageUrl = data.links[1].href
			except IndexError: 
				try:
					imageUrl = data.media_content[0]['url']
				except AttributeError:
					imageUrl = ''

			source = d.feed.title

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source) VALUES (%s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source,))
				dbconnect.commit()
			except psycopg2.IntegrityError:
				dbconnect.rollback()
				print 'Already stored:'

				

			# print title,'\n', link, '\n',time,'\n', imageUrl,'\n', source, '\n'




# with open ('parsed.txt', 'wb') as parsed:


# 	datalist = []
# 	for data in d.entries:
# 		title = data.title
# 		date = data.published
# 		description = data.description
# 		image = data.links[1].href

# 	parsed.write(data)

	# 	datalist.append(data)
	# str(datalist)
	# parsed.write(datalist)