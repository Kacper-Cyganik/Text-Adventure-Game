from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import SaveSlot
from .utils import find_paragraph_by_index
import json


@login_required
def home(request):
    return render(request, 'game/home.html')


# SAVE SLOTS

@login_required
def update_save_slot(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        save_slot_id = json_data.get('save_slot_id', 1)
        save_slot = SaveSlot.objects.get(player=request.user, slot_id=save_slot_id)
        print(save_slot)
        request.user.profile.active_slot = save_slot
        request.user.save()
        return JsonResponse({"status": "201"})
    else:
        return JsonResponse({"status": "403"})


@login_required
def get_save_slots(request):
    if request.method == 'GET':
        save_slots = SaveSlot.objects.filter(player=request.user)

        data_to_send = []
        for save_slot in save_slots:
            data_to_send.append({'saveSlotId':save_slot.slot_id, 'lastModified':str(save_slot.last_modified.strftime('%m/%d/%Y %H:%M'))})
        json_data_to_send = json.dumps(data_to_send) 
        print(json_data_to_send)
        return JsonResponse({"saveSlotData":json_data_to_send})
    else:
        return JsonResponse({"status": "403"})


# # #

@login_required
def update_game_state(request):

    if request.method == 'POST':
        current_game_state = request.user.profile.active_slot
        json_data = json.loads(request.body)

        current_game_state.current_paragraph = json_data.get('next_node', 1)
        current_game_state.character_state = json_data.get('player_state', {})
        current_game_state.save()

        return JsonResponse({"staus": "201"})
    else:
        return JsonResponse({"status": "403"})


@login_required
def get_current_game_state(request):
    if request.method == 'GET':
        #user_profile = request.user.profile.active_slot
        current_game_state = request.user.profile.active_slot
        print('--------------------------')
        print(current_game_state)
        print('--------------------------')
        # print(user_profile)
        paragraph_to_send = find_paragraph_by_index(
            current_game_state.current_paragraph)
        character_state = json.dumps(current_game_state.character_state)
        return JsonResponse({"paragraph": paragraph_to_send, "character_state": character_state})
    else:
        return JsonResponse({"status": "403"})
