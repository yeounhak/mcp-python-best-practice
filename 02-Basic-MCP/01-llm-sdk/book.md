## 📋 개요

이 프로젝트는 Anthropic Claude와 OpenAI GPT 모델을 사용한 비동기 스트리밍 API 호출의 기본 구현을 보여줍니다. 두 가지 주요 LLM(Large Language Model) 제공업체의 API를 활용하여 실시간 텍스트 생성을 수행하는 방법을 다루며, 각각의 클라이언트 라이브러리를 사용한 비동기 프로그래밍 패턴을 학습할 수 있습니다.

주요 기술 스택으로는 Python의 `asyncio`를 기반으로 한 비동기 처리, Anthropic의 `anthropic` 패키지와 OpenAI의 `openai` 패키지를 활용한 API 통신, 그리고 스트리밍 응답 처리를 위한 비동기 이터레이터 패턴이 포함됩니다.

> 🔗 **상세 코드 및 예제**: [https://github.com/yeounhak/mcp-python-best-practice/02/01/01-llm-api][github-repo]

[github-repo]: https://github.com/yeounhak/mcp-python-best-practice/02/01/01-llm-api

## 📁 파일 구성

```
01-llm-api/
├── anthropic.py       # Anthropic Claude API 비동기 스트리밍 클라이언트
└── openai.py          # OpenAI GPT API 비동기 스트리밍 클라이언트
```

### 주요 파일 설명

**anthropic.py**
```python
from anthropic import AsyncAnthropic

client = AsyncAnthropic(
    api_key="sk-ant-..."
)

async def main():
    stream = await client.messages.create(
        model="claude-3-5-sonnet-20241022",
        messages=[{"role": "user", "content": "hi"}],
        max_tokens=1024,
        stream=True
    )
    async for chunk in stream:
        print(chunk)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```
- `AsyncAnthropic` 클라이언트를 사용하여 Claude API에 비동기 연결
- `messages.create()` 메서드로 Claude 3.5 Sonnet 모델과 대화 세션 생성
- `stream=True` 옵션으로 실시간 텍스트 스트리밍 활성화
- `async for` 구문을 사용하여 스트리밍 청크를 순차적으로 처리

**openai.py**
```python
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
- `AsyncOpenAI` 클라이언트를 사용하여 OpenAI API에 비동기 연결
- `chat.completions.create()` 메서드로 GPT-5 모델과 채팅 완성 요청 생성
- `stream=True` 설정으로 토큰별 실시간 응답 스트리밍 구현
- 비동기 이터레이터를 통한 청크 단위 응답 처리

## 🚀 실행

### 사전 요구사항

**1. Python 패키지 설치**
```bash
pip install anthropic openai
```

**2. API 키 설정**
- **Anthropic API 키**: [Anthropic Console](https://console.anthropic.com/)에서 API 키 발급
- **OpenAI API 키**: [OpenAI Platform](https://platform.openai.com/)에서 API 키 발급

**3. API 키 환경변수 설정 (선택사항)**
```bash
# Anthropic
export ANTHROPIC_API_KEY="your-anthropic-api-key"

# OpenAI  
export OPENAI_API_KEY="your-openai-api-key"
```

### 실행 방법

**1. Anthropic Claude API 실행**
```bash
python anthropic.py
```

**2. OpenAI GPT API 실행**
```bash
python openai.py
```

### 실행 결과

**Anthropic Claude 실행 결과:**
```bash
$ python anthropic.py
RawMessageStartEvent(type='message_start', message=RawMessage(id='msg_01...', type='message', role='assistant', model='claude-3-5-sonnet-20241022', content=[], max_tokens=1024, stop_reason=None, stop_sequence=None, usage=Usage(input_tokens=8, output_tokens=1)))
RawContentBlockStartEvent(type='content_block_start', index=0, content_block=RawTextBlock(type='text', text=''))
RawContentBlockDeltaEvent(type='content_block_delta', index=0, delta=RawTextDelta(type='text_delta', text='Hello'))
RawContentBlockDeltaEvent(type='content_block_delta', index=0, delta=RawTextDelta(type='text_delta', text='!'))
RawMessageDeltaEvent(type='message_delta', delta=RawMessageDelta(stop_reason='end_turn', stop_sequence=None), usage=RawMessageDeltaUsage(output_tokens=2))
RawMessageStopEvent(type='message_stop')
```

위 출력에서 확인할 수 있는 주요 이벤트들:
- **message_start**: 메시지 생성 시작 및 토큰 사용량 정보
- **content_block_start**: 콘텐츠 블록 시작 
- **content_block_delta**: 실제 텍스트 청크 ("Hello", "!")
- **message_delta**: 메시지 완료 및 중단 이유
- **message_stop**: 스트리밍 종료

**OpenAI GPT 실행 결과:**
```bash
$ python openai.py
ChatCompletionChunk(id='chatcmpl-...', choices=[Choice(delta=ChoiceDelta(content='', function_call=None, role='assistant', tool_calls=None), finish_reason=None, index=0, logprobs=None)], created=1640995200, model='gpt-5', object='chat.completion.chunk', system_fingerprint=None, usage=None)
ChatCompletionChunk(id='chatcmpl-...', choices=[Choice(delta=ChoiceDelta(content='Hello', function_call=None, role=None, tool_calls=None), finish_reason=None, index=0, logprobs=None)], created=1640995200, model='gpt-5', object='chat.completion.chunk', system_fingerprint=None, usage=None)
ChatCompletionChunk(id='chatcmpl-...', choices=[Choice(delta=ChoiceDelta(content='!', function_call=None, role=None, tool_calls=None), finish_reason=None, index=0, logprobs=None)], created=1640995200, model='gpt-5', object='chat.completion.chunk', system_fingerprint=None, usage=None)
ChatCompletionChunk(id='chatcmpl-...', choices=[Choice(delta=ChoiceDelta(content=None, function_call=None, role=None, tool_calls=None), finish_reason='stop', index=0, logprobs=None)], created=1640995200, model='gpt-5', object='chat.completion.chunk', system_fingerprint=None, usage=CompletionUsage(completion_tokens=2, prompt_tokens=8, total_tokens=10))
```

OpenAI 응답에서 주목할 점들:
- **ChatCompletionChunk**: 각 청크는 완전한 응답 객체 구조를 가짐
- **delta.content**: 실제 생성된 텍스트 부분 ("Hello", "!")
- **finish_reason**: 응답 완료 이유 ('stop')
- **usage**: 최종 청크에서 토큰 사용량 정보 제공

## 📚 정리

이 예제는 두 가지 주요 LLM 제공업체인 Anthropic과 OpenAI의 비동기 스트리밍 API를 활용하는 기본적인 방법을 보여줍니다. Python의 `asyncio`를 기반으로 한 비동기 프로그래밍 패턴을 통해 실시간으로 텍스트를 생성하고 처리하는 과정을 학습할 수 있었습니다. Anthropic의 경우 이벤트 기반 스트리밍을 통해 메시지 시작부터 종료까지의 세부적인 상태를 추적할 수 있으며, OpenAI는 청크 단위로 구조화된 응답을 제공하여 각각의 장단점을 이해할 수 있습니다. 두 API 모두 `stream=True` 옵션과 `async for` 구문을 통해 일관된 비동기 스트리밍 패턴을 사용하므로, 실제 애플리케이션에서 사용자 경험을 향상시키는 실시간 응답 시스템을 구축하는 기초를 마련할 수 있습니다.