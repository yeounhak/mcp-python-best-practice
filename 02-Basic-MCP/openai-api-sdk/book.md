<div align="center" style="background:#fffbe6; border-radius:20px; box-shadow:0 4px 16px #eee; padding:40px 20px; margin:40px 0;">
  <span style="font-size:1.5em;">🚀</span>
  <div style="margin:10px 0 10px 0;">
    <span style="font-size:1.3em; font-weight:bold; color:#222;">
      OpenAI API를 Python SDK와 Bash curl 두 가지 방식으로 구현하여 </br>
      스트리밍 응답 처리와 비동기 프로그래밍 패턴을 학습할 수 있습니다.
    </span>
  </div>
</div>

## 📋 개요

이 프로젝트는 OpenAI API를 두 가지 방식으로 호출하는 예제를 제공합니다. Python의 `AsyncOpenAI` SDK를 사용한 비동기 구현과 Bash의 curl 명령어를 사용한 직접 HTTP 호출 방식을 비교하여 학습할 수 있습니다. 두 방식 모두 스트리밍 응답을 처리하는 방법을 보여주며, 실제 프로덕션 환경에서 OpenAI API를 효과적으로 활용하는 방법을 익힐 수 있습니다.

Python 구현에서는 `asyncio`와 `async/await` 패턴을 활용한 비동기 프로그래밍을 통해 효율적인 API 호출을 보여주며, Bash 구현에서는 curl을 통한 직접적인 HTTP 요청으로 API의 기본 구조를 이해할 수 있습니다. 두 방식 모두 스트리밍을 활용하여 실시간으로 응답을 받는 방법을 다룹니다.

> 🔗 **상세 코드 및 예제**: [https://github.com/yeounhak/mcp-python-best-practice/02-Basic-MCP/openai-api-sdk][github-repo]

[github-repo]: https://github.com/yeounhak/mcp-python-best-practice/02-Basic-MCP/openai-api-sdk

## 📁 파일 구성

```
openai-api-sdk/
├── openai.py          # Python SDK를 사용한 비동기 OpenAI API 호출
└── openai.sh          # Bash curl을 사용한 HTTP API 직접 호출
```

### 주요 파일 설명

**openai.py**
```python
# openai-api-sdk/openai.py 파일입니다.
from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key = "sk-..."
)

async def main():
    stream = await client.chat.completions.create(
        model="gpt-5",
        messages=[{"role":"assistant", "content": "hi"}],
        stream=True
    )
    async for chunk in stream:
        print(chunk)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

- `AsyncOpenAI` 클라이언트를 사용하여 비동기 API 호출 구현
- `stream=True` 설정으로 실시간 스트리밍 응답 처리
- `async for` 루프를 통해 스트리밍 청크를 순차적으로 처리
- GPT-5 모델을 사용하여 채팅 완성 API 호출

**openai.sh**
```bash
# openai-api-sdk/openai.sh 파일입니다.
#!/bin/bash

# OpenAI GPT API curl script
# Replace YOUR_API_KEY with your actual OpenAI API key

OPENAI_API_KEY="sk-..."
MODEL="gpt-4"

curl -X POST \
  https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "'$MODEL'",
    "messages": [
      {
        "role": "user",
        "content": "hi"
      }
    ],
    "stream": true
  }'
```

- curl 명령어를 사용한 직접적인 HTTP POST 요청
- Bearer Token 인증을 통한 API 키 인증 처리
- JSON 페이로드를 통한 채팅 완성 요청 구성
- `"stream": true` 설정으로 스트리밍 응답 활성화
- GPT-4 모델을 사용한 단순한 "hi" 메시지 처리

## 🚀 실행

### 사전 요구사항

**1. Python 패키지 설치**
```bash
pip install openai
```

**2. OpenAI API 키 설정**
- OpenAI 계정에서 API 키를 발급받아야 합니다
- 코드 내의 `"sk-..."` 부분을 실제 API 키로 교체해야 합니다

**3. 시스템 요구사항**
- Python 3.7 이상 (async/await 지원)
- Bash 환경 (shell 스크립트 실행용)
- curl 명령어 (대부분의 Unix/Linux 시스템에 기본 설치)

### 실행 방법

**1. Python SDK 방식 실행**
```bash
python openai.py
```

**2. Bash curl 방식 실행**
```bash
chmod +x openai.sh
./openai.sh
```

또는

```bash
bash openai.sh
```

### 실행 결과

**Python SDK 실행 결과:**
Python 스크립트를 실행하면 스트리밍 방식으로 응답이 출력됩니다:

```bash
ChatCompletionChunk(id='chatcmpl-ABC123', choices=[Choice(delta=ChoiceDelta(content='Hello', role=None), finish_reason=None, index=0)], created=1234567890, model='gpt-5', object='chat.completion.chunk')
ChatCompletionChunk(id='chatcmpl-ABC123', choices=[Choice(delta=ChoiceDelta(content='! How', role=None), finish_reason=None, index=0)], created=1234567890, model='gpt-5', object='chat.completion.chunk')
ChatCompletionChunk(id='chatcmpl-ABC123', choices=[Choice(delta=ChoiceDelta(content=' can I', role=None), finish_reason=None, index=0)], created=1234567890, model='gpt-5', object='chat.completion.chunk')
```

위 결과에서 확인할 수 있듯이:
- 각 청크는 `ChatCompletionChunk` 객체 형태로 반환됩니다
- `delta.content` 필드에 실제 응답 텍스트가 포함됩니다
- 스트리밍을 통해 응답이 실시간으로 도착하며 순차적으로 처리됩니다

**Bash curl 실행 결과:**
Shell 스크립트를 실행하면 Server-Sent Events 형태로 응답이 출력됩니다:

```bash
data: {"id":"chatcmpl-ABC123","object":"chat.completion.chunk","created":1234567890,"model":"gpt-4","choices":[{"index":0,"delta":{"role":"assistant","content":""},"finish_reason":null}]}

data: {"id":"chatcmpl-ABC123","object":"chat.completion.chunk","created":1234567890,"model":"gpt-4","choices":[{"index":0,"delta":{"content":"Hello"},"finish_reason":null}]}

data: {"id":"chatcmpl-ABC123","object":"chat.completion.chunk","created":1234567890,"model":"gpt-4","choices":[{"index":0,"delta":{"content":"! How can I help you today?"},"finish_reason":null}]}

data: [DONE]
```

위 결과에서 확인할 수 있듯이:
- Server-Sent Events(SSE) 프로토콜을 사용한 스트리밍 응답
- 각 데이터 청크는 `data:` 접두사로 시작하는 JSON 형태
- `delta.content` 필드에 실제 생성되는 텍스트 조각이 포함
- 응답 완료 시 `data: [DONE]` 메시지로 종료

## 📚 정리

이 예제는 OpenAI API를 활용하는 두 가지 핵심 접근 방식을 보여줍니다. Python SDK를 사용한 방식에서는 `AsyncOpenAI` 클라이언트와 `async/await` 패턴을 통해 비동기 프로그래밍의 장점을 활용하며, 스트리밍 응답을 효율적으로 처리하는 방법을 학습할 수 있습니다. 특히 `async for` 구문을 통해 스트리밍 청크를 순차적으로 처리하는 패턴은 실시간 채팅 애플리케이션이나 대화형 AI 서비스 구현에 매우 유용합니다. Bash curl 방식에서는 HTTP 프로토콜 수준에서 OpenAI API의 기본 구조를 이해할 수 있으며, Server-Sent Events를 통한 스트리밍 메커니즘을 직접 확인할 수 있습니다. 이러한 저수준 이해는 API 문제를 디버깅하거나 다른 프로그래밍 언어로 클라이언트를 구현할 때 매우 중요한 기초 지식이 됩니다. 두 방식 모두 스트리밍을 통해 실시간성을 확보하면서도 각각의 장단점을 가지고 있어, 프로젝트의 요구사항과 환경에 따라 적절한 방식을 선택할 수 있는 통찰력을 제공합니다.