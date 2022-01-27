from django.db import models
from django.urls import reverse
from django.conf import settings
import misaka


class HrBot(models.Model):
	def ask(question, chat_log=None):
		doc_list=[]
		fields = ('message')
		print('passed', fields)

		openai.api_key ="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"
		start_sequence = "\nA:"
		restart_sequence = "\n\nQ: "
		response = openai.Answer.create(
		search_model="davinci",
		model="curie",
		question=fields,
		documents=doc_list,
		examples_context="Federal law states that if an employee travels overnight to a compensable training event, all travel time that cuts across normal business hours must be paid. This travel time can be paid at a differential rate as long as it does not fall below minimum wage and it is established in writing prior to the event. However, some states have additional rules that apply. For example, in California all business travel must be paid as well as mileage.",
		examples=[["How and when do I pay employees for mandatory business travel?"]],
		max_tokens=30,
		stop=["\n", "<|endoftext|>"],
		)
		story = response['choices'][0]['text']
		print(story)