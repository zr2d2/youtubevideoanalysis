#Daniel Souza
#Lab 04

import gdata.youtube
import gdata.youtube.service
import urllib2
import time
import random
import csv

from Person import Commenter

#Uclassify 
#Read
#VwTa4ul5NrVCqyD147jT9vomcGg
#Write
#zQULlBKeMVoEdWHCMODT3LsqXVk

def analyze_comment(Comment):
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
				if happy <= .4:
					return happy, 1, 0, 0
				if happy <= .6:
					return happy, 0, 1, 1
				else:
					return happy, 0, 1, 0
				

def AnalyzeGender(Comment):
	URL = "http://uclassify.com/browse/uClassify/GenderAnalyzer_v5/ClassifyText?readkey=VwTa4ul5NrVCqyD147jT9vomcGg&text="+Comment.replace(" ", "+").replace("@","").replace("\n","").replace("\r","")
#Comment.replace(" ", "+")

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
			if line.rfind('className="female"') >=0:
				#print line.rfind('className="happy"'),line 
				female = float(line.replace("<","").replace("class","").replace("Name","").replace("female","").replace("=","").replace("/>","").replace('"',"").replace("p",""))
				print female
				if female > .5:
					return "f"
				else:
					return "m"

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


NORTHEAST = ["Connecticut", "Maine",  "Massachusetts",  "New Hampshire", "Rhode Island", "Vermont", "CT", "ME", "MA", "NH", "RI", "VT"]
MIDWEST = ["Illinois", "Indiana", "Iowa", "Kansas", "Michigan", "Minnesota", "Missouri", "Nebraska", "North Dakota", "South Dakota", "Ohio", "Wisconsin", "IL", "IN", "IA", "KS", "MI", "MN", "NE", "ND", "SD", "OH", "WI"]
SOUTH = ["Florida", "Georgia", "Maryland", "North Carolina", "South Carolina", "Virginia", "West Virginia", "Delaware", "Alabama", "Kentucky", "Mississippi", "Tennessee", "Arkansas", "Louisiana", "Oklahoma", "Texas", "FL", "GA", "MD", "NC", "SC", "VA", "DE", "AL", "KY", "MS", "TN", "AR", "LA", "OK", "TX"]
WEST = ["Alaska", "Arizona", "California", "Colorado", "Hawaii", "Idaho", "Montana", "Nevada", "New Mexico", "Oregon", "Utah", "Washington", "Wyoming", "AK", "AZ", "CA", "CO", "HI", "ID", "MT", "NV", "NM", "OR", "UT", "WA"]
UNITEDSTATES = ["United States of America", "United States", "US"]

def located_in(places, place):
	for p in places:
		if place.find(p) >= 0:
			return True
	return False

def analyze_location(location):
	if location:
		if located_in(NORTHEAST, location):
			return .34, .54, .12
		if located_in(MIDWEST, location):
			return .38, .50, .12
		if located_in(SOUTH, location):
			return .40, .49, .11
		if located_in(WEST, location):
			return .36, .53, .11
	return .38, .51, .11

def analyze_online():
	return .39, .3, .31

def analyze_age(age):
	if age >= 18 and age <= 29:
		return .33, .32, .34
	elif age >= 30:
		return .44, .45, .1
	else:
		return .38, .51, .11

def analyze_gender(gender):
	if gender == "m":
		return .28, .32, .34
	else:
		return .25, .41, .26
AGE_WEIGHT = .25
GEN_WEIGHT = .25
LOC_WEIGHT = .25
DIS_WEIGHT = .15
ONL_WEIGHT = .1
def AnalyzeCommenter(p):
	Republican = 0
	Democrat = 0
	Independent = 0

	R,D,I = analyze_age(p.age)
	Republican += AGE_WEIGHT * R
	Democrat += AGE_WEIGHT * D
	Independent += AGE_WEIGHT * I

	R,D,I = analyze_gender(p.gender)
	Republican += GEN_WEIGHT * R
	Democrat += GEN_WEIGHT * D
	Independent += GEN_WEIGHT * I

	R,D,I = analyze_location(p.location)
	Republican += LOC_WEIGHT * R
	Democrat += LOC_WEIGHT * D
	Independent += LOC_WEIGHT * I

	h,R,D,I = analyze_comment(p.comment)
	Republican += DIS_WEIGHT * R
	Democrat += DIS_WEIGHT * D
	Independent += DIS_WEIGHT * I
	
	R,D,I = analyze_online()
	Republican += ONL_WEIGHT * R
	Democrat += ONL_WEIGHT * D
	Independent += ONL_WEIGHT * I

	r = random.random()
	if r <= Republican:
		return "r"
	if r <= Republican + Democrat:
		return "d"
	else:
		return "i"
	
def PrintUserEntry(user,comment):
  # print required fields where we know there will be information
#  print 'URI: %s\n' % user.id.text
  age = None
  if user.age:
#    print 'Age: %s\n' % user.age.text
    age = int(user.age.text)
  gender = None
  if user.gender:
#    print 'Gender: %s\n' % user.gender.text
    gender = user.gender.text
  else:
    gender = AnalyzeGender(comment)
  location = None
  if user.location:
#    print 'Location: %s\n' % user.location.text
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

def writetofile(filename, headings, values):
	writer = csv.writer(open(filename, 'wb'), delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	l = []
	for h in headings:
		l.append(unicode(h,"utf-8"))
	writer.writerow(l)
	l = []
	for v in values:
		l.append(v)		
	writer.writerow(l)

from pychart import *
import sys

print "Gathering Comments"
try:
	feed = yt_service.GetYouTubeVideoCommentFeed(video_id=video_ID)
except gdata.service.RequestError, e:
	print "Request Error: ", e
	time.sleep(180)
	feed = yt_service.GetYouTubeVideoCommentFeed(video_id=video_ID)
else:
	analyze_age(12)
	happy_total = 0
	sad_total = 0
	total = 0
	people = []
	#1000 Cap
	for x in xrange(0,1):
		for entry in feed.entry:
#			print entry.content.text #comment
#			print entry.published.text #date
			for a in entry.author:
				try:
					user_entry = yt_service.GetYouTubeUserEntry(username=a.name.text)
				except gdata.service.RequestError, e:
					print "Request Error: ", e
					gender, age, location = None, None, None
					people.append(Commenter(entry.content.text, entry.published.text, gender, age, location))
				else:
					gender, age, location = PrintUserEntry(user_entry, entry.content.text)
					people.append(Commenter(entry.content.text, entry.published.text, gender, age, location))
	
		try:
			feed = yt_service.Query(feed.GetNextLink().href)
		except gdata.service.RequestError, e:
			time.sleep(180)
			feed = yt_service.Query(feed.GetNextLink().href)
	Independent = 0
	Democrat = 0
	Republican = 0
	
	NE = [0, 0, 0, 0]
	MW = [0, 0, 0, 0]
	SO = [0, 0, 0, 0]
	WE = [0, 0, 0, 0]
	US = [0, 0, 0, 0]
	OT = [0, 0, 0, 0]

	Male = [0, 0, 0, 0]
	Female = [0, 0, 0, 0]

	Teen = [0, 0, 0, 0]
	YoungAdult = [0, 0, 0, 0]
	Adult = [0, 0, 0, 0]
	Senior = [0, 0, 0, 0]
	
	T = 0 #Total
	R = 1 #Republican
	D = 2 #Democrat
	I = 3 #Indepndent
	
	for p in people:
		Party = AnalyzeCommenter(p)
		if Party == "r":
			Republican += 1
		if Party == "d":
			Democrat += 1
		if Party == "i":
			Independent += 1
		if p.location:
			if located_in(NORTHEAST, p.location):
				NE[T] += 1
				if Party == "r":
					NE[R] += 1
				if Party == "d":
					NE[D] += 1
				if Party == "i":
					NE[I] += 1
			elif located_in(MIDWEST, p.location):
				MW[T] += 1
				if Party == "r":
					MW[R] += 1
				if Party == "d":
					MW[D] += 1
				if Party == "i":
					MW[I] += 1
			elif located_in(SOUTH, p.location):
				SO[T] += 1
				if Party == "r":
					SO[R] += 1
				if Party == "d":
					SO[D] += 1
				if Party == "i":
					SO[I] += 1
			elif located_in(WEST, p.location):
				WE[T] += 1
				if Party == "r":
					WE[R] += 1
				if Party == "d":
					WE[D] += 1
				if Party == "i":
					WE[I] += 1
			elif located_in(UNITEDSTATES,p.location):
				US[T] +=1
				if Party == "r":
					US[R] += 1
				if Party == "d":
					US[D] += 1
				if Party == "i":
					US[I] += 1
			else:
				OT[T] +=1
				if Party == "r":
					OT[R] += 1
				if Party == "d":
					OT[D] += 1
				if Party == "i":
					OT[I] += 1
		else:
			OT[0] += 1
			if Party == "r":
				OT[R] += 1
			if Party == "d":
				OT[D] += 1
			if Party == "i":
				OT[I] += 1
		if p.gender == "m":
			Male[T] += 1
			if Party == "r":
				Male[R] += 1
			if Party == "d":
				Male[D] += 1
			if Party == "i":
				Male[I] += 1
		else:
			Female[T] += 1
			if Party == "r":
				Female[R] += 1
			if Party == "d":
				Female[D] += 1
			if Party == "i":
				Female[I] += 1

		if p.age < 18:
			Teen[T] += 1
			if Party == "r":
				Teen[R] += 1
			if Party == "d":
				Teen[D] += 1
			if Party == "i":
				Teen[I] += 1
		elif p.age < 30:
			YoungAdult[T] += 1
			if Party == "r":
				YoungAdult[R] += 1
			if Party == "d":
				YoungAdult[D] += 1
			if Party == "i":
				YoungAdult[I] += 1
		elif p.age < 60:
			Adult[T] += 1
			if Party == "r":
				Adult[R] += 1
			if Party == "d":
				Adult[D] += 1
			if Party == "i":
				Adult[I] += 1
		else:
			Senior[T] += 1
			if Party == "r":
				Senior[R] += 1
			if Party == "d":
				Senior[D] += 1
			if Party == "i":
				Senior[I] += 1

	writetofile("party.csv",["Republican","Democrat","Independent"],[Republican,Democrat,Independent])
	print "R: ",Republican, float(Republican)/len(people)
	print "D: ",Democrat, float(Democrat)/len(people)
	print "I: ",Independent, float(Independent)/len(people)
	writetofile("location.csv",["Northeast","Midwest","South","West","US","Other"],[NE[T],MW[T],SO[T],WE[T],US[T],OT[T]])
	writetofile("locationparty.csv",["Northeast Republican", "Northeast Democrat", "Northeast Independent","Midwest Republican", "Midwest Democrat", "Midwest Independent","South Republican", "South Democrat", "South Independent","West Republican", "West Democrat", "West Independent"], [NE[R],NE[D],NE[I],MW[R],MW[D],MW[I],SO[T],SO[R],SO[D],SO[I],WE[R],WE[D],WE[I]])
	print "NE: ",NE, float(NE[T])/len(people)
	print "MW: ",MW, float(MW[T])/len(people)
	print "SO: ",SO, float(SO[T])/len(people)
	print "WE: ",WE, float(WE[T])/len(people)
	print "US: ",US, float(US[T])/len(people)
	print "OT: ",OT, float(OT[T])/len(people)
	writetofile("gender.csv", ["Male","Female"],[Male[T],Female[T]])
	writetofile("genderparty.csv", ["Male Republican", "Male Democrat", "Male Independent", "Female Republican", "Female Democrat", "Female Independent"], [Male[R],Male[D],Male[I],Female[R],Female[D],Female[I]])
	print "M: ",Male, float(Male[T])/len(people)
	print "F: ",Female, float(Female[T])/len(people)
	writetofile("age.csv",["0-17","18-29","30-60","60+"],[Teen[T],YoungAdult[T],Adult[T],Senior[T]])
	writetofile("age.csv",["0-17 Republican","0-17 Democrat","0-17 Independent","18-29 Republican","18-29 Democrat","18-29 Independent","30-60 Republican","30-60 Democrat","30-60 Independent","60+ Republican","60+ Democrat", "60+ Independent"],[Teen[R],Teen[D],Teen[I],YoungAdult[R],YoungAdult[D],YoungAdult[I],Adult[R],Adult[D],Adult[I],Senior[R],Senior[D],Senior[I]])
	print "0-17: ",Teen, float(Teen[T])/len(people)
	print "18-29: ",YoungAdult, float(YoungAdult[T])/len(people)
	print "30-60: ",Adult, float(Adult[T])/len(people)
	print "60+: ",Senior, float(Senior[T])/len(people)

