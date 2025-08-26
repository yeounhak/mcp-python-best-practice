## 📋 개요

이 프로젝트는 LLM(Large Language Model) API를 직접 호출하는 방법을 보여주는 기본적인 예제입니다. Anthropic Claude API와 OpenAI GPT API에 대한 curl 명령어를 사용하여 HTTP 요청을 통해 각각의 AI 모델과 상호작용하는 방법을 다룹니다. 이는 MCP(Model Context Protocol) 학습의 기초 단계로, 복잡한 프레임워크나 라이브러리 없이 순수한 HTTP 통신만으로 LLM 서비스를 활용하는 방법을 제시합니다.

주요 기술 스택:
- **Shell Script**: Bash 스크립트를 통한 자동화된 API 호출
- **curl**: HTTP 클라이언트 도구를 활용한 REST API 통신
- **JSON**: API 요청 및 응답 데이터 포맷
- **Streaming Response**: 실시간 응답 스트리밍 처리

> 🔗 **상세 코드 및 예제**: [https://github.com/yeounhak/mcp-python-best-practice/02/Basic-MCP/01-llm-api][github-repo]

[github-repo]: https://github.com/yeounhak/mcp-python-best-practice/02/Basic-MCP/01-llm-api

## 📁 파일 구성

```
01-llm-api/
├── anthropic.sh          # Anthropic Claude API 호출 스크립트
└── openai.sh            # OpenAI GPT API 호출 스크립트
```

### 주요 파일 설명

**anthropic.sh**
```bash
#!/bin/bash

# Anthropic Claude API curl script
# Replace YOUR_API_KEY with your actual Anthropic API key

ANTHROPIC_API_KEY="sk-ant-..."
MODEL="claude-3-5-sonnet-20241022"

curl -X POST \
  https://api.anthropic.com/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "'$MODEL'",
    "max_tokens": 1024,
    "messages": [
      {
        "role": "user",
        "content": "hi"
      }
    ],
    "stream": true
  }' \
  --no-buffer
```

- Anthropic Claude API에 직접 HTTP POST 요청을 전송하는 Bash 스크립트
- `ANTHROPIC_API_KEY`와 `MODEL` 변수를 사용하여 API 키와 모델을 관리
- `claude-3-5-sonnet-20241022` 모델을 사용하여 메시지 생성
- `stream: true` 설정으로 실시간 응답 스트리밍 지원
- `--no-buffer` 옵션으로 즉시 출력 표시
- `x-api-key` 헤더와 `anthropic-version` 헤더를 통한 인증 및 API 버전 지정

**openai.sh**
```bash
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
  }' \
  --no-buffer
```

- OpenAI GPT API에 직접 HTTP POST 요청을 전송하는 Bash 스크립트
- `OPENAI_API_KEY`와 `MODEL` 변수를 사용하여 API 키와 모델을 관리
- `gpt-4` 모델을 사용하여 채팅 완성 기능 구현
- `stream: true` 설정으로 실시간 응답 스트리밍 지원
- `Authorization: Bearer` 헤더를 통한 API 키 인증 방식 사용
- `/v1/chat/completions` 엔드포인트를 통한 대화형 AI 상호작용

## 🚀 실행

### 사전 요구사항

**1. curl 설치**
대부분의 Linux/macOS 시스템에는 curl이 기본 설치되어 있습니다. Windows에서는 WSL이나 Git Bash를 사용하거나 curl을 별도 설치해야 합니다.

```bash
# Ubuntu/Debian
sudo apt-get install curl

# macOS (Homebrew)
brew install curl

# 설치 확인
curl --version
```

**2. API 키 획득 및 설정**

Anthropic API 키:
```bash
# https://console.anthropic.com 에서 API 키 획득
# anthropic.sh 파일의 ANTHROPIC_API_KEY 변수 수정
ANTHROPIC_API_KEY="sk-ant-your-actual-api-key-here"
```

OpenAI API 키:
```bash
# https://platform.openai.com/api-keys 에서 API 키 획득  
# openai.sh 파일의 OPENAI_API_KEY 변수 수정
OPENAI_API_KEY="sk-your-actual-openai-api-key-here"
```

**3. 실행 권한 부여**
```bash
chmod +x anthropic.sh
chmod +x openai.sh
```

### 실행 방법

**1. Anthropic Claude API 테스트**
```bash
./anthropic.sh
```

**2. OpenAI GPT API 테스트**
```bash
./openai.sh
```

**3. 메시지 내용 변경하여 테스트**
스크립트 파일을 편집하여 다른 메시지로 테스트할 수 있습니다:
```bash
# anthropic.sh 또는 openai.sh 파일 편집
"content": "안녕하세요. 간단한 Python 코드를 작성해주세요."
```

### 실행 결과

**Anthropic Claude API 실행 결과**
```bash
$ ./anthropic.sh
event: message_start
data: {"type":"message_start","message":{"id":"msg_01ABC123","type":"message","role":"assistant","model":"claude-3-5-sonnet-20241022","content":[],"stop_reason":null,"stop_sequence":null,"usage":{"input_tokens":8,"output_tokens":1}}}

event: content_block_start
data: {"type":"content_block_start","index":0,"content_block":{"type":"text","text":""}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"Hello"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"! How"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" can I"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" help"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" you"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" today"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"?"}}

event: content_block_stop
data: {"type":"content_block_stop","index":0}

event: message_delta
data: {"type":"message_delta","delta":{"stop_reason":"end_turn","stop_sequence":null},"usage":{"output_tokens":12}}

event: message_stop
data: {"type":"message_stop"}
```

**OpenAI GPT API 실행 결과**
```bash
$ ./openai.sh
data: {"id":"chatcmpl-ABC123","object":"chat.completion.chunk","created":1699876543,"model":"gpt-4-0613","choices":[{"index":0,"delta":{"role":"assistant","content":""},"finish_reason":null}]}

data: {"id":"chatcmpl-ABC123","object":"chat.completion.chunk","created":1699876543,"model":"gpt-4-0613","choices":[{"index":0,"delta":{"content":"Hello"},"finish_reason":null}]}

data: {"id":"chatcmpl-ABC123","object":"chat.completion.chunk","created":1699876543,"model":"gpt-4-0613","choices":[{"index":0,"delta":{"content":"!"},"finish_reason":null}]}

data: {"id":"chatcmpl-ABC123","object":"chat.completion.chunk","created":1699876543,"model":"gpt-4-0613","choices":[{"index":0,"delta":{"content":" How"},"finish_reason":null}]}

data: {"id":"chatcmpl-ABC123","object":"chat.completion.chunk","created":1699876543,"model":"gpt-4-0613","choices":[{"index":0,"delta":{"content":" can"},"finish_reason":null}]}

data: {"id":"chatcmpl-ABC123","object":"chat.completion.chunk","created":1699876543,"model":"gpt-4-0613","choices":[{"index":0,"delta":{"content":" I"},"finish_reason":null}]}

data: {"id":"chatcmpl-ABC123","object":"chat.completion.chunk","created":1699876543,"model":"gpt-4-0613","choices":[{"index":0,"delta":{"content":" assist"},"finish_reason":null}]}

data: {"id":"chatcmpl-ABC123","object":"chat.completion.chunk","created":1699876543,"model":"gpt-4-0613","choices":[{"index":0,"delta":{"content":" you"},"finish_reason":null}]}

data: {"id":"chatcmpl-ABC123","object":"chat.completion.chunk","created":1699876543,"model":"gpt-4-0613","choices":[{"index":0,"delta":{"content":" today"},"finish_reason":null}]}

data: {"id":"chatcmpl-ABC123","object":"chat.completion.chunk","created":1699876543,"model":"gpt-4-0613","choices":[{"index":0,"delta":{"content":"?"},"finish_reason":null}]}

data: {"id":"chatcmpl-ABC123","object":"chat.completion.chunk","created":1699876543,"model":"gpt-4-0613","choices":[{"index":0,"delta":{},"finish_reason":"stop"}]}

data: [DONE]
```

위 결과에서 확인할 수 있는 주요 특징들:

**1. 스트리밍 응답 처리**: 두 API 모두 `stream: true` 설정으로 실시간 텍스트 생성 과정을 보여줍니다. 각 단어나 구문이 생성되는 즉시 클라이언트로 전송되어 사용자 경험을 향상시킵니다.

**2. 응답 형식의 차이**: Anthropic은 Server-Sent Events(SSE) 형식의 `event:` 및 `data:` 구조를 사용하며, OpenAI는 단순한 `data:` 스트림 형식을 사용합니다.

**3. 메타데이터 정보**: 두 API 모두 메시지 ID, 모델 정보, 토큰 사용량 등의 유용한 메타데이터를 제공하여 API 사용량을 추적하고 최적화할 수 있습니다.

**4. 에러 처리**: API 키가 잘못되었거나 네트워크 오류가 발생하면 적절한 HTTP 상태 코드와 에러 메시지가 반환됩니다.

## 📚 정리

이 예제는 LLM API를 직접 호출하는 가장 기본적인 방법을 보여주며, MCP 학습의 출발점 역할을 합니다. curl을 사용한 순수한 HTTP 통신을 통해 Anthropic Claude와 OpenAI GPT API의 핵심 동작 원리를 이해할 수 있습니다. 특히 스트리밍 응답 처리 방식을 통해 실시간 텍스트 생성 과정을 직접 관찰할 수 있어, LLM의 작동 메커니즘에 대한 깊은 이해를 제공합니다. 두 API의 서로 다른 인증 방식(Anthropic의 x-api-key vs OpenAI의 Authorization Bearer)과 응답 형식의 차이점을 비교 분석함으로써, 다양한 LLM 서비스 제공업체의 API 설계 철학과 구현 방식을 학습할 수 있습니다. 이러한 기초적인 HTTP 통신 이해는 향후 MCP를 통한 고급 AI 도구 통합과 자동화된 워크플로우 구축에 필수적인 밑바탕이 됩니다.