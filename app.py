import requests
import json
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import uvicorn
import os
from fastapi.middleware.cors import CORSMiddleware  # 新增这行导入

DEFAULT_MODEL = 'Meta-Llama-3.1-8B-Instruct'
API_URL = 'https://fast.snova.ai/api/completion'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
STOP_SEQUENCE = "<|eot_id|>"
DEFAULT_ENV_TYPE = "tp16"

MODEL_ENV_MAPPING = {
    "Meta-Llama-3.1-8B-Instruct": "tp16",
    "Meta-Llama-3.1-70B-Instruct": "tp1670b",
    "Meta-Llama-3.1-405B-Instruct": "tp16405b"
}

app = FastAPI()

# 添加以下CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源,您可以根据需要限制特定域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有HTTP头
)

@app.post("/v1/chat/completions")
async def completions(request: Request):
    completion_data = await request.json()

    model = completion_data.get('model', DEFAULT_MODEL)
    messages = completion_data.get('messages', [])
    stream = completion_data.get('stream', True)

    headers = {
        'User-Agent': USER_AGENT,
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream',
    }

    env_type = MODEL_ENV_MAPPING.get(model, DEFAULT_ENV_TYPE)

    data = {
        "body": {
            "messages": messages,
            "stop": [STOP_SEQUENCE],
            "stream": True,
            "stream_options": {"include_usage": True},
            "model": model
        },
        "env_type": env_type
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(data), stream=True)
    
    if stream:
        return handle_stream_response(response)
    else:
        return handle_non_stream_response(response)

def handle_stream_response(response):
    return StreamingResponse(response.iter_content(), media_type="text/event-stream")

def handle_non_stream_response(response):
    lines = response.text.split('\n\n')
    
    new_lines = []
    for line in lines:
        if not line.startswith('data:'):
            continue
        line = line.removeprefix('data: ')
        if 'DONE' in line:
            continue
        j = json.loads(line)
        new_lines.append(j)
    
    last_obj = new_lines[-1]
    
    content = ''
    for line in new_lines:
        if len(line['choices']) == 0:
            continue
        delta = line['choices'][0]['delta']
        if 'content' not in delta:
            continue
        content += delta['content']
    
    last_obj['choices'] = new_lines[0]['choices']
    last_obj['choices'][0]['delta']['content'] = content
    return last_obj

if __name__ == "__main__":
    work_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(work_dir)
    port = int(os.environ.get("PORT", 3335))
    uvicorn.run("app:app", host="0.0.0.0", port=port)