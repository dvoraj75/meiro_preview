from .settings import *


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "evidenta_testing_db",
        "USER": "evidenta",
        "PASSWORD": "evidenta",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}

# TEST_FIXTURES_FILES = [os.path.join(BASE_DIR, "evidenta/fixtures/test_data.json")]
TEST_FIXTURES_FILES = []
