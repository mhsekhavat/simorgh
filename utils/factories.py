import factory
import random


def random_subset(field):
    @factory.post_generation
    def inner(self, create, extracted):
        if not create:
            return

        print dir(self)
        for x in random.sample(extracted, random.randrange(len(extracted))):
            getattr(self, field).add(x)

    return inner

