
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from .api.application_api import ApplicationApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from svix.openapi_client.api.application_api import ApplicationApi
from svix.openapi_client.api.authentication_api import AuthenticationApi
from svix.openapi_client.api.endpoint_api import EndpointApi
from svix.openapi_client.api.environment_api import EnvironmentApi
from svix.openapi_client.api.environment_settings_api import EnvironmentSettingsApi
from svix.openapi_client.api.event_type_api import EventTypeApi
from svix.openapi_client.api.health_api import HealthApi
from svix.openapi_client.api.integration_api import IntegrationApi
from svix.openapi_client.api.message_api import MessageApi
from svix.openapi_client.api.message_attempt_api import MessageAttemptApi
from svix.openapi_client.api.statistics_api import StatisticsApi
