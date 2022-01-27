from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import SelectRelatedMixin
from django.http import HttpResponse, JsonResponse
import json
from . import forms
import os
import openai

def doclist():
	global doc_list
	doc_list=[]
	for doc in os.listdir('hrjson'):
		with open(os.path.abspath('hrjson/{doc}'.format(doc=doc))) as json_file:
			#print(json_file)
			data1 = json.loads(json_file.read()) # deserialises it
			data2 = json.dumps(data1) # json formatted string
			if len(doc_list)<199:
				doc_list.append(data2)
	print(len(doc_list))
	return doc_list

openai.api_key = "enterkeyhere"
completion = openai.Completion()

start_sequence = "\nA:"
restart_sequence = "\n\nQ: "
session_prompt = "I am an intelligent Human resources assistant bot. I will research company policies and labor policies applicable to your question then answer your question. I will also tell you where I found the answer. If I cannot answer the question or it confuses me I will respond with \"Unknown\".\n\nQ:How should I define my payroll workweek?\nA: The FLSA says a workweek is 7 consecutive 24-hour periods, but does not necessarily have to correspond to the calendar week. Here at CEDR, we recommend Sunday through Saturday in order to split the weekend down the middle and limit the chance of overtime caused by traveling or CEs.\n\nQ: How and when do I pay employees for mandatory business travel?\nA: Federal law states that if an employee travels overnight to a compensable training event, all travel time that cuts across normal business hours must be paid. This travel time can be paid at a differential rate as long as it does not fall below minimum wage and it is established in writing prior to the event. However, some states have additional rules that apply. For example, in California all business travel must be paid as well as mileage\n\nQ: When can I make deductions from an exempt employee’s paycheck?\nA: You can deduct for a full day’s absence, or replace a full day with vacation or sick leave, as long as you have a bona fide vacation or sick leave policy in your medical or dental office’s employee manual. But if the employee works for even a few minutes before going home, you are required to pay the full day’s wages.\n\nQ:"

def ask(question, chat_log=None):
    prompt_text = f'{chat_log}{restart_sequence}: {question}{start_sequence}:'
    response = openai.Completion.create(
      engine="davinci",
      prompt=prompt_text,
      temperature=0.1,
      max_tokens=150,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      stop=["\n"],
    )
    story = response['choices'][0]['text']
    print(story)
    return story

def adcopy(question, chat_log=None):
    prompt_text = question
    response = openai.Completion.create(
		engine="davinci-instruct-beta",
		prompt=prompt_text,
		temperature=0.5,
		max_tokens=60,
		top_p=1.0,
		frequency_penalty=0.0,
		presence_penalty=0.0,
		stop=["\"\"\"\"\"\""]
		)
    story = response['choices'][0]['text']
    print(story)
    return story

class HomePage(TemplateView):
	template_name='index.html'

class TestPage(TemplateView):
	template_name='test.html'

class ThanksPage(TemplateView):
	template_name='thanks.html'

class BotPage(TemplateView,LoginRequiredMixin,SelectRelatedMixin):
	doclist()
	template_name='bot.html'

def chats2(request):
	#print(doc_list)
	if request.method == 'POST':
		#def form_valid(self, form):
		form=request.POST['message']
		print('passed',form)
		openai.api_key ="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"
		start_sequence = "\nA:"
		restart_sequence = "\n\nQ: "
		response = openai.Answer.create(
		search_model="ada",
		model="curie",
		question=form,
		documents=doc_list,
		max_rerank=5,
		examples_context="Federal law states that if an employee travels overnight to a compensable training event, all travel time that cuts across normal business hours must be paid. This travel time can be paid at a differential rate as long as it does not fall below minimum wage and it is established in writing prior to the event. However, some states have additional rules that apply. For example, in California all business travel must be paid as well as mileage.",
		examples=[["How and when do I pay employees for mandatory business travel?","Federal law states that if an employee travels overnight to a compensable training event, all travel time that cuts across normal business hours must be paid. This travel time can be paid at a differential rate as long as it does not fall below minimum wage and it is established in writing prior to the event. However, some states have additional rules that apply. For example, in California all business travel must be paid as well as mileage."]],
		max_tokens=100,
		stop=["\n", "<|endoftext|>"],
		)
		story = response['choices'][0]['text']
		#print(story)
		#story='This is the answer object2'
		return JsonResponse({"answer": story})
	else:
		print('get method called')
		return JsonResponse({"answer": story})

def chats(request):
	#print(doc_list)
	if request.method == 'POST':
		#def form_valid(self, form):
		form=request.POST['message']
		print('passed',form)
		story=ask(question=form)
		return JsonResponse({"answer": story})
	else:
		print('get method called')
		return JsonResponse({"answer": story})

def getmessages(request):
	messages ='tester'
	return JsonResponse({"answer":messages})