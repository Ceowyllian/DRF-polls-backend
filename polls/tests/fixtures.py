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
            return QuestionConfig.CHOICES_MAX_NUMBER

        @staticmethod
        def too_many():
            return QuestionConfig.CHOICES_MAX_NUMBER + 1

        @staticmethod
        def too_few():
            return QuestionConfig.CHOICES_MIN_NUMBER - 1

    class text:
        @staticmethod
        def valid():
            i = 0
            while True:
                i += 1
                yield get_random_string(ChoiceConfig.TEXT_MAX_LEN - len(str(i))) + str(i)

        @staticmethod
        def empty():
            while True:
                yield ''

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


def choice_list(number=C.number.valid(), text=C.text.valid()):
    return [next(text) for _ in range(number)]


def question(
        title=Q.title.valid(),
        text=Q.text.valid(),
):
    return {
        'title': title,
        'text': text,
    }


def question_with_choices(
        title=Q.title.valid(),
        text=Q.text.valid(),
        choices=None
):
    choices_value = choices if choices is not None else choice_list()
    return {
        'title': title,
        'text': text,
        'choices': choices_value
    }
