
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get-current-game-state', views.get_current_game_state, name='get-current-game-state'),
    path('update-game-state', views.update_game_state, name='update-game-state'),

]
