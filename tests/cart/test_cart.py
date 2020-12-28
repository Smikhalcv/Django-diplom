import pytest
from django.contrib.auth import authenticate
from django.urls import reverse
from django.test import Client

from cart.views import add_to_cart
from shop.models import RelationshipUser


@pytest.mark.django_db
def test_add_cart(client, user_factory, good_factory):
    username = 'example'
    email = 'example@example.com'
    password = 'example'
    user = user_factory(username=username, email=email, password=password)
    good = good_factory()

    # Check authenticated
    response = client.post(reverse('add_to_cart', args=[good.slug]))
    assert response.url == '/login/'

    # Check create item in cart
    client.force_login(user)
    client.post(reverse('add_to_cart', args=[good.slug]))
    username_test_user = good.relationshipuser_set.filter(user=user).all()[0].user.username
    assert username_test_user == username

    # Check growth quantity
    quantity_before = user.relationshipuser_set.filter(good=good)[0].quantity
    client.post(reverse('add_to_cart', args=[good.slug]))
    quantity_after = user.relationshipuser_set.filter(good=good)[0].quantity
    assert quantity_after > quantity_before


@pytest.mark.django_db
def test_cart(client, user_factory, good_factory, relationship_user_factory):
    username = 'example'
    email = 'example@example.com'
    password = 'example'
    user = user_factory(username=username, email=email, password=password)
    good = good_factory()

    # Check authenticated
    response = client.get(reverse('cart'))
    assert response.url == '/login/'

    client.force_login(user)

    # Check empty cart
    assert not user.cart.all()

    order = relationship_user_factory(user=user, good=good, quantity=2)

    # Check minus
    quantity_before = user.relationshipuser_set.filter(id=good.id)[0].quantity
    client.get(reverse('cart') + f'?parametr=minus&item={good.slug}')
    quantity_after = user.relationshipuser_set.filter(id=good.id)[0].quantity
    assert quantity_after < quantity_before

    # Check plus
    quantity_before = user.relationshipuser_set.filter(id=good.id)[0].quantity
    client.get(reverse('cart') + f'?parametr=plus&item={good.slug}')
    quantity_after = user.relationshipuser_set.filter(id=good.id)[0].quantity
    assert quantity_after > quantity_before

    #Check delete
    client.get(reverse('cart') + f'?parametr=delete&item={good.slug}')
    assert not user.cart.all()