import factory
from django.utils.functional import classproperty

from db.polls.models import (
    CHOICES_MAX_NUMBER,
    CHOICES_MIN_NUMBER,
    Choice,
    Question,
    Vote,
)
from tests.users.factories import UserFactory

__all__ = [
    "QuestionFactory",
    "QuestionDictFactory",
    "QuestionChoicesDictFactory",
    "ChoiceFactory",
    "VoteFactory",
    "WrongChoice",
]


class QuestionDictFactory(factory.DictFactory):
    title = factory.Sequence(lambda n: f"Test question #{n} (dict) 6e59bdba4efb71")
    text = factory.Sequence(lambda n: f"Test question text #{n} (dict)")


class QuestionChoicesDictFactory(QuestionDictFactory):
    choices = factory.LazyAttribute(
        lambda _: [f"Choice #{i} (dict)" for i in range(CHOICES_MAX_NUMBER)],
    )


class WrongChoice:
    @classproperty
    def list_too_long(cls):
        return [f"Choice {i}" for i in range(CHOICES_MAX_NUMBER + 1)]

    @classproperty
    def list_too_short(cls):
        return [f"Choice {i}" for i in range(CHOICES_MIN_NUMBER - 1)]

    @classproperty
    def list_with_empty_choices(cls):
        return ["", "", ""]

    @classproperty
    def identical_choices(cls):
        return ["123", "123", "123"]

    empty_text = ""


class QuestionFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: f"Test question #{n}")
    text = factory.Sequence(lambda n: f"Test question text #{n}")
    owner = factory.SubFactory(UserFactory)

    class Meta:
        model = Question


class ChoiceFactory(factory.django.DjangoModelFactory):
    text = factory.Sequence(lambda n: f"Choice #{n}")
    question = factory.SubFactory(QuestionFactory)

    class Meta:
        model = Choice


class VoteFactory(factory.django.DjangoModelFactory):
    question = factory.SubFactory(QuestionFactory)
    choice = factory.SubFactory(ChoiceFactory)
    owner = factory.SubFactory(UserFactory)

    class Meta:
        model = Vote
