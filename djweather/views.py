from django.shortcuts import render, redirect
import os, requests
from django.http import Http404
from .models import City
from .forms import CityForm
import operator


# Create your views here.
def index(request):
    key = os.environ['WEATHER_API']
    cities = City.objects.all()
    form = CityForm()
    weather_data = []
    url = 'http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid={key}'
    if request.method == 'DELETE':
        print(request.DELETE)
    if request.method == 'POST':
        city_name = request.POST['name']
        res = requests.get(url.format(city=city_name,key=key)).json()
        if res['cod'] != 200:
            form = CityForm()
        else:
            form = CityForm(request.POST) # add actual request data to form for processing
            form.save() # will validate and save if validate
            form = CityForm()
    for city in cities:
        print(city.id)
        
        city_weather = requests.get(url.format(city=city.name,key=key)).json()
        weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon'],
            'id' : city.id
        }
        weather_data.append(weather)
    context = {
        'weather_data' : weather_data,
        'form' : form,
    } 
    return render(request, 'weather/weather.html', context)

def city_detail_view(request, id):
    try:
        obj = City.objects.get(id=id)
    except City.DoesNotExist:
        raise Http404
    if request.method == "POST":
        obj.delete()
        return redirect('../')
    context = {
        "weather": obj
        }
    return render(request, "weather/city_detail.html", context)