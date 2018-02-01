from django.contrib import admin
from .models import AnswerUser,Questionnaire,ChoiceQuestion,Choice,NonChoiceQuestion,AnswerSheet,SingleChoiceAnswer,MultiChoiceAnswer,TextAnswer,FileAnswer

class AnswerUserAdmin(admin.ModelAdmin):
	list_display = ('company_name', 'answer_post', 'person_incharge_name', 'user_sex','user_age','user_edu','user_phone','user_fax','user_address','establishment_time','company_url','company_email')
	list_filter = ("company_name","user_phone")
	search_fields = ['company_name']

class ChoiceQuestionInline(admin.TabularInline):
	model = ChoiceQuestion
	extra = 5

class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 5

class QuestionnaireAdmin(admin.ModelAdmin):
	list_display = ('question_name', 'questionnaire_description', 'created_at', 'modified_at','is_active','user')
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

admin.site.register(AnswerUser,AnswerUserAdmin)
admin.site.register(Questionnaire,QuestionnaireAdmin)
admin.site.register(ChoiceQuestion,ChoiceQuestionAdmin)
admin.site.register(Choice,ChoiceAdmin)
admin.site.register(NonChoiceQuestion)
