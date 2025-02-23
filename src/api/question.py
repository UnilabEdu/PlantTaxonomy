from flask_restx import Resource, reqparse

from src.ext import api
from src.models import Question


@api.route("/questions/<int:question_id>")
class QuestionAPI(Resource):
    def get(self, question_id):
        question = Question.query.filter_by(id=question_id)
        paired_question = Question.query.filter_by(pair_number=question.pair_number)

        response = [
            {
                "question": question.text,
                "next_question_id": question.question_id,
                "identified_plant_id": question.plant_id,
            }
        ]

        if paired_question:
            response.append({
                "question": paired_question.text,
                "next_question_id": paired_question.question_id,
                "identified_plant_id": paired_question.plant_id,
            })

        return response, 200