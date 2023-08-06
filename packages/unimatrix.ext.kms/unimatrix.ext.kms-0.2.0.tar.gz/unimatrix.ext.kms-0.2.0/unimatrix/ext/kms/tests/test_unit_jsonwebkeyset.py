# pylint: skip-file
import pytest

from ..loaders import JWKSLoader
from ..jsonwebkeyset import JSONWebKeySet


class TestJSONWebKeySet:

    def test_add(self):
        x = JSONWebKeySet()
        y = JSONWebKeySet()
        assert len(x + y) == (len(x) + len(y))

    #@pytest.mark.asyncio
    #async def test_loader_discover(self):
    #    loader = JWKSLoader()
    #    jwks = await loader.discover("https://accounts.google.com")
