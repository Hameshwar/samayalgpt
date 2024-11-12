from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_URL = 'https://integrate.api.nvidia.com/v1'
API_KEY = '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'

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    user_message = data['query']
    
    response = requests.post(f'{API_URL}/chat/completions', headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }, json={
        'model': 'nvidia/llama-3.1-nemotron-70b-instruct',
        'messages': [{'role': 'user', 'content': user_message}],
        'temperature': 0.5,
        'top_p': 1,
        'max_tokens': 1024,
        'stream': True
    })

    ai_response = ""
    for chunk in response.iter_content(chunk_size=128):
        if chunk:
            ai_response += chunk.decode('utf-8')
    
    return jsonify({'answer': ai_response})

if __name__ == '__main__':
    app.run(debug=True)
