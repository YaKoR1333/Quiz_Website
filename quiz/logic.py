from django.http import JsonResponse

from quiz.models import Question, Answer, Quiz, Result


def _get_questions_list(data_dict: dict) -> list:
    questions = []
    list(map(lambda k: questions.append(Question.objects.get(text=k)), data_dict.keys()))
    return questions


def _get_checkbox_answers(question, request) -> list[str]:
    a_selected = request.POST.get(question.text)
    a_selected_list = a_selected.split(',')
    a_selected_list.remove('')
    return a_selected_list


def _get_correct_question_answers(question) -> list[str]:
    question_answers_list = []
    question_answers = Answer.objects.filter(question=question)
    list(map(lambda answer: (question_answers_list.append(answer.text)) if answer.correct else False, question_answers))
    return question_answers_list


def _score_counting(checkbox_answers: list, question_answers: list) -> int:
    score = 0
    if len(checkbox_answers) == len(question_answers):
        for checkbox_answer in checkbox_answers:
            if checkbox_answer in question_answers:
                continue
            else:
                break
        else:
            score += 1
    return score


def scored_logic(data: dict, request, pk) -> JsonResponse:
    questions = _get_questions_list(data)
    quiz = Quiz.objects.get(pk=pk)
    user = request.user
    multiplier = 100 / quiz.number_of_questions
    score = 0
    results = []
    for question in questions:
        a_selected = _get_checkbox_answers(question, request)
        correct_answers = _get_correct_question_answers(question)
        results.append({str(question): {'correct_answers': correct_answers, 'answered': a_selected}})
        score += _score_counting(a_selected, correct_answers)
    score_ = score * multiplier
    Result.objects.create(quiz=quiz, user=user, score=score_)
    return JsonResponse({'score': score_, 'results': results})
