from django.shortcuts import render
import json

def home(request):
    json_data = open("static/game-data.json")
    data1 = json.load(json_data)
    data2 = json.dumps(data1)
    json_data.close()
    return render(request, 'game/home.html', {'game_data':data2})