## 📋 개요

이 프로젝트는 FastMCP(Fast Model Context Protocol) 라이브러리를 활용하여 **리소스(Resources) 기능**을 구현한 예제입니다. MCP 서버에서 다양한 형태의 데이터 리소스를 제공하고, 클라이언트가 이를 조회하고 읽어오는 기본적인 패턴을 학습할 수 있습니다. 

서버는 문자열과 JSON 형태의 두 가지 리소스를 제공하며, 클라이언트는 HTTP 연결을 통해 서버에 접속하여 사용 가능한 모든 리소스를 나열하고 각각의 내용을 읽어옵니다. FastMCP의 `@mcp.resource` 데코레이터를 사용하여 함수를 리소스로 등록하는 방법과, 클라이언트에서 `list_resources()`와 `read_resource()` 메서드를 활용하는 방법을 다룹니다.

> 🔗 **상세 코드 및 예제**: [https://github.com/yeounhak/mcp-python-best-practice/03-Server-Features/3-Resources][github-repo]

[github-repo]: https://github.com/yeounhak/mcp-python-best-practice/03-Server-Features/3-Resources

## 🔍 리소스와 템플릿 이해하기

### 리소스(Resources)란?

리소스는 **MCP 서버가 LLM/클라이언트 애플리케이션에게 읽기 전용 데이터 접근을 제공하는 메커니즘**입니다. 도구(Tools)가 특정 작업을 실행하는 것과 달리, 리소스는 서버에 저장된 정보나 동적으로 생성된 데이터를 조회할 수 있게 해줍니다.

### @resource 데코레이터

**가장 일반적인 리소스 정의 방법**으로, 함수를 MCP 리소스로 변환합니다:

```python
@mcp.resource("resource://greeting")
def get_greeting() -> str:
    """간단한 인사 메시지를 제공합니다."""
    return "Hello from FastMCP Resources!"
```

### 핵심 개념

**1. URI (Uniform Resource Identifier)**
- `@resource`의 첫 번째 인수는 고유한 URI입니다 (예: `"resource://greeting"`)
- 클라이언트가 리소스에 접근할 때 사용하는 식별자
- 일관된 명명 규칙을 통해 리소스 구조를 체계화

**2. 지연 로딩 (Lazy Loading)**
- 리소스 함수는 클라이언트가 `resources/read`를 통해 실제 요청할 때만 실행됩니다
- 서버 시작 시점이 아닌 필요 시점에 데이터를 생성하여 성능 최적화
- 동적 데이터나 비용이 큰 연산에 특히 유용

**3. 메타데이터 자동 추론**
- 리소스 이름: 함수명에서 자동으로 생성 (`get_greeting` → `greeting`)
- 리소스 설명: 함수의 독스트링(docstring)에서 자동으로 추출
- 별도 설정 없이도 클라이언트에서 리소스 정보를 확인할 수 있음


## 📁 파일 구성

```
3-Resources/
├── server.py          # MCP 서버 구현 (리소스 제공)
└── client.py          # 리소스를 조회하는 클라이언트
```

### 주요 파일 설명

**server.py**

**1. 라이브러리 임포트 및 서버 초기화**
```python
from fastmcp import FastMCP

mcp = FastMCP(name="DataServer")
```
- FastMCP 라이브러리를 임포트하고 "DataServer"라는 이름의 MCP 서버 인스턴스 생성

**2. 문자열 리소스 제공**
```python
@mcp.resource("resource://greeting")
def get_greeting() -> str:
    """간단한 인사 메시지를 제공합니다."""
    return "Hello from FastMCP Resources!"
```
- `@mcp.resource` 데코레이터를 사용하여 함수를 리소스로 등록
- URI `resource://greeting`으로 접근 가능한 문자열 리소스
- **지연 로딩 적용**: 클라이언트가 실제로 요청할 때까지 함수가 실행되지 않음
- **메타데이터 자동 추론**: 함수명 `get_greeting`에서 리소스 이름 `greeting` 자동 생성
- 독스트링이 리소스 설명으로 자동 설정됨

**3. JSON 데이터 리소스 제공**
```python
@mcp.resource("data://config")
def get_config() -> dict:
    """JSON 형태의 애플리케이션 설정을 제공합니다."""
    return {
        "theme": "dark",
        "version": "1.2.0",
        "features": ["tools", "resources"],
    }
```
- **자동 JSON 직렬화**: 딕셔너리 형태의 데이터를 반환하면 자동으로 JSON으로 변환
- URI `data://config`으로 접근 가능한 설정 데이터
- **복합 데이터 타입 지원**: 문자열, 숫자, 리스트가 포함된 복잡한 구조도 처리 가능
- 애플리케이션의 테마, 버전, 기능 목록 등을 포함한 구성 정보
- 설정 파일이나 환경 변수를 동적으로 읽어와 제공하는 패턴에 활용 가능

**4. 서버 실행**
```python
mcp.run(
    transport="http",
    host="0.0.0.0",
    port=9000,
)
```
- HTTP 프로토콜을 통해 모든 인터페이스(0.0.0.0)의 9000번 포트에서 서버 시작

**client.py**

**1. 라이브러리 임포트 및 메인 함수**
```python
from fastmcp import Client

async def main():
    async with Client("http://0.0.0.0:9000/mcp") as client:
```
- FastMCP Client 클래스를 임포트
- `async with` 문을 사용하여 서버와의 연결을 안전하게 관리
- HTTP 프로토콜로 서버의 `/mcp` 엔드포인트에 연결

**2. 리소스 목록 조회 및 출력**
```python
resources = await client.list_resources()
print(f"✅ {len(resources)}개의 리소스를 찾았습니다.\n")
```
- `list_resources()` 메서드로 서버에서 제공하는 모든 리소스 목록 조회
- 찾은 리소스의 개수를 사용자에게 표시

**3. 각 리소스 내용 읽기**
```python
for i, resource in enumerate(resources, 1):
    print(f"\n📄 [{i}] Resource URI: {resource}")
    
    content = await client.read_resource(resource.uri)
    print(f"📝 Content: {content}")
```
- 각 리소스를 순회하면서 URI를 출력
- `read_resource()` 메서드로 개별 리소스의 실제 내용을 읽어옴
- 리소스 번호, URI, 내용을 체계적으로 표시

**4. 프로그램 실행**
```python
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```
- 스크립트가 직접 실행될 때 asyncio를 통해 메인 함수 실행

## 🚀 실행

### 사전 요구사항

1. **Python 패키지 설치**
```bash
pip install fastmcp
```

2. **Python 3.7 이상**
- async/await 문법과 asyncio 라이브러리 지원을 위해 필요

### 실행 방법

1. **MCP 서버 시작**
```bash
python server.py
```

2. **새 터미널에서 클라이언트 실행**
```bash
python client.py
```

### 실행 결과

서버를 먼저 실행하면 다음과 같은 출력이 나타납니다:

```bash
FastMCP server starting on http://0.0.0.0:9000
Server ready to accept connections...
```

이후 클라이언트를 실행하면 다음과 같은 결과를 확인할 수 있습니다:

```bash
✅ 2개의 리소스를 찾았습니다.

📄 [1] Resource URI: resource://greeting
📝 Content: Hello from FastMCP Resources!

📄 [2] Resource URI: data://config
📝 Content: {'theme': 'dark', 'version': '1.2.0', 'features': ['tools', 'resources']}
```

위 결과에서 확인할 수 있는 핵심 개념들:

- **리소스 발견**: 서버에서 제공하는 2개의 리소스가 `list_resources()`를 통해 성공적으로 발견됨
- **URI 기반 접근**: 각 리소스가 고유한 URI(`resource://greeting`, `data://config`)로 식별됨
- **지연 로딩 실증**: `read_resource()` 호출 시점에 서버의 리소스 함수가 실행되어 데이터 생성
- **다양한 데이터 타입 지원**: 
  - 문자열 리소스: `resource://greeting`에서 단순 텍스트 반환
  - JSON 리소스: `data://config`에서 복합 구조 데이터 반환
- **자동 직렬화**: 서버의 딕셔너리가 클라이언트에서 자동으로 적절한 형태로 변환
- **메타데이터 활용**: 클라이언트가 리소스의 URI와 내용을 모두 확인할 수 있어 동적 탐색 가능

## 📚 정리

이 예제는 FastMCP의 리소스(Resources) 기능을 통해 서버가 LLM/클라이언트 애플리케이션에게 읽기 전용 데이터 접근을 제공하는 핵심 메커니즘을 보여줍니다. `@mcp.resource` 데코레이터를 사용하여 일반 Python 함수를 MCP 리소스로 변환하는 과정에서 URI 기반 식별, 지연 로딩, 메타데이터 자동 추론 등의 핵심 개념들을 실제로 구현했습니다. 특히 지연 로딩을 통해 클라이언트가 실제로 요청할 때만 리소스 함수가 실행되어 성능을 최적화하고, 함수명과 독스트링에서 자동으로 추론되는 메타데이터가 클라이언트의 동적 탐색을 지원하는 것을 확인할 수 있습니다. 텍스트와 JSON 데이터 타입을 통해 단순한 문자열부터 복잡한 구조화된 데이터까지 자연스럽게 처리할 수 있으며, 향후 리소스 템플릿을 활용하면 URI 매개변수를 통한 동적 콘텐츠 생성도 가능합니다. 이러한 리소스 패턴은 설정 관리, 데이터베이스 쿼리, 실시간 모니터링, API 프록시 등 다양한 시나리오에서 MCP 서버가 구조화된 정보를 제공하는 핵심 메커니즘으로 활용됩니다. HTTP 기반의 안전한 원격 접근을 통해 분산 시스템과 마이크로서비스 아키텍처에서도 일관된 데이터 접근 인터페이스를 제공할 수 있습니다.