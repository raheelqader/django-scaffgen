Scaffgen
=============

Scaffgen is a simple scaffold generator for django projects that creates views, forms, and templates for a given app's one or more models. Please note that scaffgen DOES NOT create models for you, you should have already defined your models before running scaffgen.



Quick start
-----------
Here is a short video showing the installation and usage of Scaffgen:
	https://www.youtube.com/watch?v=Gu9biHc6-ls



Installation
-----------

	pip install git+https://github.com/raheelqader/django-scaffgen



Usage
------
1. Add "scaffgen" to INSTALLED_APPS:
	```
	INSTALLED_APPS = {
		...
		'scaffgen',
	}
	```


2. Run 'python manage.py scaffold [Options: --base(creates the base.html)] app model model ...' to create scaffolds from models.
	e.g:
	```
	python manage.py scaffgen --base myblog Post Comment
	```

3. Include the app's URLconf in urls.py:
	```
	urlpatterns += patterns ('',

	(r'^', include('yourapp.urls')),

	)
	```

4. Define the template directory in settings.py:
	```
	TEMPLATE_DIRS = (
    	os.path.join(BASE_DIR,  'templates'),
	)
	```


5. Run the development server and access http://127.0.0.1:8000/yourapp/yourmodel/list/ to see the newly created pages.