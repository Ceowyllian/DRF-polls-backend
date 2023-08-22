import pytest
from django.core.exceptions import PermissionDenied, ValidationError

from db.polls.models import Question
from services.polls import (
    cancel_vote,
    choices_create,
    perform_vote,
    question_create,
    question_destroy,
    question_update,
)

from .conftest import C, Q


def get_default(value, default):
    return default if value is None else value


def choice_list(number=None, text=None):
    number = get_default(number, C.number.valid())
    text = get_default(text, C.text.valid())
    return [next(text) for _ in range(number)]


def question_dict(title=None, text=None):
    title = get_default(title, Q.title.valid())
    text = get_default(text, Q.text.valid())
    return {
        "title": title,
        "text": text,
    }


def question_with_choices(title=None, text=None, choices=None):
    choices = get_default(choices, choice_list())
    return {**question_dict(title=title, text=text), "choices": choices}


class TestQuestionCreate:
    def test_created_successfully(self, user):
        question_data = question_with_choices()
        question = question_create(created_by=user, **question_data)
        del question_data["choices"]
        for field, value in question_data.items():
            assert getattr(question, field) == value

    def test_fail_too_short_title(self, user):
        self.fail(title=Q.title.too_short(), created_by=user)

    def test_fail_too_long_title(self, user):
        self.fail(title=Q.title.too_long(), created_by=user)

    def test_fail_too_short_text(self, user):
        self.fail(title=Q.text.too_short(), created_by=user)

    def test_fail_too_long_text(self, user):
        self.fail(title=Q.text.too_long(), created_by=user)

    @staticmethod
    def fail(**kwargs):
        question_data = question_with_choices()
        for key, value in kwargs.items():
            question_data[key] = value
        with pytest.raises(ValidationError):
            question_create(**question_data)


class TestCreateChoiceInstances:
    def test_created_successfully(self, question):
        choices = choice_list()

        instances = choices_create(question=question, new_choices=choices)

        assert len(instances) == len(choices)
        for choice_instance in instances:
            assert choice_instance.text in choices

    def test_fail_too_many_choices(self, question):
        self.fail(question, number=C.number.too_many())

    def test_fail_too_few_choices(self, question):
        self.fail(question, number=C.number.too_few())

    def test_fail_empty_text_choices(self, question):
        self.fail(question, text=C.text.empty())

    def test_fail_too_long_text_choices(self, question):
        self.fail(question, text=C.text.too_long())

    def test_fail_identical_choices(self, question):
        self.fail(question, text=C.text.identical())

    @staticmethod
    def fail(question, **kwargs):
        choices = choice_list(**kwargs)
        with pytest.raises(ValidationError):
            choices_create(question=question, new_choices=choices)


class TestQuestionDestroy:
    def test_destroyed_successfully(self, question, user):
        question_destroy(question_pk=question.pk, destroyed_by=user)
        with pytest.raises(Question.DoesNotExist):
            Question.objects.get(id=question.pk)

    def test_fail_question_does_not_exist(self, question, user):
        question.delete()
        with pytest.raises(Question.DoesNotExist):
            question_destroy(question_pk=question.pk, destroyed_by=user)

    def test_fail_cannot_destroy_someone_elses_question(self, question, another_user):
        with pytest.raises(PermissionDenied):
            question_destroy(question_pk=question.pk, destroyed_by=another_user)


class TestQuestionUpdate:
    def test_update_successfully(self, user, question):
        updated_fields = question_dict()

        question_update(question_pk=question.pk, updated_by=user, data=updated_fields)
        question.refresh_from_db()

        for field, value in updated_fields.items():
            assert getattr(question, field) == value

    def test_fail_to_update_someone_elses_question(self, question, another_user):
        updated_fields = question_dict()
        with pytest.raises(PermissionDenied):
            question_update(
                question_pk=question.pk, updated_by=another_user, data=updated_fields
            )

    def test_fail_to_update_invalid_values(self, user, question):
        updated_fields = question_dict(
            title=Q.title.too_long(), text=Q.title.too_short()
        )

        with pytest.raises(ValidationError):
            question_update(
                question_pk=question.pk, updated_by=user, data=updated_fields
            )


class TestPerformVote:
    def test_perform_vote_successfully(self, user, choice_a):
        assert choice_a.vote_set.count() == 0
        perform_vote(choice_pk=choice_a.pk, user=user)
        assert choice_a.vote_set.count() == 1

    def test_fail_to_vote_twice_for_the_same_choice(self, user, choice_a):
        perform_vote(choice_pk=choice_a.pk, user=user)
        with pytest.raises(ValidationError):
            perform_vote(choice_pk=choice_a.pk, user=user)

    def test_fail_to_vote_twice_for_the_same_question(self, user, choice_a, choice_b):
        assert choice_a.question == choice_b.question
        perform_vote(choice_pk=choice_a.pk, user=user)
        with pytest.raises(ValidationError):
            perform_vote(choice_pk=choice_b.pk, user=user)


class TestCancelVote:
    def test_cancel_vote_successfully(self, user, vote):
        choice = vote.choice
        cancel_vote(choice_pk=choice.pk, user=user)
        assert choice.vote_set.count() == 0

    def test_fail_user_did_not_vote(self, user, vote):
        choice = vote.choice
        vote.delete()
        with pytest.raises(ValidationError):
            cancel_vote(choice_pk=choice.pk, user=user)
