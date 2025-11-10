import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_health_check():
    """Test health check endpoint."""
    client = Client()
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'healthy'


@pytest.mark.django_db
def test_products_list():
    """Test products list endpoint."""
    client = Client()
    response = client.get('/api/products/')
    assert response.status_code == 200
    data = response.json()
    assert 'total' in data
    assert 'products' in data
