from django.shortcuts import render
from django.http import HttpResponse
import time

import pygeoip
from geopy.distance import vincenty

# grab data for IP addresses at the start
gi = pygeoip.GeoIP('static/GeoLiteCity.dat')

def getIpFromRequest(request):	
	# heroku hack
	ip = request.META.get('HTTP_X_FORWARDED_FOR', None)
	# if not heroku
	if ip is None:
		ip = request.META.get('REMOTE_ADDR', None)
	return ip

def getPlaceFromRequest(request):
	ip = getIpFromRequest(request)
	return gi.record_by_addr(ip)
	
# Index Page
def indexView(request):
	template_name = 'geodistance/index.html'
	place = getPlaceFromRequest(request)
	
	niceAddress = "Unable to get place"
	
	if place is not None:
		if place['metro_code'] is not None:
			# try to use "Los Angeles, CA" format
			niceAddress = place['metro_code']
		elif place['city'] is not None:
			# use "Los Angeles" if above not available
			niceAddress = place['city']
		else:
			# if city is unknown, display as such.
			niceAddress = "Unknown city"
			
		if place['country_code3'] is not None:
			# try to grab country code
			niceAddress = niceAddress + ', ' + place['country_code3']
		
	return render (request, template_name, {
		'address': niceAddress,
		'ip': getIpFromRequest(request)
	})

def calculate(request):
	place = getPlaceFromRequest(request)
	
	localLatitude = place['latitude']
	localLongitude = place['longitude']
	remoteLatitude = request.GET['latitude']
	remoteLongitude = request.GET['longitude']
	
	distance = vincenty((localLatitude, localLongitude), (remoteLatitude, remoteLongitude)).miles
	distance = str(round(distance,2)) + " mi"
	return HttpResponse(distance)