from django.core.exceptions import FieldDoesNotExist, ValidationError
from django.db import models

from evidenta.common.validators import BaseDataValidator


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    def update(self, **data: dict[str, any]) -> None:
        for field_name, value in data.items():
            try:
                if (field := self._meta.get_field(field_name)).is_relation and not isinstance(field, models.ForeignKey):
                    getattr(self, field_name).set(value)
                else:
                    setattr(self, field_name, value)
            except FieldDoesNotExist as e:
                raise ValidationError(f"Field {field_name} does not exist") from e


class BaseModelManagerMixin:
    data_validator = BaseDataValidator

    def clean_and_validate_data(cls, user_data: dict[str, any]) -> None:
        cls.clean_data(user_data)
        cls.data_validator.validate_data(user_data)

    @staticmethod
    def clean_data(user_data: dict[str, any]) -> None:
        pass
