import os
from unittest import mock

os.environ["MODE"] = "TEST"

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda x: x).start()
