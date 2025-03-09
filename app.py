from flask import Flask, request, jsonify, redirect
import hashlib
import asyncio

app = Flask(__name__)

# Dictionary for storing shortened URLs
url_mapping = {}

# Endpoint for URL shortening
@app.route('/', methods=['POST'])
def shorten_url():
    original_url = request.json.get('url')
    if not original_url:
        return jsonify({"error": "URL is required"}), 400

    # Generating a unique identifier for a shortened URL
    url_hash = hashlib.md5(original_url.encode()).hexdigest()[:8]
    url_mapping[url_hash] = original_url

    # We return the shortened URL with the 201 code.
    return jsonify({"short_url": f"http://127.0.0.1:8080/{url_hash}"}), 201

# Endpoint for redirection to the original URL
@app.route('/<shorten_url_id>', methods=['GET'])
def redirect_to_original(shorten_url_id):
    original_url = url_mapping.get(shorten_url_id)
    if not original_url:
        return jsonify({"error": "URL not found"}), 404

    # Redirecting to the original URL with the 307 code
    return redirect(original_url, code=307)

# Asynchronous endpoint
async def async_task():
    await asyncio.sleep(2)  # Simulating an asynchronous task
    return {"data": "Async task completed"}

@app.route('/async', methods=['GET'])
def async_endpoint():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(async_task())
    return jsonify(result)

# Starting the server
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
