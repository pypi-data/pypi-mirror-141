==================
dj-rest-register
==================

Django rest framework custom user authentication package

Quick start
=============

1. Add "app" in your `INSTALLED_APPS` settings like this::

    INSTALLED_APPS = [
        ...
        'dj_swift_auth',
        'rest_framework',
        'rest_framework.authtoken',
    ]

2. Include the app URLconf in your project urls.py like this::
    path('user/', include('dj_swift_auth.urls')),

3. `settings.py` file add your use model::
    AUTH_USER_MODEL = 'dj_swift_auth.User'

4. Drop current database and delete all migrations file from your application then again run migration in the app::
    1) python manage.py makemigrations dj_swift_auth
    2) python manage.py migrate dj_swift_auth
    3) python manage.py migrate

API endpoint:
==============
1. Registration: ``user/api/register/``
2. Login: ``user/api/login/``
3. Profile: ``user/api/profile/``
4. Profile Update: ``user/api/profile/1/``
5. Change Password: ``user/api/change-password/1/`` # Pass the user ID
6. Logout: ``user/api/logout/``
