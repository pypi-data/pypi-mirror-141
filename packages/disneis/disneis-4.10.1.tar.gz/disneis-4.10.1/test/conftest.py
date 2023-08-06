from disneis import Neispt
import pytest


@pytest.fixture
def client():
    yield Neispt.sync()
