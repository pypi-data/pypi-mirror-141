from .duplicates import Duplicate
from .utils import duplicate


class DuplicateMixin:

    duplicate_class = Duplicate

    def duplicate(self, override_fields=None, paths=None):
        copied_obj = self.__class__.objects.get(pk=self.pk)
        return duplicate(
            copied_obj,
            override_fields=override_fields,
            paths=paths,
        )
