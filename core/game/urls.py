
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('game/get-current-game-state', views.get_current_game_state, name='get-current-game-state'),
    path('game/update-game-state', views.update_game_state, name='update-game-state'),
    path('game/update-save-slot', views.update_save_slot, name='update-save-slot'),
    path('game/get-save-slots', views.get_save_slots, name='get-save-slots'),

]
