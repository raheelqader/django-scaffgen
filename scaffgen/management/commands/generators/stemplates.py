import os 
from django import forms
from django.db import models

class Template:



	def __init__(self, appname):
		self.appname = appname
		self.model = None

		# curr_dir =  os.path.dirname(os.path.realpath(__file__))
		parentdir = os.path.dirname(os.path.dirname(__file__))


		with open(os.path.join(parentdir, 'scaffold_templates/templates/template_base_template.txt')) as ft:
			self.RENDER_TEMPLATES_BASE_TEMPLATE = ft.read()
		with open(os.path.join(parentdir, 'scaffold_templates/templates/template_list_template.txt')) as ft:
			self.RENDER_TEMPLATES_LIST_TEMPLATE = ft.read()
		with open(os.path.join(parentdir, 'scaffold_templates/templates/template_create_edit_template_1.txt')) as ft:
			self.RENDER_TEMPLATES_CREATE_EDIT_TEMPLATE_1 = ft.read()
		with open(os.path.join(parentdir, 'scaffold_templates/templates/template_create_edit_template_2.txt')) as ft:
			self.RENDER_TEMPLATES_CREATE_EDIT_TEMPLATE_2 = ft.read()
		with open(os.path.join(parentdir, 'scaffold_templates/templates/template_create_edit_template_3.txt')) as ft:
			self.RENDER_TEMPLATES_CREATE_EDIT_TEMPLATE_3 = ft.read()
		with open(os.path.join(parentdir, 'scaffold_templates/templates/template_detail_template.txt')) as ft:
			self.RENDER_TEMPLATES_DETAIL_TEMPLATE = ft.read()


	def set_model(self, model):
		self.model = model


	def render_base_template(self, navs):
		rendered_template_base = self.RENDER_TEMPLATES_BASE_TEMPLATE.format(navs=navs)
		return rendered_template_base, 'base.html'


	def render_list_template(self):
		rendered_template_list = self.RENDER_TEMPLATES_LIST_TEMPLATE.format(model_name= self.model['model_name'], model=self.model['model_name'].lower(), app_name=self.appname)
		return rendered_template_list, 'list_{0}.html'.format(self.model['model_name'].lower())


	def render_create_edit_template(self, temp_type):

		
		if temp_type ==	1:
			rendered_template_edit_create = self.RENDER_TEMPLATES_CREATE_EDIT_TEMPLATE_1.format(model_name=self.model['model_name'])
			return rendered_template_edit_create, 'create_edit_{0}.html'.format(self.model['model_name'].lower())
		
		if temp_type ==	2:
			rendered_template_edit_create = self.RENDER_TEMPLATES_CREATE_EDIT_TEMPLATE_2.format(model_name=self.model['model_name'])
			return rendered_template_edit_create, 'create_edit_{0}.html'.format(self.model['model_name'].lower())

		if temp_type ==	3:

			model_instance = models.get_model(self.appname ,self.model['model_name'])

			meta = type('Meta', (), { "model":model_instance, 'fields':'__all__'})
			form = type(self.model['model_name']+ 'Form', (forms.ModelForm,), {"Meta": meta})

			form_fields = ''

			for field in form():
				form_fields += field.name + ': ' + str(field)  + '\n'


			rendered_template_edit_create = self.RENDER_TEMPLATES_CREATE_EDIT_TEMPLATE_3.format(model_name=self.model['model_name'], form_fields=form_fields)
			return rendered_template_edit_create, 'create_edit_{0}.html'.format(self.model['model_name'].lower())


	def render_detail_template(self):
		rendered_template_detail = self.RENDER_TEMPLATES_DETAIL_TEMPLATE.format(model_name=self.model['model_name'])
		return rendered_template_detail, 'view_{0}.html'.format(self.model['model_name'].lower())