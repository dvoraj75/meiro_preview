from django.db import models, transaction

from evidenta.common.services.base import BaseService

from .models import User


class UserService(BaseService):
    manager = User.objects

    def create(self, **user_data) -> User:
        with transaction.atomic():
            user = self.manager.create(**user_data)
            # todo: vytvorit penezenku, odeslat notifikace,...
        return user

    def get(self, user_id: int, as_user: User) -> User:
        return self.get_all(as_user=as_user).get(pk=user_id)

    def get_all(self, *args, **kwargs) -> models.QuerySet[User]:
        return self.manager.get_all_related_users(*args, **kwargs)

    def update(self, user_id: int, as_user: User, **user_data) -> None:
        with transaction.atomic():
            self.manager.update(user_id=user_id, as_user=as_user, **user_data)
            # todo: mozna nejake dalsi notifikace

    def delete(self, user_id: int, **kwargs) -> None:
        self.manager.delete(user_id=user_id, **kwargs)
