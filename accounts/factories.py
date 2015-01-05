# -*- coding: utf-8 -*-
import factory


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'auth.User'

    username = factory.Sequence(lambda n: 'User %d' % n)
