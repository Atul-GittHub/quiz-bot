
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(self, user_id, answer):
    # Validate the answer (e.g., check if it's in the correct format)
    if not isinstance(answer, str):
        return False

    # Store the answer in the session or database
    user_session = self.get_user_session(user_id)
    user_session['current_answer'] = answer
    self.save_user_session(user_id, user_session)

    return True


def get_next_question(self, user_id):
    user_session = self.get_user_session(user_id)
    questions = self.get_all_questions()
    
    # Determine the next question index
    current_question_index = user_session.get('current_question_index', 0)
    
    if current_question_index >= len(questions):
        return None  # No more questions
    
    next_question = questions[current_question_index]
    user_session['current_question_index'] = current_question_index + 1
    self.save_user_session(user_id, user_session)
    
    return next_question


def generate_final_response(self, user_id):
    user_session = self.get_user_session(user_id)
    answers = user_session.get('answers', [])
    correct_answers = self.get_correct_answers()

    # Calculate the score
    score = sum(1 for user_answer, correct_answer in zip(answers, correct_answers) if user_answer == correct_answer)

    # Generate the final response
    response = {
        "score": score,
        "total_questions": len(correct_answers),
        "message": f"Your final score is {score} out of {len(correct_answers)}."
    }

    return response
