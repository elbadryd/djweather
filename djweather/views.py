from django.shortcuts import render
import os, requests
from .models import City
from .forms import CityForm


# Create your views here.
def index(request):
    print(request)
    key = os.environ['WEATHER_API']
    cities = City.objects.all()
    form = CityForm()
    weather_data = []
    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate
    form = CityForm()
    if request.method == "DELETE":
        print(request, 'req')
    for city in cities:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city.name}&units=imperial&appid={key}'
        city_weather = requests.get(url).json()
        weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }
        weather_data.append(weather)
    context = {
        'weather_data' : weather_data,
        'form' : form,
    } 
    return render(request, 'weather/weather.html', context)