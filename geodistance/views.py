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
# use static ip for testing
ip = '134.201.250.155' # los angeles
#ip = '94.253.190.183' # Zagreb

def indexView(request):
	# how it should be done
	#ip = request.META.get('REMOTE_ADDR', None)
	# heroku hack
	ip = request.META.get('HTTP_X_FORWARDED_FOR', None)
	
	
	place = gi.record_by_addr(ip)
	niceAddress = "Unable to get place"
	template_name = 'geodistance/index.html'
	if place is not None:
		if place['metro_code'] is None:
			niceAddress = place['city']
		else:
			niceAddress = place['metro_code']
		
		
		niceAddress = niceAddress + ', ' + place['country_code3']
		
		#place = "This is my new place"
	return render (request, template_name, {
		'place': place,
		'address': niceAddress,
		'ip': ip
	})
	
def calculate(request):
	place = gi.record_by_addr(ip)
	localLatitude = place['latitude']
	localLongitude = place['longitude']
	remoteLatitude = request.POST['latitude']
	remoteLongitude = request.POST['longitude']
	output = "(" + str(localLatitude) + ", " + str(localLongitude) + ")  -  (" + str(remoteLatitude) + ", " + str(remoteLongitude) + ")"
	distance = vincenty((localLatitude, localLongitude), (remoteLatitude, remoteLongitude))
	time.sleep(1)
	return HttpResponse(distance )