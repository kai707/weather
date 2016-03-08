import urllib
import json
import sys
import argparse
try:
	from config import *
	config=True
except:
	config=False

def fetchweather(city, unit, sun=False, forecast=0, current=False):
	if type(forecast) is list:
		forecast = forecast[0]
	baseurl = "https://query.yahooapis.com/v1/public/yql?"
	query = "select * from weather.forecast where u='{unit}' and woeid in " \
			"(select woeid from geo.places(1) where text='{city}')"
	yql_url = baseurl + urllib.urlencode({'q':query.format(city=city, unit=unit), 'format':'json'})
	result = urllib.urlopen(yql_url).read()
	jsonresult = json.loads(result)
	data = jsonresult['query']['results']['channel']
	if current:
		print '%s, %s, %s%s' % \
			(data['location']['city'], data['item']['condition']['text'], \
			data['item']['condition']['temp'], unit.upper())
	if forecast > 0:
		forecast_format = "{date} {day} {low}~{high}{temp} {text}"
		for day in data['item']['forecast']:
			print forecast_format.format(date=day['date'], day=day['day'], temp=unit.upper(),\
				high=day['high'], low=day['low'], text=day['text'])
			forecast = forecast-1
			if forecast == 0:
				break
	if sun:
		print 'sunrise:%s, sunset:%s' % (data['astronomy']['sunrise'], data['astronomy']['sunset'])

def checkconfig():
	try:
		Location
	except NameError:
		return False
	try:
		Unit
	except NameError:
		return False
	return True

if len(sys.argv) == 1:
	if config:
		check = checkconfig()
		if check:
			try:
				Forecast
			except NameError:
				Forecast = 0
			try:
				Current
			except NameError:
				Current=False
			try:
				Sun
			except NameError:
				Sun=False
			try:
				Allinfo
				Forecast=5
				Current=True
			except NameError:
				Allinfo=False
			if Forecast>0 or Current or Sun:
				print 'load confit.py...'
				fetchweather(Location, Unit, Sun, Forecast, Current)
			else:
				print 'What do you want to do?'
	else:
		print 'Please enter the arguments or prepare the config.py'
else:
	parser = argparse.ArgumentParser(description='Get the weather of the city')
	parser.add_argument('-l', dest='city', nargs=1, help='locations', metavar = 'locaiton')
	parser.add_argument('-u', dest='unit', nargs=1, choices=['c','f'], \
						help='unit', metavar='unit')
	parser.add_argument('-s', action='store_true', help='sunset/sunrise', default=False)
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-c', action='store_true', help='current condition', default=False)
	group.add_argument('-a', action='store_true', help='equal to -c -d 5', default=False)
	group.add_argument('-d', dest='day', nargs=1, type=int, choices=range(1,6), \
					   help='forecast', metavar='day', default=0)
	args = parser.parse_args()
	if(args.city==None or args.unit==None):
		print 'Please enter location and unit'
	else:
		if args.s or args.day or args.c or args.a:
			if args.a:
				args.day =5
				args.c = True
			fetchweather(args.city[0], args.unit[0], args.s, args.day, args.c)
		else:
			print 'What do you want to do ?'
