import re
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
from .models import GameState
from .utils import find_paragraph_by_index


@login_required
def home(request):
    current_game_state = GameState.objects.get(player=request.user)

    paragraph_to_send = find_paragraph_by_index(current_game_state.current_paragraph)
    character_state = current_game_state.character_state

    # print(paragraph_to_send, character_state)
    return render(request, 'game/home.html', {'paragraph': paragraph_to_send, 'character_state': character_state})


def update_game_state(request):

    if request.method == 'POST':
        current_game_state = GameState.objects.get(player=request.user)
        json_data = json.loads(request.body) # request.raw_post_data w/ Django < 1.4
        try:
            player_choice = json_data['next_node']
            player_state = json_data['player_state']
            print(player_state, type(player_state))
            print(player_choice, type(player_choice))
            current_game_state.current_paragraph=player_choice
            current_game_state.character_state=player_state
            current_game_state.save()
        except KeyError:
            pass
        return JsonResponse({"ok":"ok"})


def get_current_game_state(request):
    if request.method == 'GET':
        current_game_state = GameState.objects.get(player=request.user)
        paragraph_to_send = find_paragraph_by_index(current_game_state.current_paragraph)
        character_state = json.dumps(current_game_state.character_state)
        return JsonResponse({"paragraph":paragraph_to_send, "character_state":character_state})
