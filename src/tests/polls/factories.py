import factory
from django.utils.crypto import get_random_string
from django.utils.functional import classproperty

from db.polls.models import (
    CHOICE_TEXT_MAX_LEN,
    CHOICES_MAX_NUMBER,
    CHOICES_MIN_NUMBER,
    QUESTION_TEXT_MAX_LEN,
    QUESTION_TEXT_MIN_LEN,
    QUESTION_TITLE_MAX_LEN,
    QUESTION_TITLE_MIN_LEN,
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
    "WrongQuestion",
]


class QuestionDictFactory(factory.DictFactory):
    title = factory.Sequence(lambda n: f"Test question #{n} (dict) 6e59bdba4efb71")
    text = factory.Sequence(lambda n: f"Test question text #{n} (dict)")


class QuestionChoicesDictFactory(QuestionDictFactory):
    choices = factory.LazyAttribute(
        lambda _: [f"Choice #{i} (dict)" for i in range(CHOICES_MAX_NUMBER)],
    )


class WrongQuestion:
    @classproperty
    def title_too_long(cls):
        return get_random_string(QUESTION_TITLE_MAX_LEN + 1)

    @classproperty
    def title_too_short(cls):
        return get_random_string(QUESTION_TITLE_MIN_LEN - 1)

    @classproperty
    def text_too_long(cls):
        return get_random_string(QUESTION_TEXT_MAX_LEN + 1)

    @classproperty
    def text_too_short(cls):
        return get_random_string(QUESTION_TEXT_MIN_LEN - 1)


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

    @classproperty
    def too_long_text(cls):
        return get_random_string(CHOICE_TEXT_MAX_LEN + 1)

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
