from clients.api_client import APIClient
from httpx import Response
from clients.private_http_builder import get_private_http_client, AuthenticationUserSchema
from clients.exercises.exercises_schema import GetExerciseQuerySchema, CreateExerciseRequestSchema, \
    UpdateExerciseRequestSchema, GetExercisesResponseSchema


class ExercisesClient(APIClient):
    """
    Клиент для работы с /api/v1/exercises
    """

    def get_exercises_api(self, query: GetExerciseQuerySchema) -> Response:
        """
        Метод получения списка заданий.

        :param query: Словарь с courseId.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(f'/api/v1/exercises', params=query.model_dump(by_alias=True))

    def get_exercise_api(self, exercise_id: str) -> Response:
        """
        Метод получения задания.

        :param exercise_id: Идентификатор задания.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(f'/api/v1/exercises/{exercise_id}')

    def create_exercise_api(self, request: CreateExerciseRequestSchema) -> Response:
        """
        Метод создания задания.

        :param request: Словарь с title, courseId, maxScore, minScore, orderIndex, description, estimatedTime.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post(f'/api/v1/exercises', json=request.model_dump(by_alias=True))

    def update_exercise_api(self, exercise_id: str, request: UpdateExerciseRequestSchema) -> Response:
        """
        Метод обновления задания.

        :param exercise_id: Идентификатор курса.
        :param request: Словарь с title, maxScore, minScore, orderIndex, description, estimatedTime.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.patch(f'/api/v1/exercises/{exercise_id}', json=request.model_dump(by_alias=True))

    def delete_exercise_api(self, exercise_id: str) -> Response:
        """
        Метод удаления задания.

        :param exercise_id: Идентификатор курса.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.delete(f'/api/v1/exercises/{exercise_id}')

    def get_exercise(self, exercise_id: str) -> GetExercisesResponseSchema:
        response = self.get_exercise_api(exercise_id)
        return GetExercisesResponseSchema.model_validate_json(response.text)

    def get_exercises(self, query: GetExerciseQuerySchema) -> GetExercisesResponseSchema:
        response = self.get_exercises_api(query=query)
        return GetExercisesResponseSchema.model_validate_json(response.text)

    def create_exercise(self, request: CreateExerciseRequestSchema) -> GetExercisesResponseSchema:
        response = self.create_exercise_api(request=request)
        return GetExercisesResponseSchema.model_validate_json(response.text)

    def update_exercise(self, exercise_id: str, request: UpdateExerciseRequestSchema) -> GetExercisesResponseSchema:
        response = self.update_exercise_api(exercise_id=exercise_id, request=request)
        return GetExercisesResponseSchema.model_validate_json(response.text)


def get_exercises_client(user: AuthenticationUserSchema) -> ExercisesClient:
    """
    Функция создаёт экземпляр ExercisesClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию CoursesClient.
    """
    return ExercisesClient(client=get_private_http_client(user))
