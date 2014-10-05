from django.core.management.base import BaseCommand, CommandError
from django.db import models

import re, os, sys
from optparse import make_option


curr_dir = os.path.dirname(__file__)
sys.path.insert(0, curr_dir+'/generators') 

import sforms, sviews, surls, stemplates, smodels


class Command(BaseCommand):

    args = '<app model model ...>'
    # help = 'Generates scaffold for specified models of inside an app. Usage : manage.py scaffold [Options: -temp (s, e) -form (1, 2, 3)] <app> <model> <model> ...'
    help = 'Generates scaffold for specified models of inside an app. Usage : manage.py scaffold [Options: --base(creates the base.html)] <app> <model> <model> ...'

    option_list = BaseCommand.option_list + (
        # make_option('--temp',
        #     default=1,
        #     dest='temp',
        #     help='Specifies template type. Default is 1. Options are: 1, 2, 3'),
        # make_option('--form',
        #     default='s',
        #     dest='form',
        #     help='Specifies form type. Default is s(simple). Options are s(simple), e(extended).'),
        make_option('--base',
            action='store_true',
            dest='base',
            default=False,
            help='Creates the base.html template'),
        )
    def handle(self, *args, **options):
        ""

        PROJECT_ROOT = os.getcwd() 
        TEMPLATE_DIR = os.path.join ( PROJECT_ROOT , 'templates')


        try:
            appname = args[0] # App name is the first parameter
            model_names = args[1:] # Models which need to be scaffolded will follow

            # create_edit_temp_type = int(options['temp'])
            # form_type = options['form']
            create_edit_temp_type = 1
            form_type = 's'

            #class initializations
            f = sforms.Form(appname)
            v = sviews.View(appname)
            t = stemplates.Template(appname)
            u = surls.Url(appname)


            #call import functions
            fi = f.render_imports()
            self.write_file(PROJECT_ROOT + '/' + appname, 'forms.py', fi, 'a')

            vi = v.render_imports()
            self.write_file(PROJECT_ROOT + '/' + appname, 'views.py', vi, 'a')

            ui = u.render_imports()
            self.write_file(PROJECT_ROOT + '/' + appname, 'urls.py', ui, 'a')


            urls = ''
            navs = ''
            for model_name in model_names:

                #models
                m = smodels.Model(model_name, appname)
                model = m.create_model()
                # write_file('scaffold/' + appname, 'models.py', content)


                #forms
                f.set_model(model)
                form = f.render_form(form_type)
                self.write_file(PROJECT_ROOT + '/' + appname, 'forms.py', form, 'a')


                #views
                v.set_model(model)
                view = v.render_view()
                self.write_file(PROJECT_ROOT + '/' + appname, 'views.py', view, 'a')


                #templates
                t.set_model(model)
                template, file_name = t.render_list_template()
                self.write_file(PROJECT_ROOT + '/templates/' + appname, file_name, template, 'w')

                template, file_name = t.render_create_edit_template(create_edit_temp_type)
                self.write_file(PROJECT_ROOT + '/templates/' + appname, file_name, template, 'w')

                template, file_name = t.render_detail_template()
                self.write_file(PROJECT_ROOT + '/templates/' + appname, file_name, template, 'w')

                navs+= '<a href="/{app_name}/{model}/list/">{model_name}</a><br>'.format(app_name=appname, model_name=model_name, model=model_name.lower())


                #urls
                u.set_model(model)
                url = u.render_url()
                urls += url


            if options['base']:
                template, file_name = t.render_base_template(navs)
                self.write_file(PROJECT_ROOT + '/templates/', file_name, template, 'w') #move this part out of the for-loop

            main_url_template = u.render_main_url(urls)
            self.write_file(PROJECT_ROOT + '/' + appname, 'urls.py', main_url_template, 'a')

            url = u.render_url_contact()
            self.write_file(PROJECT_ROOT, 'urls.py', url, 'a')

            print('Done...')


        except:
            print "Usage : manage.py scaffold [Options: --base(creates the base.html)] <app model model ...>"



    def write_file(self, appname, filename, content, access):

        if not os.path.exists(appname):
                os.makedirs(appname)

        file_path = os.path.join (appname, filename)
        f = open(file_path , access)
        f.write(content)
        f.close() 
