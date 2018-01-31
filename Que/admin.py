from django.contrib import admin
from .models import Questionnaire,ChoiceQuestion,Choice,NonChoiceQuestion,AnswerSheet,SingleChoiceAnswer,MultiChoiceAnswer,TextAnswer,FileAnswer

class ChoiceQuestionInline(admin.TabularInline):
	model = ChoiceQuestion
	extra = 5

class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 5

class QuestionnaireAdmin(admin.ModelAdmin):
	list_display = ('question_name', 'created_at', 'modified_at','is_active','user')
	list_filter = ("question_name","user")
	search_fields = ['question_name']

	#自定义管理界面--可以管理问卷对应的问题
	inlines = [ChoiceQuestionInline]


class ChoiceQuestionAdmin(admin.ModelAdmin):
	list_display = ('question','required','questionnaire','order_in_list','created_at','multi_choice')
	list_filter = ("question",)
	search_fields = ['question']

	#自定义管理界面--可以管理问题对应的选项
	inlines = [ChoiceInline]

class ChoiceAdmin(admin.ModelAdmin):
	list_display = ('question','questionnaire','descripiton','order_in_list','multi_choice')
	list_filter = ("question",)
	search_fields = ['question']

admin.site.register(Questionnaire,QuestionnaireAdmin)
admin.site.register(ChoiceQuestion,ChoiceQuestionAdmin)
admin.site.register(Choice,ChoiceAdmin)
admin.site.register(NonChoiceQuestion)
