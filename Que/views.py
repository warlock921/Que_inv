from django.shortcuts import render,get_object_or_404

from .models import Questionnaire,ChoiceQuestion,Choice,NonChoiceQuestion,AnswerSheet,SingleChoiceAnswer,MultiChoiceAnswer,TextAnswer,FileAnswer

def display_Que(request):
	que_title = Questionnaire.objects.all()
	return render(request,"Que/que_list.html",{"que_title":que_title})

def display_Que_content(request,que_id):
	que_content = get_object_or_404(Questionnaire,id=que_id)
	# print(que_content.question_name)
	pub = que_content.created_at
	que_choices_title = ChoiceQuestion.objects.filter(questionnaire_id=que_id)
	print(que_choices_title)
	que_choices = Choice.objects.filter(questionnaire_id=que_id)
	print(que_choices.count())
	return render(request,"Que/que_content.html",{"que_content":que_content,"pub":pub,"que_choices_title":que_choices_title,"que_choices":que_choices})
