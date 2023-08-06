from disneis import neis
import pytest


@pytest.fixture
def client():
    yield neis.sync()
