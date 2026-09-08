from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, \
    GetExerciseResponseSchema, ExerciseSchema, UpdateExerciseRequestSchema, UpdateExerciseResponseSchema, \
    GetExercisesResponseSchema
from tools.assertions.base import assert_equal, assert_length
from tools.assertions.errors import assert_internal_error_response
import allure
from tools.logger import get_logger

logger = get_logger("EXERCISES_ASSERTIONS")


@allure.step("Assert exercise")
def assert_exercise(actual: ExerciseSchema, expected: ExerciseSchema):
    """
    Проверяет, что фактические данные задания соответствуют ожидаемым.

    :param actual: Фактические данные задания.
    :param expected: Ожидаемые данные задания.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Assert exercise")

    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.title, expected.title, "title")
    assert_equal(actual.course_id, expected.course_id, "courseId")
    assert_equal(actual.max_score, expected.max_score, "maxScore")
    assert_equal(actual.min_score, expected.min_score, "minScore")
    assert_equal(actual.order_index, expected.order_index, "orderIndex")
    assert_equal(actual.description, expected.description, "description")
    assert_equal(actual.estimated_time, expected.estimated_time, "estimatedTime")


@allure.step("Assert get exercise response")
def assert_get_exercise_response(
        get_exercise_response: GetExerciseResponseSchema,
        create_exercise_response: CreateExerciseResponseSchema,
):
    """
    Проверяет, что ответ на получение задания соответствует ответу на его создание.

    :param get_exercise_response: Ответ API при запросе данных задания.
    :param create_exercise_response: Ответ API при создании задания.
    :raises AssertionError: Если данные задания не совпадают.
    """
    logger.info("Assert get exercise response")

    assert_exercise(get_exercise_response.exercise, create_exercise_response.exercise)


@allure.step("Assert create exercise response")
def assert_create_exercise_response(
        request: CreateExerciseRequestSchema,
        response: CreateExerciseResponseSchema,
):
    """
    Проверяет, что ответ на создание задания соответствует данным запроса.

    :param request: Данные запроса на создание задания.
    :param response: Ответ API при создании задания.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Assert create exercise response")

    assert_equal(response.exercise.title, request.title, "title")
    assert_equal(response.exercise.course_id, request.course_id, "courseId")
    assert_equal(response.exercise.max_score, request.max_score, "maxScore")
    assert_equal(response.exercise.min_score, request.min_score, "minScore")
    assert_equal(response.exercise.order_index, request.order_index, "orderIndex")
    assert_equal(response.exercise.description, request.description, "description")
    assert_equal(response.exercise.estimated_time, request.estimated_time, "estimatedTime")


@allure.step("Assert update exercise response")
def assert_update_exercise_response(
        request: UpdateExerciseRequestSchema,
        response: UpdateExerciseResponseSchema,
):
    """
    Проверяет, что ответ на обновление задания соответствует данным запроса.

    :param request: Данные запроса на обновление задания.
    :param response: Ответ API при обновлении задания.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Assert update exercise response")

    if request.title is not None:
        assert_equal(response.exercise.title, request.title, "title")
    if request.max_score is not None:
        assert_equal(response.exercise.max_score, request.max_score, "maxScore")
    if request.min_score is not None:
        assert_equal(response.exercise.min_score, request.min_score, "minScore")
    if request.order_index is not None:
        assert_equal(response.exercise.order_index, request.order_index, "orderIndex")
    if request.description is not None:
        assert_equal(response.exercise.description, request.description, "description")
    if request.estimated_time is not None:
        assert_equal(response.exercise.estimated_time, request.estimated_time, "estimatedTime")


@allure.step("Assert exercise not found response")
def assert_exercise_not_found_response(response: InternalErrorResponseSchema):
    """
    Проверяет, что ответ API соответствует ошибке «задание не найдено».

    :param response: Десериализованный ответ API с внутренней ошибкой.
    :raises AssertionError: Если сообщение об ошибке не содержит ожидаемого текста.
    """
    logger.info("Assert exercise not found response")

    expected = InternalErrorResponseSchema(details="Exercise not found")
    assert_internal_error_response(response, expected)


@allure.step("Assert get exercises response")
def assert_get_exercises_response(
        get_exercises_response: GetExercisesResponseSchema,
        create_exercise_responses: list[CreateExerciseResponseSchema]
):
    """
    Проверяет, что ответ на получение списка заданий соответствует ответам на их создание.

    :param get_exercises_response: Ответ API при запросе списка заданий.
    :param create_exercise_responses: Список ответов API при создании заданий.
    :raises AssertionError: Если данные заданий не совпадают.
    """
    logger.info("Assert get exercises response")

    assert_length(get_exercises_response.exercises, create_exercise_responses, "exercises")

    for index, create_exercise_response in enumerate(create_exercise_responses):
        assert_exercise(get_exercises_response.exercises[index], create_exercise_response.exercise)
