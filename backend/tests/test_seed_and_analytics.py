import pytest
from django.core.management import call_command
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_seed_basics_and_summary_month():
	call_command('seed_basics')
	User = get_user_model()
	u = User.objects.create_user(username='t1', password='p')
	client = APIClient()
	assert client.login(username='t1', password='p')
	res = client.get('/api/analytics/summary/month/')
	assert res.status_code == 200
	assert isinstance(res.json(), list)