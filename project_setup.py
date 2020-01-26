import os
import re
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# Create Apps Directory
try:
    os.mkdir(os.path.join(BASE_DIR, 'apps'))
except:
    pass
print('Created apps/')

# Create Static Directory
try:
    os.mkdir(os.path.join(BASE_DIR, 'static'))
except:
    pass
print('Created static/')

# Get Project Name (ie: Base Folder Name)
PROJECT_NAME = os.path.split(BASE_DIR)[1]
print('Project Name set to {}'.format(PROJECT_NAME))

print('Loading Settings')
settings = open(os.path.join(BASE_DIR, PROJECT_NAME, 'settings.py'), "r").read()

matches = re.finditer(
    r"^(?P<key>[A-Za-z_\d]*)\s*=\s*(?P<value>.*[\'\s\[.,\]{}_:\(\)\-\/\w]*)(?=(^[A-Za-z_\d]*\s*=|$|#))", settings,
    re.MULTILINE)

COMMON = [
    'BASE_DIR',
    'INSTALLED_APPS',
    'MIDDLEWARE',
    'ROOT_URLCONF',
    'TEMPLATES',
    'WSGI_APPLICATION',
    'AUTH_PASSWORD_VALIDATORS',
    'LANGUAGE_CODE',
    'TIME_ZONE',
    'USE_I18N',
    'USE_L10N',
    'USE_TZ',
    'STATIC_URL'
]

SPECIAL = [
    'SECRET_KEY',
    'DEBUG',
    'ALLOWED_HOSTS',
    'DATABASES'
]

f = open(os.path.join(BASE_DIR, PROJECT_NAME, 'common.py'), 'a+')
f.write("import os\n\nimport sys\n")
f.close()
print('Created common.py')
f = open(os.path.join(BASE_DIR, PROJECT_NAME, 'production.py'), 'a+')
f.write('import os\nfrom .common import *\n')
f.close()
print('Created production.py')
f = open(os.path.join(BASE_DIR, PROJECT_NAME, 'development.py'), 'a+')
f.write('import os\nfrom .common import *\n')
f.close()
print('Created development.py')

for matchNum, match in enumerate(matches, start=1):
    if match.group('key') in COMMON:
        f = open(os.path.join(BASE_DIR, PROJECT_NAME, 'common.py'), 'a+')
        f.write('\n\n{} = {}'.format(match.group('key'), match.group('value').rstrip()))
        if match.group('key') == 'BASE_DIR':
            f.write("\nsys.path.append(os.path.normpath(os.path.join(BASE_DIR, 'apps')))")
        f.close()

    if match.group('key') in SPECIAL:
        f = open(os.path.join(BASE_DIR, PROJECT_NAME, 'production.py'), 'a+')
        if match.group('key') == 'DEBUG':
            f.write('\n\n{} = {}'.format(match.group('key'), 'False'))
        else:
            f.write('\n\n{} = {}'.format(match.group('key'), match.group('value').rstrip()))
        f.close()
        f = open(os.path.join(BASE_DIR, PROJECT_NAME, 'development.py'), 'a+')
        f.write('\n\n{} = {}'.format(match.group('key'), match.group('value').rstrip()))
        f.close()

f = open(os.path.join(BASE_DIR, PROJECT_NAME, 'common.py'), 'a+')
static_files = (
    "\n\nSTATICFILES_DIRS = [\n"
    "    os.path.join(BASE_DIR, 'static'),\n"
    "    os.path.join(BASE_DIR, 'node_modules'),\n"
    "]\n"
)
f.write(static_files)
f.write('\n')
f.close()
f = open(os.path.join(BASE_DIR, PROJECT_NAME, 'production.py'), 'a+')
f.write('\n')
f.close()
f = open(os.path.join(BASE_DIR, PROJECT_NAME, 'development.py'), 'a+')
f.write('\n')
f.close()

print('Created new Settings Structure')

NGINX_CONFIG = (
    "# {PROJECT_NAME}_nginx.conf\n"
    "# the upstream component nginx needs to connect to\n"
    "upstream django {\n"
    "    server unix:///var/www/projects/{PROJECT_NAME}/{PROJECT_NAME}.sock; # for a file socket\n"
    "}\n"
    "# configuration of the server\n"
    "server {\n"
    "    # the port your site will be served on\n"
    "    listen      80;\n"
    "    # the domain name it will serve for\n"
    "    server_name DOMAIN_NAME; # substitute your machine's IP address or FQDN\n"
    "    charset     utf-8;\n"
    "# max upload size\n"
    "    client_max_body_size 75M;   # adjust to taste\n"
    "\n"
    "    location /static {\n"
    "        alias /var/www/html/{PROJECT_NAME}/static; # your Django project's static files - amend as required\n"
    "    }\n"
    "# Finally, send all non-media requests to the Django server.\n"
    "    location / {\n"
    "        uwsgi_pass  django;\n"
    "        include     /var/www/projects/{PROJECT_NAME}/uwsgi_params; # the uwsgi_params file you installed\n"
    "    }\n"
    "\n"
    "    location ^~ /admin/ {\n"
    "        allow 127.0.0.1/32;\n"
    "        deny all;\n"
    "        uwsgi_pass django;\n"
    "        include /var/www/projects/{PROJECT_NAME}/uwsgi_params;\n"
    "    }\n"
    "}\n"
    "\n"
)

UWSGI_INI = (
    "# project_uwsgi.ini file\n"
    "[uwsgi]\n"
    "# Django-related settings\n"
    "# the base directory (full path)\n"
    "chdir           = /var/www/projects/{PROJECT_NAME}\n"
    "# Django's wsgi file\n"
    "module          = {PROJECT_NAME}.wsgi\n"
    "# the virtualenv (full path)\n"
    "home            = /var/www/projects/{PROJECT_NAME}/venv\n"
    "# process-related settings\n"
    "# master\n"
    "master          = true\n"
    "# maximum number of worker processes\n"
    "processes       = 10\n"
    "# the socket (use the full path to be safe\n"
    "socket          = /var/www/projects/{PROJECT_NAME}/{PROJECT_NAME}.sock\n"
    "# ... with appropriate permissions - may be needed\n"
    "# chmod-socket    = 664\n"
    "# clear environment on exit\n"
    "vacuum          = true\n"
    "\n"
)

UWSGI_PARAMS = (
    "uwsgi_param  QUERY_STRING       $query_string;\n"
    "uwsgi_param  REQUEST_METHOD     $request_method;\n"
    "uwsgi_param  CONTENT_TYPE       $content_type;\n"
    "uwsgi_param  CONTENT_LENGTH     $content_length;\n"
    "\n"
    "uwsgi_param  REQUEST_URI        $request_uri;\n"
    "uwsgi_param  PATH_INFO          $document_uri;\n"
    "uwsgi_param  DOCUMENT_ROOT      $document_root;\n"
    "uwsgi_param  SERVER_PROTOCOL    $server_protocol;\n"
    "uwsgi_param  REQUEST_SCHEME     $scheme;\n"
    "uwsgi_param  HTTPS              $https if_not_empty;\n"
    "\n"
    "uwsgi_param  REMOTE_ADDR        $remote_addr;\n"
    "uwsgi_param  REMOTE_PORT        $remote_port;\n"
    "uwsgi_param  SERVER_PORT        $server_port;\n"
    "uwsgi_param  SERVER_NAME        $server_name;\n"
)

f = open(os.path.join(BASE_DIR, '{}_nginx.conf'.format(PROJECT_NAME)), 'a+')
f.write(NGINX_CONFIG.replace('{PROJECT_NAME}', PROJECT_NAME))
f.close()
f = open(os.path.join(BASE_DIR, '{}_uwsgi.ini'.format(PROJECT_NAME)), 'a+')
f.write(UWSGI_INI.replace('{PROJECT_NAME}', PROJECT_NAME))
f.close()
f = open(os.path.join(BASE_DIR, 'uwsgi_params'), 'a+')
f.write(UWSGI_PARAMS)
f.close()
print('Created new Deployment Configs')
print('')
print('Verify new project structure and settings are correct:')
print('  1. Delete settings.py')
print('  2. Create symlink to either development.py or production.py depending on environment.')