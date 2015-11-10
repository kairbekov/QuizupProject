from django.conf.urls import url
from mainapp.views import *

__author__ = 'abuka'


urlpatterns = [
    url(r'^login/', login_view),
    url(r'^logout/', logout_view),
    url(r'^registration/', registration),


    url(r'^categories/', category_list, name='category_list'),

    url(r'^addtopool/', add_to_pool, name='add_to_pool'),

    url(r'^ranking/', rank_list, name='rank_list'),

    url(r'^friends/', friend_list, name='friend_list'),

    # Android API methods
    url(r'^getmyprofile/', get_my_profile, name='get_my_profile'),
    url(r'^getmycategorylist/', get_my_category_list, name='get_my_category_list'),
    url(r'^getmyrankbycategory/', get_my_rank_by_category, name='get_my_rank_by_category'),
    url(r'^getplayedgames/', get_played_games_list, name='get_played_games_list'),
    url(r'^getplayedgameinfo/', get_played_game_info, name='get_played_game_info'),
    url(r'^gameend/', game_end, name='game_end'),
    url(r'^getmyrank/', get_my_rank, name='get_my_rank'),
    url(r'^gameresult/', game_result, name='game_result'),
    url(r'^killsearch/', kill_search, name='kill_search'),
    url(r'^getranking/', get_top_20, name='get_top_20'),
    url(r'^getfriends/', get_friends, name='get_friends'),

    #4 methods for rematch and invitation
    url(r'^iwanttoplaywithfriend/', i_want_to_play_with_friend, name='i_want_to_play_with_friend'),
    url(r'^whochallengeme/', who_challenge_me, name='who_challenge_me'),
    url(r'^answertochallenge/', answer_to_challenge, name='answer_to_challenge'),

    #url(r'^generate/', generateQuestions(category_id=1), name='generate'),

    # Script for reading from file
    url(r'^getdata/', get_data_from_file, name='get_data_from_file'),
    url(r'^readfile/', read_file, name='read_file'),
    url(r'^fromfiletodb/', from_file_to_db, name='from_file_to_db'),

    # Vk and Fb methods
    url(r'^login_sn/', login_social_network, name='login_social_network'),

    # play with bot
    url(r'^playwithbot/', play_with_bot, name='play_with_bot'),

    url(r'^clear/', clear, name='clear'),
    #url(r'^test/', test, name='test'),
    url(r'^search/', search_users, name='search'),

    url(r'^regid/', reg_id, name='reg_id'),
    url(r'^notification/', notification, name='notification'),

]
