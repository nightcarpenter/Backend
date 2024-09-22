import json
import math
from typing import Any, Awaitable, Callable

# Основная ASGI-функция, обрабатывающая запросы
async def application(
    scope: dict[str, Any],
    receive: Callable[[], Awaitable[dict[str, Any]]],
    send: Callable[[dict[str, Any]], Awaitable[None]]
) -> None:

    # Проверка типа запроса (http)
    if scope['type'] == 'http':
        # Получение метода запроса
        method = scope['method']
        # Получение пути запроса
        path = scope['path']

        # Проверка, что метод запроса - GET
        if method == 'GET':
            # Обработка запроса на вычисление факториала
            if path == '/factorial':
                # Получение строки запроса
                query_string = scope['query_string'].decode()
                # Разбор параметров из строки запроса
                params = dict(q.split('=') for q in query_string.split('&') if '=' in q)
                # Получение параметра n, если он отсутствует, значение по умолчанию - 0
                n = int(params.get('n', 0))

                # Проверка, что n не отрицательное
                if n < 0:
                    # Формирование ответа с ошибкой
                    response_body = json.dumps({'error': 'Number must be non-negative'})
                    status_code = 400
                else:
                    # Вычисление факториала
                    result = math.factorial(n)
                    # Формирование ответа с результатом
                    response_body = json.dumps({'factorial': result})
                    status_code = 200

                # Отправка ответа
                await send_response(send, response_body, status_code)

            # Обработка запроса на вычисление последовательности Фибоначчи
            elif path == '/fibonacci':
                # Получение строки запроса
                query_string = scope['query_string'].decode()
                # Разбор параметров из строки запроса
                params = dict(q.split('=') for q in query_string.split('&') if '=' in q)
                # Получение параметра limit, если он отсутствует, значение по умолчанию - 10
                limit = int(params.get('limit', 10))

                # Проверка, что limit не отрицательное
                if limit < 0:
                    # Формирование ответа с ошибкой
                    response_body = json.dumps({'error': 'Limit must be non-negative'})
                    status_code = 400
                else:
                    # Вычисление последовательности Фибоначчи
                    fib_sequence = fibonacci(limit)
                    # Формирование ответа с результатом
                    response_body = json.dumps({'fibonacci': fib_sequence})
                    status_code = 200

                # Отправка ответа
                await send_response(send, response_body, status_code)

            # Обработка запроса на вычисление среднего арифметического
            elif path == '/mean':
                # Получение строки запроса
                query_string = scope['query_string'].decode()
                # Разбор параметров из строки запроса
                params = dict(q.split('=') for q in query_string.split('&') if '=' in q)
                # Получение параметра numbers, представляющего собой строку чисел через запятую
                numbers_str = params.get('numbers', '')

                try:
                    # Преобразование строки чисел в список чисел
                    numbers = [float(num) for num in numbers_str.split(',')]
                    # Если список чисел пустой, вызвать ошибку
                    if not numbers:
                        raise ValueError()
                    # Вычисление среднего арифметического
                    mean_value = sum(numbers) / len(numbers)
                    # Формирование ответа с результатом
                    response_body = json.dumps({'mean': mean_value})
                    status_code = 200
                except ValueError:
                    # Формирование ответа с ошибкой при некорректном вводе
                    response_body = json.dumps({
                        'error': 'Invalid input, must be a comma-separated list of numbers'
                    })
                    status_code = 400

                # Отправка ответа
                await send_response(send, response_body, status_code)

            # Обработка запроса на неизвестный путь
            else:
                # Формирование ответа с ошибкой "Не найдено"
                response_body = json.dumps({'error': 'Not found'})
                status_code = 404
                # Отправка ответа
                await send_response(send, response_body, status_code)

# Функция для отправки HTTP-ответа
async def send_response(
    send: Callable[[dict[str, Any]], Awaitable[None]],
    body: str,
    status: int
) -> None:
    # Отправка заголовков ответа
    await send({
        'type': 'http.response.start',
        'status': status,
        'headers': [
            (b'content-type', b'application/json')
        ]
    })
    # Отправка тела ответа
    await send({
        'type': 'http.response.body',
        'body': body.encode('utf-8')
    })

# Функция для вычисления последовательности Фибоначчи
def fibonacci(limit: int):
    # Начальная последовательность Фибоначчи
    sequence = [0, 1]
    # Генерация последовательности до достижения заданного лимита
    while len(sequence) < limit:
        sequence.append(sequence[-1] + sequence[-2])
    # Возврат последовательности с длиной limit
    return sequence[:limit]