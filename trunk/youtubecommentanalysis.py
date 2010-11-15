#Daniel Souza
#Lab 04

import gdata.youtube
import gdata.youtube.service
import urllib2
import time
from Person import Commenter

#Uclassify 
#Read
#VwTa4ul5NrVCqyD147jT9vomcGg
#Write
#zQULlBKeMVoEdWHCMODT3LsqXVk

def AnalyzeComment(Comment):
	URL = "http://uclassify.com/browse/prfekt/Mood/ClassifyText?readkey=VwTa4ul5NrVCqyD147jT9vomcGg&text="+Comment.replace(" ", "+").replace("@","").replace("\n","").replace("\r","")
#Comment.replace(" ", "+")
	#print URL

	response = urllib2.urlopen(URL)

	html = response.read()
	#error handling
	req = urllib2.Request(URL)
	try:
		response = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		print 'The server couldn\'t fulfill the request.'
		print 'Error code: ', e.code
	except urllib2.URLError, e:
		print 'We failed to reach a server.'
		print 'Reason: ', e.reason
	else:
		#<status success="true" statusCode="2000"/>
		#<readCalls>
		#<classify id="cls1">
		#	<classification>
#				<class className="happy" p="0.585561"/>

		# everything is fine
		for line in html.splitlines():
			if line.rfind('className="happy"') >=0:
				#print line.rfind('className="happy"'),line 
				happy = float(line.replace("<","").replace("class","").replace("Name","").replace("happy","").replace("=","").replace("/>","").replace('"',"").replace("p",""))
				return happy, 1-happy
				



def GetUserUploadsFeed(username):
	yt_service = gdata.youtube.service.YouTubeService()
	uri = 'http://gdata.youtube.com/feeds/api/users/%s/uploads' % username
	return yt_service.GetYouTubeVideoFeed(uri)

def GetSearchFeed(search_terms):
	query = gdata.youtube.service.YouTubeVideoQuery()
	query.vq = search_terms
	query.orderby = 'viewCount'
	query.racy = 'include'
	return yt_service.YouTubeQuery(query)

def GetRelatedFeed(video_id):
	return yt_service.GetYouTubeRelatedVideoFeed

def Login(email, password):
	yt_service.email = email
	yt_service.password = password
	yt_service.source = 'my-example-application'
	yt_service.developer_key = 'AI39si7JxcEVDfPMZvcvw9rXyXNtSBhwzQiQTyTsGm4PTIU-TUDXkvy2fcpQpJggdYpW0zI4-u5QHs6_s8RHqYVV_ujUh8m-rg'
	yt_service.client_id = 'webscitest'
	yt_service.ProgrammaticLogin()
def PrintEntryDetails(entry):
	print 'Video title: %s' % entry.media.title.text
	print 'Video published on: %s ' % entry.published.text
	print 'Video description: %s' % entry.media.description.text
	print 'Video category: %s' % entry.media.category[0].text
	print 'Video tags: %s' % entry.media.keywords.text
	print 'Video watch page: %s' % entry.media.player.url
	print 'Video flash player URL: %s' % entry.GetSwfUrl()
	print 'Video duration: %s' % entry.media.duration.seconds

	# non entry.media attributes
#	print 'Video geo location: %s' % entry.geo.location()
	print 'Video view count: %s' % entry.statistics.view_count
	print 'Video rating: %s' % entry.rating.average

	# show alternate formats
	for alternate_format in entry.media.content:
		if 'isDefault' not in alternate_format.extension_attributes:
			print 'Alternate format: %s | url: %s ' % (alternate_format.type,
                                                 alternate_format.url)

	  # show thumbnails
	for thumbnail in entry.media.thumbnail:
		print 'Thumbnail url: %s' % thumbnail.url

def PrintUserEntry(user):
  # print required fields where we know there will be information
#  print 'URI: %s\n' % user.id.text
  age = None
  if user.age:
    print 'Age: %s\n' % user.age.text
    age = int(user.age.text)
  gender = None
  if user.gender:
    print 'Gender: %s\n' % user.gender.text
    gender = user.gender.text
  location = None
  if user.location:
    print 'Location: %s\n' % user.location.text
    location = user.location.text
  return gender, age, location
  # check if there is information in the other fields and if so print it
#  if user.first_name: 
#    print 'First Name: %s\n' % user.first_name.text
#  if user.last_name:
#    print 'Last Name: %s\n' % user.last_name.text
#  if user.relationship:
#    print 'Relationship: %s\n' % user.relationship.text
#  if user.description:
#    print 'About me: %s\n' % user.description.text
#  for link in user.link:
#    if link.rel == 'related':
#      print 'Website: %s\n' % link.href
#  if user.company:
#    print 'Company: %s\n' % user.company.text
#  if user.occupation:
#    print 'Occupation: %s\n' % user.occupation.text
#  if user.school:
#    print 'School: %s\n' % user.school.text
#  if user.hobbies:
#    print 'Hobbies: %s\n' % user.hobbies.text
#  if user.movies:
#    print 'Movies: %s\n' % user.movies.text
#  if user.music:
#    print 'Music: %s\n' % user.music.text
#  if user.books:
#    print 'Books: %s\n' % user.books.text
  if user.hometown:
    print 'Hometown: %s\n' % user.hometown.text

video_uri = "http://www.youtube.com/watch?v=9SnQOdEXbNQ"
video_ID = "9SnQOdEXbNQ"
#Login Example
yt_service = gdata.youtube.service.YouTubeService()
entry = yt_service.GetYouTubeVideoEntry(video_id=video_ID)
PrintEntryDetails(entry)

AnalyzeComment("This video is great...")

print "Comments:"
try:
	feed = yt_service.GetYouTubeVideoCommentFeed(video_id=video_ID)
except gdata.service.RequestError, e:
	print "Request Error: ", e
else:

	happy_total = 0
	sad_total = 0
	total = 0
	#1000 Cap
	people = []
	for x in xrange(0,39):
		for entry in feed.entry:
			print entry.content.text #comment
			print entry.published.text #date
			happy, sad = AnalyzeComment(entry.content.text)
			print "Positive: ", happy
			print "Negative: ", sad
			for a in entry.author:
				try:
					user_entry = yt_service.GetYouTubeUserEntry(username=a.name.text)
				except gdata.service.RequestError, e:
					print "Request Error: ", e
					gender, age, location = None, None, None
					people.append(Commenter(entry.content.text, entry.published.text,happy,sad, gender, age, location))
				else:
					gender, age, location = PrintUserEntry(user_entry)
					people.append(Commenter(entry.content.text, entry.published.text,happy,sad, gender, age, location))
		
			happy_total += happy
			sad_total += sad
			total += 1
		feed = yt_service.Query(feed.GetNextLink().href)
	print people
	print "Overall Positive: ", happy_total/total
	print "Overall Negative: ", sad_total/total
	

