import pytest
from model_bakery import baker


@pytest.fixture
def user_factory():
    def factory(**kwargs):
        user = baker.make('shop.User', **kwargs)
        return user
    return factory


@pytest.fixture
def good_factory():
    def factory(**kwargs):
        good = baker.make('shop.Good', **kwargs)
        return good
    return factory


@pytest.fixture
def relationship_user_factory():
    def factory(**kwargs):
        relationship_user = baker.make('shop.RelationshipUser', **kwargs)
        return relationship_user
    return factory