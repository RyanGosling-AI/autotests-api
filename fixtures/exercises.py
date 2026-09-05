from http import HTTPStatus

import pytest
from pydantic import BaseModel
from clients.exercises.exercises_client import ExercisesClient, get_exercises_client
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, GetExercisesResponseSchema, \
    CreateExerciseResponseSchema
from fixtures.courses import CourseFixture
from tools.assertions.base import assert_status_code


class ExerciseFixture(BaseModel):
    request: CreateExerciseRequestSchema
    response: CreateExerciseResponseSchema


@pytest.fixture
def exercises_client(function_user) -> ExercisesClient:
    return get_exercises_client(function_user.authentication_user)


@pytest.fixture
def function_exercise(
        exercises_client: ExercisesClient,
        function_course: CourseFixture,
) -> ExerciseFixture:
    request = CreateExerciseRequestSchema(
        course_id=function_course.response.course.id,
    )
    response = exercises_client.create_exercise_api(request)

    assert_status_code(response.status_code, HTTPStatus.OK)

    return ExerciseFixture(
        request=request,
        response=CreateExerciseResponseSchema.model_validate_json(response.text),
    )
