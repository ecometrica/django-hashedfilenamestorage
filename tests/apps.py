try:
    from django.apps import AppConfig
except ImportError:
    # Early Django versions import everything in test, avoid the failure due to
    # AppConfig only existing in 1.7+
    AppConfig = object


class TestConfig(AppConfig):
    name = 'tests'
    label = '_tests'
