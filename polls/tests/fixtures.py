__all__ = (
    "Q",
    "C",
    "choice_list",
    "question",
    "question_with_choices",
)

from django.utils.crypto import get_random_string

from ..models import (
    QuestionConfig,
    ChoiceConfig,
)


class Q:
    class title:
        @staticmethod
        def valid():
            return get_random_string(QuestionConfig.TITLE_MAX_LEN)

        @staticmethod
        def too_long():
            return get_random_string(QuestionConfig.TITLE_MAX_LEN + 1)

        @staticmethod
        def too_short():
            return get_random_string(QuestionConfig.TITLE_MIN_LEN - 1)

    class text:
        @staticmethod
        def valid():
            return get_random_string(QuestionConfig.TEXT_MAX_LEN)

        @staticmethod
        def too_long():
            return get_random_string(QuestionConfig.TEXT_MAX_LEN + 1)

        @staticmethod
        def too_short():
            return get_random_string(QuestionConfig.TEXT_MIN_LEN - 1)


class C:
    class number:
        @staticmethod
        def valid():
            return ChoiceConfig.CHOICES_MAX_NUMBER

        @staticmethod
        def too_many():
            return ChoiceConfig.CHOICES_MAX_NUMBER + 1

        @staticmethod
        def too_few():
            return ChoiceConfig.CHOICES_MIN_NUMBER - 1

    class text:
        @staticmethod
        def valid():
            i = 0
            while True:
                i += 1
                yield get_random_string(ChoiceConfig.TEXT_MAX_LEN - len(str(i))) + str(
                    i
                )

        @staticmethod
        def empty():
            while True:
                yield ""

        @staticmethod
        def too_long():
            i = 0
            while True:
                i += 1
                yield get_random_string(ChoiceConfig.TEXT_MAX_LEN) + str(i)

        @staticmethod
        def identical():
            text = get_random_string(ChoiceConfig.TEXT_MAX_LEN)
            while True:
                yield text


def get_default(value, default):
    return default if value is None else value


def choice_list(number=None, text=None):
    number = get_default(number, C.number.valid())
    text = get_default(text, C.text.valid())
    return [next(text) for _ in range(number)]


def question(title=None, text=None):
    title = get_default(title, Q.title.valid())
    text = get_default(text, Q.text.valid())
    return {
        "title": title,
        "text": text,
    }


def question_with_choices(title=None, text=None, choices=None):
    choices = get_default(choices, choice_list())
    return {**question(title=title, text=text), "choices": choices}
