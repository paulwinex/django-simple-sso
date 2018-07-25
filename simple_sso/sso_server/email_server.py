from simple_sso.sso_server.server import Server as DefauleServer


class Server(DefauleServer):
    def get_user_data(self, user, consumer, extra_data=None):
        user_data = getattr(self, 'user_data', None) or {
            'email': user.email,
            'is_staff': False,
            'is_superuser': False,
            'is_active': user.is_active,
        }
        if extra_data:
            user_data['extra_data'] = self.get_user_extra_data(
                user, consumer, extra_data)
        return user_data

    def get_user_extra_data(self, user, consumer, extra_data):
        data = {}
        for name in extra_data:
            try:
                data[name] = self.get_attr(user, name)
            except AttributeError:
                print('Error extra attribute not exists: {}'.format(name))
                continue
        return data

    def get_attr(self, obj, atr):
        names = atr.split('.')
        first = names.pop(0)
        if hasattr(obj, first):
            atr_obj = getattr(obj, first)
        else:
            raise AttributeError
        if names:
            return self.get_attr(atr_obj, '.'.join(names))
        else:
            return atr_obj