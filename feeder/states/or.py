#!/usr/bin/env python
import os
import feedparser
import psycopg2
import urlparse

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])
with psycopg2.connect(database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port) as dbconnect:
	cur = dbconnect.cursor()

	url = (
			'http://www.opb.org/feeds/all/',
			'http://www.ktvz.com/15237042?format=rss_2.0&view=feed',
			'http://kval.com/news/local.rss',
			'http://nbc16.com/news/local.rss',
			'http://www.kezi.com/templates/HL-RSS?type=Article&c=n&section=/news',
			'https://kobi5.com/category/news/local-news/feed/',
			'http://kunptv.com/news/local.rss',
			'https://kobi5.com/category/news/local-news/feed/',
			'http://ktvl.com/news/local.rss',
			'http://www.fox26medford.com/feed/',
			'http://katu.com/news/local.rss',
			'http://koin.com/category/news/local-news/feed/',
			'http://rssfeeds.kgw.com/kgw/local&x=1',
			'http://www.kptv.com/category/210845/app-news?clienttype=rss',
			'http://democratherald.com/search/?f=rss&t=article&c=news/local&l=25&s=start_time&sd=desc',
			'http://www.dailytidings.com/news?template=rss&mime=xml',
			'http://www.dailyastorian.com/section/rssfeed/1483&template=rss&mime=xml',
			'http://feeds.feedburner.com/bakercityherald/LeEi',
			'http://www.pamplinmedia.com/component/obrss/portland-tribune',
			'http://www.pamplinmedia.com/component/obrss/beaverton-valley-times',
			'http://feeds.feedburner.com/CurryCoastalPilot?format=xml',
			'http://btimesherald.com/feed/',
			'http://portlandtribune.com/component/obrss/canby-herald',
			'http://www.gazettetimes.com/search/?f=rss&t=article&c=news/local&l=25&s=start_time&sd=desc',
			'http://www.polkio.com/rss/headlines/news/',
			'http://www.eugeneweekly.com/rss/articles/News',
			'http://www.thesiuslawnews.com/TopStories.xml',
			'http://www.pamplinmedia.com/component/obrss/gresham-outlook',
			'http://www.oregonlive.com/news/atom.xml',
			'http://www.oregonlive.com/argus/atom.xml',
			'http://www.hoodrivernews.com/rss/headlines/news/',
			'http://www.heraldandnews.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://feeds.feedburner.com/LaGrandeObserver?format=xml',
			'http://www.pamplinmedia.com/component/obrss/lake-oswego-review',
			'http://lebanon-express.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.pamplinmedia.com/component/obrss/madras-pioneer',
			'http://www.mailtribune.com/news?template=rss&mime=xml',
			'http://www.pamplinmedia.com/component/obrss/molalla-pioneer',
			'http://www.pamplinmedia.com/component/obrss/newberg-graphic',
			'http://www.newportnewstimes.com/TopStories.xml',
			'http://www.argusobserver.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.eastoregonian.com/section/rssfeed/2117&template=rss&mime=xml',
			'http://djcoregon.com/news/category/news/feed/',
			'https://nwlaborpress.org/feed/',
			'http://keizertimes.com/feed/',
			'http://www.portlandmercury.com/portland/Rss.xml?section=22100',
			'https://wweek-feeds.partner.nile.works/api/v1/feeds/rss/',
			'http://portlandtribune.com/component/obrss/central-oregonian',
			# 'http://www.nrtoday.com/csp/mediapool/sites/SwiftShared/assets/csp/rssCategoryFeed.csp?pub=NewsReview&sectionId=564&sectionLabel=Local',
			'http://www.thechronicleonline.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://rssfeeds.statesmanjournal.com/salem/news&x=1',
			'http://www.willamettelive.com/category/news/feed/',
			'http://portlandtribune.com/component/obrss/sandy-post',
			'http://www.dailyastorian.com/section/rssfeed/1483&template=rss&mime=xml',
			'http://www.thedalleschronicle.com/rss/headlines/local/',
			'http://www.tillamookheadlightherald.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.pamplinmedia.com/component/obrss/wilsonville-spokesman',
			'http://www.pamplinmedia.com/component/obrss/woodburn-independent'

			)

	for link in url:
		d = feedparser.parse(link)

		for data in d.entries:


			title = data.title
			link = data.link
			try:
				time = data.published
			except AttributeError:
				try:
					time = d.feed.published
				except AttributeError:
					time = data.updated

			try: 
				imageUrl = data.links[1].href
			except (IndexError, AttributeError): 
				try:
					imageUrl = data.media_content[0]['url']
				except (AttributeError, KeyError):
					imageUrl = 'http://polar-spire-13485.herokuapp.com/static/img/logo3.png'

			source = d.feed.title
			location = "OR"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			