from distutils.log import warn
from django.test import TestCase

from .models import Warning
from .models import WaringCategory

class TestDjangoSiteWarnings(TestCase):

    def test01(self):
        category = WaringCategory()
        category.code = "category"
        category.name = "category"
        category.save()
        warning = Warning.make(category=category, title="Account not exists...", data="Account: test01", save=True)
        assert len(Warning.objects.all()) == 1
        assert warning.category.pk == category.pk

