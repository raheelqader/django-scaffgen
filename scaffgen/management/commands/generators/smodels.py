import re
import collections
from django.db import models


class Model:

	def __init__(self, model_name, appname):
		self.appname = appname
		self.model_name = model_name


	#access raw model data
	def __create_model(self):

		model_pattern = re.compile('(class.+:\n)(\t(.+))', re.DOTALL)
		model_class_pattern = '(class) (.+)\(.+\):'
		model_field_pattern =  '((.+)( )+?=( )+?models\.(.+)\((.+)?\)\n?)'

		# model_pattern = re.compile('((class) (.+)\(.+\):\n((.+)( )+?=( )+?models\.(.+)\((.+)?\)\n?)+)', re.DOTALL)


		model_pattern_matches = re.search(model_pattern, self.model_instance)
		if model_pattern_matches:
			class_line = model_pattern_matches.group(1)
			field_line = model_pattern_matches.group(2)

			model_class_pattern_matches = re.search(model_class_pattern, class_line)
			model_name = model_class_pattern_matches.group(2)

			model_field_pattern_matches = re.findall(model_field_pattern, field_line)
			fields = model_field_pattern_matches


			_fields = collections.OrderedDict()
			for field in fields[:]:
				field_name = field[1].strip()
				_fields[field_name] = {}
				_fields[field_name]['type'] = field[4].strip()

				_attributes = collections.OrderedDict()
				attributes = field[5].split(',')

				if len(attributes) > 1:
					for attribute in attributes:

						key, value = attribute.split('=') if len( attribute.split('=')) > 1 else ('_',attribute)
						_attributes[key.strip()] = value.strip()

				_fields[field_name]['attributes'] = _attributes

				
			

			_model = {'model_name':model_name, 'fields':_fields}

			return _model


	#access mode via meta class
	def create_model(self):

		self.model_instance = models.get_model(self.appname, self.model_name)

		model_name = self.model_instance.__name__
		fields = self.model_instance._meta.fields

		_fields = collections.OrderedDict()

		for field in fields:

			field_name = field.name
			_fields[field_name] = {}
			_fields[field_name]['type'] = field.get_internal_type()

			_attributes = collections.OrderedDict()

			if field.get_internal_type() == 'ForeignKey':
				_attributes['blank'] = field.blank
				_attributes['related_key'] = field.rel.to.__name__
				#add other field related attributes here

			elif field.get_internal_type() in ['CharField', 'TextField']:
				_attributes['blank'] = field.blank
				_attributes['max_length'] = field.max_length
				#add other field related attributes here

			elif field.get_internal_type() in ['IntegerField', 'DateField', 'BooleanField', 'ImageField']:
				_attributes['blank'] = field.blank
				#add other field related attributes here

			elif field.get_internal_type()  in ['DecimalField']:
				_attributes['blank'] = field.blank
				_attributes['max_digits'] = field.max_digits
				_attributes['decimal_places'] = field.decimal_places
				#add other field related attributes here
	

			_fields[field_name]['attributes'] = _attributes



			
		

		_model = {'model_name':model_name, 'fields':_fields}


		return _model
