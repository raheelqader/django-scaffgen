import collections
import os

class Form:


	def __init__(self, appname):
		self.appname = appname
		self.model = None

		# curr_dir =  os.path.dirname(os.path.realpath(__file__))
		parentdir = os.path.dirname(os.path.dirname(__file__))

		with open(os.path.join(parentdir, 'scaffold_templates/forms/form_import_template.txt')) as ft:
			self.RENDER_FORM_IMPORT_TEMPLATE = ft.read()
		with open(os.path.join(parentdir, 'scaffold_templates/forms/simple_form_template.txt')) as ft:
			self.RENDER_SIMPLE_FORM_TEMPLATE = ft.read()
		with open(os.path.join(parentdir, 'scaffold_templates/forms/ext_form_template.txt')) as ft:
			self.RENDER_EXT_FORM_TEMPLATE = ft.read()
		with open(os.path.join(parentdir, 'scaffold_templates/forms/form_field_template.txt')) as ft:
			self.RENDER_FORM_FIELD_TEMPLATE = ft.read()

	
	def set_model(self, model):
		self.model = model


	def render_imports(self):
		rendered_imports = self.RENDER_FORM_IMPORT_TEMPLATE.format(app_name=self.appname)
		return rendered_imports


	def render_form_simple(self):
		rendered_form = self.RENDER_SIMPLE_FORM_TEMPLATE.format(model_name = self.model['model_name'])
		return rendered_form




	def render_form_extended(self):
		
		form = self.model

		fields = ''
		for field in form['fields']:
			rendered_field = self.RENDER_FORM_FIELD_TEMPLATE
			_field = self.__render_field(field, form['fields'][field])
			if _field:
				_rendered_field = self.__render_field(field, form['fields'][field])
				fields += ('\t' + rendered_field.format(field_name=_rendered_field[0], field_type=_rendered_field[1], field_attr=_rendered_field[2]))
		
		rendered_form = self.RENDER_EXT_FORM_TEMPLATE.format(model_name=form['model_name'], form_fields=fields)

		return rendered_form



	def render_form(self, form_type):
		
		if form_type == 'e':
			return self.render_form_extended()
		else:
			return self.render_form_simple()




	def __render_field(self, field_key, field_value):

		rendered_field = []

		rendered_field.append(field_key)

		if field_value['type'] == 'ForeignKey':
			rendered_field.append('ModelChoiceField')

			atributes = ''
			atributes += 'queryset=' + str(field_value['attributes']['related_key']) + '.objects.all()'

			if 'blank' in field_value['attributes']:
				if field_value['attributes']['blank'] == True:
					atributes += ', required=False'

			rendered_field.append(atributes)


		elif field_value['type'] in ['CharField', 'TextField']:

			rendered_field.append('CharField')

			atributes = ''
			atributes += 'max_length=' + str(field_value['attributes']['max_length'])

			if 'blank' in field_value['attributes']:
				if field_value['attributes']['blank'] == 'True':
					atributes += ', required=False'

			rendered_field.append(atributes)


		elif field_value['type'] in ['IntegerField', 'DateField', 'BooleanField', 'ImageField']:

			rendered_field.append(field_value['type'])

			atributes = ''
			if 'blank' in field_value['attributes']:
				if field_value['attributes']['blank'] == 'True':
					atributes += ', required=False'

			rendered_field.append(atributes)


		elif field_value['type'] in ['DecimalField']:

			rendered_field.append('DecimalField')

			atributes = ''
			if 'max_digits' in field_value['attributes']:
				atributes += 'max_digits=' + field_value['attributes']['max_digits']

			if 'decimal_places' in field_value['attributes']:
				atributes += ', decimal_places=' + field_value['attributes']['decimal_places']

			rendered_field.append(atributes)

		else:
			return None
			rendered_field.append(field_value['type'])
		
			atributes = ''
			if 'blank' in field_value['attributes']:
				if field_value['attributes']['blank'] == 'True':
					atributes += ', required=False'

			rendered_field.append(atributes)

		return rendered_field



	

