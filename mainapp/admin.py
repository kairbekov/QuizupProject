from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.utils.translation import ugettext_lazy
from mainapp.models import *

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subcategory')

class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'question_text', 'answer_1', 'answer_2', 'answer_3', 'answer_4', 'correct_answer', 'level')

class PoolAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'user_id', 'rank')

class RankingAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'user_id', 'rank')

class FriendsAdmin(admin.ModelAdmin):
    list_display = ('user_id_1', 'user_id_2')

class GameInfoAdmin(admin.ModelAdmin):
    list_display = ('user_id_1', 'user_id_2', 'game_id', 'category_id', 'game_status', 'point_1', 'point_2')

class GameAdmin(admin.ModelAdmin):
    list_display = ('question_id_1', 'question_id_2', 'question_id_3', 'question_id_4', 'question_id_5', 'user1_answer_id', 'user2_answer_id')

class UserAnswerListAdmin(admin.ModelAdmin):
    list_display = ('user_answer_1', 'user_answer_2', 'user_answer_3', 'user_answer_4', 'user_answer_5', 'point_1', 'point_2', 'point_3', 'point_4', 'point_5')

class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'vk_id', 'fb_id', 'city', 'avatar', 'total_points')

class InvitationAdmin(admin.ModelAdmin):
    list_display = ('id', 'game_id', 'challenger_id', 'status')


admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Questions, QuestionsAdmin)
admin.site.register(Pool, PoolAdmin)
admin.site.register(Ranking, RankingAdmin)
admin.site.register(Friends, FriendsAdmin)
admin.site.register(GameInfo, GameInfoAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(UserAnswerList, UserAnswerListAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Invitation, InvitationAdmin)