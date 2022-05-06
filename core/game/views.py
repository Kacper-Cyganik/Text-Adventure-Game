from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import SaveSlot
from .utils import find_paragraph_by_index
import json


@login_required
def home(request):
    return render(request, 'game/home.html')


def update_game_state(request):

    if request.method == 'POST':
        current_game_state, created = SaveSlot.objects.get_or_create(player=request.user)
        json_data = json.loads(request.body)

        current_game_state.current_paragraph = json_data.get('next_node', 1)
        current_game_state.character_state = json_data.get('player_state', {})
        current_game_state.save()

        return JsonResponse({"staus": "201"})
    else:
        return JsonResponse({"status": "403"})


def get_current_game_state(request):
    if request.method == 'GET':
        current_game_state = SaveSlot.objects.get(player=request.user)
        paragraph_to_send = find_paragraph_by_index(
            current_game_state.current_paragraph)
        character_state = json.dumps(current_game_state.character_state)
        return JsonResponse({"paragraph": paragraph_to_send, "character_state": character_state})
    else:
        return JsonResponse({"status": "403"})



# CHANGE TO REST, ADD SAVE SLOTS, CREATE BETTER STORY