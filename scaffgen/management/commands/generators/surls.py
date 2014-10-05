import os


class Url:


	def __init__(self, appname):
		self.appname = appname
		self.model = None

		
		# curr_dir =  os.path.dirname(os.path.realpath(__file__))
		parentdir = os.path.dirname(os.path.dirname(__file__))

		with open(os.path.join(parentdir, 'scaffold_templates/urls/url_import_template.txt')) as ft:
			self.RENDER_URL_IMPORT_TEMPLATE = ft.read()
		with open(os.path.join(parentdir, 'scaffold_templates/urls/url_template.txt')) as ft:
			self.RENDER_URL_TEMPLATE = ft.read()
		with open(os.path.join(parentdir, 'scaffold_templates/urls/url_main_template.txt')) as ft:
			self.RENDER_URL_MAIN_TEMPLATE = ft.read()
		with open(os.path.join(parentdir, 'scaffold_templates/urls/url_concat_template.txt')) as ft:
			self.RENDER_URL_CONCAT_TEMPLATE = ft.read()
	

	def set_model(self, model):
		self.model = model


	def render_imports(self):
		rendered_imports = self.RENDER_URL_IMPORT_TEMPLATE.format(app_name=self.appname)
		return rendered_imports


	def render_url(self):
		render_url = self.RENDER_URL_TEMPLATE.format(app_name=self.appname, model=self.model['model_name'].lower())
		return render_url


	def render_main_url(self, urls):
		render_main_url = self.RENDER_URL_MAIN_TEMPLATE.format(urls=urls)
		return render_main_url


	def render_url_contact(self):
		return self.RENDER_URL_CONCAT_TEMPLATE.format(app_name=self.appname)