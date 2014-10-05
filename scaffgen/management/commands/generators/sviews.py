import os


class View:



    def __init__(self, appname):
        self.appname = appname
        self.model = None

        # curr_dir =  os.path.dirname(os.path.realpath(__file__))
        parentdir = os.path.dirname(os.path.dirname(__file__))


        with open(os.path.join(parentdir, 'scaffold_templates/views/view_import_template.txt')) as ft:
            self.RENDER_VIEW_IMPORT_TEMPLATE = ft.read()
        with open(os.path.join(parentdir, 'scaffold_templates/views/view_list_template.txt')) as ft:
            self.RENDER_VIEW_LIST_TEMPLATE = ft.read()
        with open(os.path.join(parentdir, 'scaffold_templates/views/view_create_edit_template.txt')) as ft:
            self.RENDER_VIEW_CREATE_EDIT_TEMPLATE = ft.read()
        with open(os.path.join(parentdir, 'scaffold_templates/views/view_detail_template.txt')) as ft:
            self.RENDER_VIEW_DETAIL_TEMPLATE = ft.read()
        with open(os.path.join(parentdir, 'scaffold_templates/views/view_delete_template.txt')) as ft:
            self.RENDER_VIEW_DELETE_TEMPLATE = ft.read()


    def set_model(self, model):
        self.model = model


    def render_imports(self):
        rendered_imports = self.RENDER_VIEW_IMPORT_TEMPLATE.format(app_name=self.appname)
        return rendered_imports


    def render_view(self):

        rendered_view = self.RENDER_VIEW_LIST_TEMPLATE.format(model=self.model['model_name'].lower(), model_name=self.model['model_name'], app_name=self.appname)
        rendered_view +=  self.RENDER_VIEW_CREATE_EDIT_TEMPLATE.format(model=self.model['model_name'].lower(), model_name=self.model['model_name'], app_name=self.appname)
        rendered_view += self.RENDER_VIEW_DETAIL_TEMPLATE.format(model=self.model['model_name'].lower(), model_name=self.model['model_name'], app_name=self.appname)
        rendered_view += self.RENDER_VIEW_DELETE_TEMPLATE.format(model=self.model['model_name'].lower(), model_name=self.model['model_name'], app_name=self.appname)
        return rendered_view
