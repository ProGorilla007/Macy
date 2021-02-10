from factory.django import DjangoModelFactory
from factory import Faker, SubFactory, fuzzy
from Macy.models import User, Links

"""
    factories.py:
    Provides dummy data through faker from factory_boy
"""

FAKER_LOCALE = 'ja_JP'
MEDIA_CHOICES = [x[0] for x in Links.MEDIA_CHOICES]


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    # 'user_name'というprovider
    username = Faker('user_name', locale=FAKER_LOCALE)
    first_name = Faker('first_name', locale=FAKER_LOCALE)
    last_name = Faker('last_name', locale=FAKER_LOCALE)
    email = Faker('email', locale=FAKER_LOCALE)
    intro = Faker('sentence', locale=FAKER_LOCALE)
    is_staff = False


class LinksFactory(DjangoModelFactory):
    class Meta:
        model = Links

    user_id = SubFactory(UserFactory)
    account_id = Faker('user_name', locale=FAKER_LOCALE)
    media_choice = fuzzy.FuzzyChoice(MEDIA_CHOICES)
    link = Faker('uri', locale=FAKER_LOCALE)


"""
    --available provider list-- 
            date   
            email
            http_method
            image_url
            uri
            user_name
            paragraphs
            sentence
            first_name
            last_name
    
    More available at
    https://faker.readthedocs.io/en/latest/locales/ja_JP.html#faker-providers-internet
"""