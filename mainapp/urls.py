from django.conf.urls import url
from mainapp.views import *

__author__ = 'abuka'


urlpatterns = [
    url(r'^login/', login_view),
    url(r'^logout/', logout_view),
    url(r'^registration/', registration),

    url(r'^users/', users_list, name='user_list'),

    url(r'^categories/', category_list, name='category_list'),
    url(r'^addcategories/', add_category, name='add_category'),
    url(r'^deletecategories/', delete_category, name='delete_category'),

    url(r'^questions/', question_list, name='question_list'),
    url(r'^addquestion/', add_question, name='add_question'),

    url(r'^pool/', pool, name='pool'),
    url(r'^addtopool/', add_to_pool, name='add_to_pool'),

    url(r'^ranking/', rank_list, name='rank_list'),

    url(r'^friends/', friend_list, name='friend_list'),

    url(r'^gameinfo/', game_info, name='game_info'),

    # Saken's methods
    url(r'^getmyprofile/', get_my_profile, name='get_my_profile'),
    url(r'^getmycategorylist/', get_my_category_list, name='get_my_category_list'),
    url(r'^getmyrankbycategory/', get_my_rank_by_category, name='get_my_rank_by_category'),
    url(r'^getplayedgames/', get_played_games_list, name='get_played_games_list'),
    url(r'^getplayedgameinfo/', get_played_game_info, name='get_played_game_info'),
    url(r'^gameend/', game_end, name='game_end'),
    url(r'^getmyrank/', get_my_rank, name='get_my_rank'),
    url(r'^gameresult/', game_result, name='game_result'),
    url(r'^killsearch/', kill_search, name='kill_search'),

    # Script for reading from file
    url(r'^getdata/', get_data_from_file, name='get_data_from_file'),

]


