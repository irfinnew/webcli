![webcli cover image](https://moreaux.nl/projects/webcli/github.png)

# About

_webcli_ is a web service that takes a command with optional arguments, and then redirects the request to a corresponding web page.
Set it as the default search engine in your browser, and you can do things like `gim peacock` to search Google Images for peacocks, `wp Lady Gaga` to take you to the Wikipedia page for Lady Gaga, and `tiny http://example.com/` to create a tinyurl link.
You can define custom commands, tailored to what you want to do.

_webcli_ uses an [OpenSearch](https://en.wikipedia.org/wiki/OpenSearch) description to easily register with browsers.  
It was inspired by [YubNub](http://yubnub.org).


# Using webcli

To start using _webcli_, visit its home page with your browser.  

With Chrome, just visit the _webcli_ home page, and Chrome should register it as a search engine.
Then, go to `Settings` » `Search Engine` » `Manage search engines and site search`.
At the bottom of the page, find the _webcli_ entry, click the three dots on the right side, and choose `Make default`.

With Firefox, visit the _webcli_ home page, click the URL bar or search bar, find the _webcli_ icon with a little ⊕ on it, and click it.
This will register it as a search engine.
Next, go to `Settings` » `Search` » `Default Search Engine`, and choose _webcli_.



# Installation

_webcli_ is a simple [Django](https://www.djangoproject.com/) project.
For various ways how to host Django projects, see [their official documentation](https://docs.djangoproject.com/en/4.1/topics/install/).
_webcli's_ configuration uses a bunch of environment variables starting with `WEB_`, so modifying `settings.py` shouldn't be necessary in many cases.
It can either read these variables from the environment, or from a `.env` file somewhere up its path.
See `env.example` for the possible variables.

To quickly get _webcli_ up and running in a development environment, create a folder somewhere appropriate, and in that folder, execute the following commands and visit [localhost:8000](http://localhost:8000/):

```
git clone https://github.com/mmoreaux/webcli app/
virtualenv venv/
source venv/bin/activate
pip install -r app/requirements.txt
cp app/env.example app/.env
sed -i 's/WEB_DEBUG=False/WEB_DEBUG=True/' app/.env
./app/webcli/manage.py migrate
./app/webcli/manage.py createsuperuser
./app/webcli/manage.py runserver
```

For running _webcli_ in a production environment, I recommend running the application under an application server such as _gunicorn_ that is proxied from a real web server.
_webcli_ comes with a script to start gunicorn in `bin/appserver`, an example systemd service file in `system/webcli.service` and an example nginx virtualhost file in `system/webcli.nginx`.
If you use simple logging to a file, you may also want to add a cron job for `bin/logrotate`.

When running _webcli_ in a production setting, you want to change the following variables in `.env`:

 - `WEB_DEBUG` must be `False`. Using `True` is a [security risk](https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-DEBUG).
 - `WEB_SECRET_KEY` must be set to a strongly random generated password, unique to this deployment.
 - You may want to modify `WEB_LOGFILE_PATH` and `WEB_DB_NAME` to point to a more appropriate location. Or change the various `DB_*` variables to use a real database.
 - If your server can send emails, set `WEB_ERROR_EMAIL_*` to enable Django to send emails with detailed error reports.



# Managing commands

Visit [/admin/](https://cli.example.com/admin/) (default path, can be changed with `WEB_ADMIN_PATH`) on a _webcli_ installation and log in with an admin account to get access to the admin interface.
Click on `Commands` to see an overview of the defined commands.
Here you can edit existing commands, delete them, and add new ones.
