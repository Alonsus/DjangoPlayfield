from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from geopy.distance import vincenty
import time

import pygeoip

# Create your views here.

gi = pygeoip.GeoIP('static/GeoLiteCity.dat')

def indexView(request):
	# heroku hack
	ip = request.META.get('HTTP_X_FORWARDED_FOR', None)
	if ip is None:
		ip = request.META.get('REMOTE_ADDR', None)
	
	place = gi.record_by_addr(ip)
	niceAddress = "Unable to get place"
	template_name = 'geodistance/index.html'
	if place is not None:
		if place['metro_code'] is None:
			niceAddress = place['city']
		else:
			niceAddress = place['metro_code']
		
		if place['country_code3'] is not None:
			niceAddress = niceAddress + ', ' + place['country_code3']
		
	return render (request, template_name, {
		'place': place,
		'address': niceAddress,
		'ip': ip
	})
	
def calculate(request):
	ip = request.META.get('HTTP_X_FORWARDED_FOR', None)
	if ip is None:
		ip = request.META.get('REMOTE_ADDR', None)
	place = gi.record_by_addr(ip)
	localLatitude = place['latitude']
	localLongitude = place['longitude']
	remoteLatitude = request.POST['latitude']
	remoteLongitude = request.POST['longitude']
	output = "(" + str(localLatitude) + ", " + str(localLongitude) + ")  -  (" + str(remoteLatitude) + ", " + str(remoteLongitude) + ")"
	distance = vincenty((localLatitude, localLongitude), (remoteLatitude, remoteLongitude))
	time.sleep(1)
	return HttpResponse(distance )