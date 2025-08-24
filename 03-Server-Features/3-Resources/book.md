## 📋 개요

이 프로젝트는 **Model Context Protocol(MCP) 리소스 기능**의 구현 예제입니다. FastMCP 라이브러리를 사용하여 MCP 서버에서 **동적 리소스**를 제공하고, 클라이언트에서 이를 조회하고 읽는 방법을 보여줍니다.

MCP 리소스는 서버가 클라이언트에게 데이터나 콘텐츠를 제공할 수 있는 메커니즘입니다. 이 예제에서는 문자열과 JSON 형태의 두 가지 리소스 타입을 구현하여, 각각 간단한 인사 메시지와 애플리케이션 설정 정보를 제공합니다.

주요 기술 스택:
- **FastMCP**: MCP 서버/클라이언트 구현을 위한 Python 라이브러리
- **HTTP 전송**: 서버와 클라이언트 간 통신 프로토콜
- **비동기 프로그래밍**: `async/await` 패턴 활용

> 🔗 **상세 코드 및 예제**: [https://github.com/yeounhak/mcp-python-best-practice/03-Server-Features/3-Resources][github-repo]

[github-repo]: https://github.com/yeounhak/mcp-python-best-practice/03-Server-Features/3-Resources

## 📁 파일 구성

```
3-Resources/
├── server.py          # MCP 리소스 서버 구현
└── client.py          # 리소스 조회 클라이언트
```

### 주요 파일 설명

**server.py**
```python
from fastmcp import FastMCP
mcp = FastMCP(name="DataServer")

# 문자열을 반환하는 기본 동적 리소스
@mcp.resource("resource://greeting")
def get_greeting() -> str:
    """간단한 인사 메시지를 제공합니다."""
    return "Hello from FastMCP Resources!"

# JSON 데이터를 반환하는 리소스 (dict는 자동으로 직렬화됨)
@mcp.resource("data://config")
def get_config() -> dict:
    """JSON 형태의 애플리케이션 설정을 제공합니다."""
    return {
        "theme": "dark",
        "version": "1.2.0",
        "features": ["tools", "resources"],
    }

mcp.run(
    transport="http",
    host="0.0.0.0",
    port=9000,
)
```
- `DataServer` 이름으로 MCP 서버 생성
- `@mcp.resource` 데코레이터로 함수를 MCP 리소스로 등록
- `resource://greeting`: 간단한 문자열 인사 메시지 제공
- `data://config`: JSON 형태의 애플리케이션 설정 정보 제공
- HTTP 전송 방식으로 0.0.0.0:9000 포트에서 서버 실행

**client.py**
```python
from fastmcp import Client

async def main():
    # MCP 서버에 연결
    async with Client("http://0.0.0.0:9000/mcp") as client:
        resources = await client.list_resources()
        print(f"✅ {len(resources)}개의 리소스를 찾았습니다.\n")
        
        # 각 리소스의 내용을 읽어서 출력
        for i, resource in enumerate(resources, 1):
            print(f"\n📄 [{i}] Resource URI: {resource}")
            
            content = await client.read_resource(resource.uri)
            print(f"📝 Content: {content}")

        
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```
- FastMCP Client를 사용하여 HTTP MCP 서버에 연결
- `list_resources()`로 서버에서 제공하는 모든 리소스 목록 조회
- 각 리소스를 순회하며 URI 정보 출력
- `read_resource()`로 개별 리소스의 내용을 읽어와서 화면에 표시
- `asyncio.run()`으로 비동기 메인 함수 실행

## 🚀 실행

### 사전 요구사항

1. **Python 패키지 설치**
```bash
pip install fastmcp
```

2. **Python 3.8 이상** 버전 필요 (async/await 지원)

### 실행 방법

1. **MCP 서버 실행**
```bash
python server.py
```
서버가 시작되면 `http://0.0.0.0:9000`에서 MCP 서비스 제공

2. **클라이언트 실행 (새 터미널)**
```bash
python client.py
```

### 실행 결과

**1. 서버 실행 시**
```bash
$ python server.py
FastMCP server running on http://0.0.0.0:9000
```

**2. 클라이언트 실행 시**
```bash
$ python client.py
✅ 2개의 리소스를 찾았습니다.

📄 [1] Resource URI: resource://greeting
📝 Content: Hello from FastMCP Resources!

📄 [2] Resource URI: data://config
📝 Content: {'theme': 'dark', 'version': '1.2.0', 'features': ['tools', 'resources']}
```

위 실행 결과에서 확인할 수 있는 주요 내용:
- 서버에서 제공하는 2개의 리소스가 성공적으로 조회됨
- `resource://greeting`: 문자열 형태의 인사 메시지
- `data://config`: 딕셔너리 형태의 JSON 설정 데이터
- 각 리소스의 URI와 내용이 명확하게 구분되어 출력됨

## 📚 정리

이 예제는 Model Context Protocol(MCP)의 리소스 기능을 활용하여 서버-클라이언트 간 데이터 제공 메커니즘을 구현한 사례입니다. FastMCP 라이브러리의 `@mcp.resource` 데코레이터를 사용하면 일반 Python 함수를 MCP 리소스로 간단하게 등록할 수 있으며, 문자열과 딕셔너리 등 다양한 데이터 타입을 자동으로 직렬화하여 제공합니다. 클라이언트 측에서는 `list_resources()`로 사용 가능한 리소스를 탐색하고 `read_resource()`로 개별 리소스 내용을 읽어올 수 있어, MCP 생태계에서 구조화된 데이터 교환이 가능함을 보여줍니다. 이러한 리소스 패턴은 설정 정보, 문서, 메타데이터 등을 LLM이나 다른 클라이언트에게 체계적으로 제공하는 데 매우 유용합니다.