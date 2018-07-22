from .client import Client as DefaultClient
from django.contrib.auth import get_user_model
import logging as _logging
logger = _logging.getLogger(__name__)

User = get_user_model()


class Client(DefaultClient):
    def build_user(self, user_data):
        extra_data = {}
        if 'extra_data' in user_data:
            extra_data = user_data.pop('extra_data')
        try:
            user = User.objects.get(email=user_data['email'])
        except User.DoesNotExist:

            user = User(**user_data)
        user.set_unusable_password()
        self.set_user_extra_data(user, extra_data)
        user.save()
        return user

    def set_user_extra_data(self, user, extra_data):
        if not extra_data:
            return
        objects = []
        for k, v in extra_data.items():
            try:
                res = self.set_attr(user, k, v)
            except Exception as e:
                logger.error(str(e))
                continue
            if res:
                if res not in objects:
                    objects.append(res)
        for res in objects:
            if hasattr(res, 'save'):
                if callable(getattr(res, 'save')):
                    try:
                        getattr(res, 'save')()
                    except Exception as e:
                        logger.error(str(e))

    def set_attr(self, obj, name, value):
        names = name.split('.')
        attr_name = names.pop(0)
        if hasattr(obj, attr_name):
            if names:
                attr = getattr(obj, attr_name)
                return self.set_attr(attr, '.'.join(names), value)
            else:
                setattr(obj, attr_name, value)
                return obj
        else:
            return False
