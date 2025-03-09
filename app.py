from flask import Flask, request, jsonify, redirect
import hashlib
import asyncio

app = Flask(__name__)

# Словарь для хранения сокращенных URL
url_mapping = {}

# Эндпоинт для сокращения URL
@app.route('/', methods=['POST'])
def shorten_url():
    original_url = request.json.get('url')
    if not original_url:
        return jsonify({"error": "URL is required"}), 400

    # Генерация уникального идентификатора для сокращенного URL
    url_hash = hashlib.md5(original_url.encode()).hexdigest()[:8]
    url_mapping[url_hash] = original_url

    # Возвращаем сокращенный URL с кодом 201
    return jsonify({"short_url": f"http://127.0.0.1:8080/{url_hash}"}), 201

# Эндпоинт для перенаправления на оригинальный URL
@app.route('/<shorten_url_id>', methods=['GET'])
def redirect_to_original(shorten_url_id):
    original_url = url_mapping.get(shorten_url_id)
    if not original_url:
        return jsonify({"error": "URL not found"}), 404

    # Перенаправляем на оригинальный URL с кодом 307
    return redirect(original_url, code=307)

# Асинхронный эндпоинт
async def async_task():
    await asyncio.sleep(2)  # Имитация асинхронной задачи
    return {"data": "Async task completed"}

@app.route('/async', methods=['GET'])
def async_endpoint():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(async_task())
    return jsonify(result)

# Запуск сервера
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
