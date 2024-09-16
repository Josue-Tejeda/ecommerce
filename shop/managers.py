from django.db import models

class ProductQuerySet(models.query.QuerySet):
    def get_all_available(self):
        return self.filter(is_available=True)