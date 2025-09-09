import pytest
from django.contrib.auth import get_user_model
from backend.importers.models import ImportDedup
from django.db import IntegrityError

@pytest.mark.django_db
def test_import_dedup_unique():
	User = get_user_model()
	u = User.objects.create_user(username='t2', password='p')
	h = 'a'*64
	ImportDedup.objects.create(user=u, row_hash=h)
	with pytest.raises(IntegrityError):
		ImportDedup.objects.create(user=u, row_hash=h)