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
from tests.polls.factories import (
    QuestionChoicesDictFactory,
    QuestionDictFactory,
    WrongChoice,
    WrongQuestion,
)


def get_default(value, default):
    return default if value is None else value


class TestQuestionCreate:
    def test_created_successfully(self, user, question_with_choices_dict):
        question = question_create(**question_with_choices_dict, created_by=user)
        choices = question_with_choices_dict.pop("choices")
        for field, value in question_with_choices_dict.items():
            assert getattr(question, field) == value
        for choice in question.choice_set.all():
            assert choice.text in choices

    def test_fail_too_short_title(self, user):
        self.fail(user, title=WrongQuestion.title_too_short)

    def test_fail_too_long_title(self, user):
        self.fail(user, title=WrongQuestion.title_too_long)

    def test_fail_too_short_text(self, user):
        self.fail(user, title=WrongQuestion.text_too_short)

    def test_fail_too_long_text(self, user):
        self.fail(user, title=WrongQuestion.text_too_long)

    @staticmethod
    def fail(user, **kwargs):
        with pytest.raises(ValidationError):
            question_create(**QuestionChoicesDictFactory(**kwargs), created_by=user)


class TestCreateChoiceInstances:
    def test_created_successfully(self, question, choice_list):
        instances = choices_create(question=question, new_choices=choice_list)
        assert len(instances) == len(choice_list)
        for choice_instance in instances:
            assert choice_instance.text in choice_list

    def test_fail_too_many_choices(self, question):
        self.fail(question, WrongChoice.list_too_long)

    def test_fail_too_few_choices(self, question):
        self.fail(question, WrongChoice.list_too_short)

    def test_fail_empty_text_choices(self, question):
        self.fail(question, WrongChoice.list_with_empty_choices)

    def test_fail_too_long_text_choices(self, question, choice_list):
        choice_list[0] = WrongChoice.too_long_text
        self.fail(question, choice_list)

    def test_fail_identical_choices(self, question):
        self.fail(question, WrongChoice.identical_choices)

    @staticmethod
    def fail(question, choices):
        with pytest.raises(ValidationError):
            choices_create(question=question, new_choices=choices)


class TestQuestionDestroy:
    def test_destroyed_successfully(self, question, user):
        question_destroy(question=question, destroyed_by=user)
        with pytest.raises(Question.DoesNotExist):
            Question.objects.get(id=question.pk)

    def test_fail_cannot_destroy_someone_elses_question(self, question, another_user):
        with pytest.raises(PermissionDenied):
            question_destroy(question=question, destroyed_by=another_user)


class TestQuestionUpdate:
    def test_update_successfully(self, user, question, question_dict):
        question_update(question=question, updated_by=user, data=question_dict)
        question.refresh_from_db()

        for field, value in question_dict.items():
            assert getattr(question, field) == value

    def test_fail_to_update_someone_elses_question(
        self, question, another_user, question_dict
    ):
        with pytest.raises(PermissionDenied):
            question_update(
                question=question, updated_by=another_user, data=question_dict
            )

    def test_fail_to_update_invalid_values(self, user, question):
        with pytest.raises(ValidationError):
            question_update(
                question=question,
                updated_by=user,
                data=QuestionDictFactory(text=WrongQuestion.text_too_long),
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
