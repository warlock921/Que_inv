from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class AnswerUser(models.Model):
	company_name = models.CharField(max_length=200,verbose_name="企业名称",unique=True)
	answer_post = models.CharField(max_length=50,verbose_name="被调查者职务或职称")
	person_incharge_name = models.CharField(max_length=50,verbose_name="负责人姓名")
	user_sex = models.SmallIntegerField(verbose_name="性别", choices=((0,"男"),(1,"女")), default=0)
	user_age = models.SmallIntegerField(verbose_name="年龄", choices=((0,"30岁以下"),(1,"31—40岁"),(2,"41—50岁"),(3,"51岁以上")), default=1)
	user_edu = models.SmallIntegerField(verbose_name="文化程度", choices=((0,"初中"),(1,"高中（中专）"),(2,"大专"),(3,"本科"),(4,"本科以上")),default=2)
	user_phone = models.CharField(max_length=11,verbose_name="手机")
	user_fax = models.CharField(max_length=11,blank=True,verbose_name="传真")
	user_address = models.CharField(max_length=200,verbose_name="通讯地址")
	establishment_time = models.DateField(editable=True,verbose_name="企业成立时间")
	company_url = models.URLField(max_length=500,blank=True,verbose_name="企业网址")
	company_email = models.EmailField(verbose_name="邮箱")

	def __str__(self):
		return self.company_name

	class Meta:
		ordering = ["-company_name"]
		verbose_name = "用户信息管理"
		verbose_name_plural = "用户信息管理"


#这是对问卷的抽象Model--整个问卷的抽象
class Questionnaire(models.Model):
	question_name = models.CharField(max_length=200,null=True,verbose_name="问卷名称")
	questionnaire_description = models.TextField(blank=True,verbose_name="问卷说明")
	created_at = models.DateTimeField(default=timezone.now, editable=False ,verbose_name="创建时间")
	modified_at = models.DateTimeField(default=timezone.now, editable=False, verbose_name="修改时间")
	is_active = models.BooleanField(default=True, verbose_name="是否显示")

	participants = models.ManyToManyField(AnswerUser,related_name="Que_participants", verbose_name="参与者")
	user = models.ForeignKey(User,related_name="Que_user", verbose_name="创建者")

	def __str__(self):
		return self.question_name

	class Meta:
		ordering = ["-created_at"]
		verbose_name = "问卷管理"
		verbose_name_plural = "问卷管理"

#问题的抽象基类---基类是抽象类，不可以在后台管理添加，否则报错
class Question(models.Model):
	"""这个类是对单个问题的抽象"""
	question = models.CharField(max_length=200,verbose_name="问题")
	required = models.BooleanField(default=True, help_text="这个问题是否必须回答",verbose_name="是否必填")

	questionnaire = models.ForeignKey(Questionnaire,verbose_name="问卷名称")
	order_in_list = models.IntegerField(default=1,verbose_name="选项顺序")
	created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="创建时间")

	def __str__(self):
		return self.question

	class Meta:
		abstract = True

#选择题的Model
class ChoiceQuestion(Question):
	"""选择题"""
	multi_choice = models.BooleanField(default=False, verbose_name="是否为多选")
	is_first_title = models.BooleanField(default=False, verbose_name="是否为一级标题")
	is_second_title = models.BooleanField(default=False, verbose_name="是否为二级标题")

	class Meta:
		ordering = ["order_in_list"]
		verbose_name = "问卷-选择题管理"
		verbose_name_plural = "问卷-选择题管理"

#常数定义--请勿修改
TEXT_QUESTION_TYPE = 0 #问答题
FILE_QUESTION_TYPE = 1 #文件题

#主观题的Model
class NonChoiceQuestion(Question):
	"""主观题"""
	type = models.SmallIntegerField(verbose_name="主观题类型",choices=((TEXT_QUESTION_TYPE,'问答题'),(FILE_QUESTION_TYPE,'文件题')),default=0)

	class Meta:
		verbose_name = "无选项题管理"
		verbose_name_plural = "无选项题管理"

#为问答题设计选项
class Choice(models.Model):
	question = models.ForeignKey(ChoiceQuestion, related_name="choices", verbose_name="问题题目")
	questionnaire = models.ForeignKey(Questionnaire, null=True, related_name="choices_que", verbose_name="问卷名称")
	descripiton = models.CharField(max_length=50, verbose_name="选项内容")
	multi_choice = models.BooleanField(default=False, verbose_name="是否为多选")
	order_in_list = models.IntegerField(default=1, verbose_name="第几个选项")

	def __str__(self):
		return self.descripiton
	class Meta:
		ordering = ["question","order_in_list"]
		verbose_name = "选择题-选项管理"
		verbose_name_plural = "选择题-选项管理"


#------答案部分---------------------------------------------------------------------------------------------------------------------------------
class AnswerSheet(models.Model):
	"""答卷的抽象"""
	user = models.ForeignKey(AnswerUser)                    #答题者
	questionnaire = models.ForeignKey(Questionnaire)  #对应的问卷

	created_at = models.DateTimeField(default=timezone.now, editable=False)
	modified_at = models.DateTimeField(default=timezone.now, editable=False)
	is_active = models.BooleanField(default=True)

#答案的抽象基类---基类是抽象类，不可以在后台管理添加，否则报错
class Answer(models.Model):
	"""答案的基类"""
	answer_sheet = models.ForeignKey(AnswerSheet)

	class Meta:
		abstract =True

class SingleChoiceAnswer(Answer):
	"""单选题的答案"""
	choice = models.ForeignKey(Choice, related_name="single_choice_answers") #单选题
	question = models.ForeignKey(ChoiceQuestion, related_name="single_choice_answer_set")

class MultiChoiceAnswer(Answer):
	"""多选题的答案"""
	choices = models.ManyToManyField(Choice, related_name="multi_choice_answers")
	question = models.ForeignKey(ChoiceQuestion, related_name="multi_choice_answer_set")

class TextAnswer(Answer):
	"""文字题答案"""
	text = models.TextField()
	question = models.ForeignKey(NonChoiceQuestion)

class FileAnswer(Answer):
	file = models.ImageField(upload_to='images/%Y/%m/%d')
	question = models.ForeignKey(NonChoiceQuestion)
	is_image = models.BooleanField(default=True)






