import pytest
from model import Question, Choice


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    question.add_choice('a', False)
    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct


# ------------------------------
# Novos testes
# ------------------------------

def test_choice_with_empty_text():
    with pytest.raises(Exception):
        Choice(id=1, text='', is_correct=False)

def test_choice_with_too_long_text():
    with pytest.raises(Exception):
        Choice(id=1, text='a' * 101)

def test_remove_choice_by_id():
    question = Question(title='q1')
    c1 = question.add_choice('a')
    question.remove_choice_by_id(c1.id)
    assert len(question.choices) == 0

def test_remove_invalid_choice_id():
    question = Question(title='q1')
    question.add_choice('a')
    with pytest.raises(Exception):
        question.remove_choice_by_id(99)

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.remove_all_choices()
    assert len(question.choices) == 0

def test_set_correct_choices_and_verify():
    question = Question(title='q1')
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    question.set_correct_choices([c1.id])
    assert c1.is_correct
    assert not c2.is_correct

def test_correct_selected_choices_valid():
    question = Question(title='q1', max_selections=2)
    c1 = question.add_choice('a', True)
    c2 = question.add_choice('b', False)
    result = question.correct_selected_choices([c1.id, c2.id])
    assert result == [c1.id]

def test_correct_selected_choices_exceeding_max():
    question = Question(title='q1', max_selections=1)
    c1 = question.add_choice('a', True)
    c2 = question.add_choice('b', False)
    with pytest.raises(Exception):
        question.correct_selected_choices([c1.id, c2.id])

def test_generate_incremental_choice_ids():
    question = Question(title='q1')
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    assert c1.id == 1
    assert c2.id == 2

def test_find_correct_choice_ids():
    question = Question(title='q1')
    c1 = question.add_choice('a', True)
    c2 = question.add_choice('b', False)
    assert question._find_correct_choice_ids() == [c1.id]

    
# ------------------------------
# Fixture
# ------------------------------

@pytest.fixture
def sample_question():
    """Retorna uma questão com 3 alternativas, sendo a primeira correta."""
    q = Question(title="Sample Question", max_selections=2)
    c1 = q.add_choice("Option A", True)
    c2 = q.add_choice("Option B", False)
    c3 = q.add_choice("Option C", False)
    return q

# ------------------------------
# Testes usando a fixture
# ------------------------------

def test_fixture_question_has_choices(sample_question):
    assert len(sample_question.choices) == 3
    assert any(c.is_correct for c in sample_question.choices)

def test_fixture_correct_selection(sample_question):
    correct_ids = [c.id for c in sample_question.choices if c.is_correct]
    result = sample_question.correct_selected_choices(correct_ids)
    assert result == correct_ids