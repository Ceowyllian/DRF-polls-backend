LOCAL_APPS = [
    "apps.users.apps.UsersConfig",
    "apps.polls.apps.PollsConfig",
]

THIRD_PARTY_APPS = [
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "djoser",
    "django_filters",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    *THIRD_PARTY_APPS,
    *LOCAL_APPS,
]
