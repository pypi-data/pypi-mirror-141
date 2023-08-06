from disneis import disneis
import pytest


@pytest.fixture
def client():
    yield disneis.sync()
