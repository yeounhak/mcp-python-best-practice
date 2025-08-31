<div align="center" style="background:#fffbe6; border-radius:20px; box-shadow:0 4px 16px #eee; padding:40px 20px; margin:40px 0;">
  <span style="font-size:1.5em;">🧪</span>
  <div style="margin:10px 0 10px 0;">
    <span style="font-size:1.3em; font-weight:bold; color:#222;">
      FastMCP의 오류 마스킹 동작을 A/B 테스트로 실제 검증하여 </br>
      6가지 시나리오별 오류 메시지 가시성 패턴을 체계적으로 학습할 수 있습니다.
    </span>
  </div>
</div>

## 📋 개요

이 프로젝트는 FastMCP의 `mask_error_details` 설정이 실제로 어떤 오류 메시지를 마스킹하고 어떤 메시지는 그대로 노출하는지를 A/B 테스트 방식으로 체계적으로 검증합니다. 동일한 3가지 오류 유형을 마스킹 서버와 비마스킹 서버에서 각각 테스트하여 총 6가지 시나리오의 실제 결과를 비교 분석할 수 있습니다.

### 핵심 테스트 결과

실제 A/B 테스트를 통해 확인된 오류 처리 패턴:

| 오류 유형 | 마스킹 서버 결과 | 비마스킹 서버 결과 | 차이점 |
|----------|---------------|-----------------|-------|
| **ToolError** | `ToolError message from MASKED server` | `ToolError message from UNMASKED server` | ❌ **동일** |
| **Standard Exception** | `Error calling tool 'test_standard_exception_masked'` | `Standard exception from UNMASKED server - should be visible!` | ✅ **다름** |
| **Input Validation** | `Input validation error: 'invalid' is not of type 'integer'` | `Input validation error: 'invalid' is not of type 'integer'` | ❌ **동일** |

주요 학습 내용으로는 `ToolError`는 마스킹 설정과 무관하게 항상 동일한 메시지를 표시하며, 표준 예외(`ValueError`, `FileNotFoundError` 등)만 마스킹 적용으로 "Error calling tool" 형태로 숨겨지고, 입력 검증 오류는 마스킹 설정과 무관하게 항상 구체적인 타입 안내 메시지를 제공하며, 실제 운영 환경에서 보안과 디버깅 효율성 간의 균형점을 찾는 전략을 다룹니다.

> 🔗 **상세 코드 및 예제**: [https://github.com/yeounhak/mcp-python-best-practice/03-Server-Features/1-Tools/Error-Handling][github-repo]

[github-repo]: https://github.com/yeounhak/mcp-python-best-practice/03-Server-Features/1-Tools/Error-Handling

## 📁 파일 구성

```
Error-Handling/
├── server.py          # 마스킹/비마스킹 서버를 선택적으로 실행하는 A/B 테스트 서버
└── client.py          # 6가지 시나리오를 체계적으로 테스트하는 비교 분석 클라이언트
```

### 주요 파일 설명

**server.py**

```python
# Error-Handling/server.py 파일입니다.
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

# ===============================
# MASKED SERVER (mask_error_details=True)
# ===============================
mcp_masked = FastMCP(name="MaskedServer", mask_error_details=True)

@mcp_masked.tool
def test_toolerror_masked() -> str:
    """Test ToolError with masking enabled."""
    raise ToolError("ToolError message from MASKED server")

@mcp_masked.tool
def test_standard_exception_masked() -> str:
    """Test standard exception with masking enabled."""
    raise ValueError("Standard exception from MASKED server - should be hidden!")

@mcp_masked.tool  
def test_input_validation_masked(number: int) -> str:
    """Test input validation with masking enabled."""
    return f"Valid number received by MASKED server: {number}"

# ===============================
# UNMASKED SERVER (mask_error_details=False)
# ===============================
mcp_unmasked = FastMCP(name="UnmaskedServer", mask_error_details=False)

@mcp_unmasked.tool
def test_toolerror_unmasked() -> str:
    """Test ToolError with masking disabled."""
    raise ToolError("ToolError message from UNMASKED server")

@mcp_unmasked.tool
def test_standard_exception_unmasked() -> str:
    """Test standard exception with masking disabled."""
    raise ValueError("Standard exception from UNMASKED server - should be visible!")

@mcp_unmasked.tool  
def test_input_validation_unmasked(number: int) -> str:
    """Test input validation with masking disabled."""
    return f"Valid number received by UNMASKED server: {number}"

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "unmasked":
        print("🔓 Starting UNMASKED server on port 8001...")
        mcp_unmasked.run(transport='http', port=8001)
    else:
        print("🔒 Starting MASKED server on port 8000...")
        mcp_masked.run(transport='http', port=8000)
```

- A/B 테스트를 위한 두 개의 독립적인 FastMCP 인스턴스 구현
- `mcp_masked`: `mask_error_details=True`로 설정된 마스킹 서버 (포트 8000)
- `mcp_unmasked`: `mask_error_details=False`로 설정된 비마스킹 서버 (포트 8001)
- 각 서버마다 동일한 3가지 오류 시나리오를 테스트할 수 있는 도구 함수들 제공
- 명령행 인자로 실행할 서버 유형을 선택하는 유연한 구조

**client.py**

```python
# Error-Handling/client.py 파일입니다.
from fastmcp import Client
import asyncio

async def test_error_type(error_type: str, masked_client: Client, unmasked_client: Client):
    """Test a specific error type on both masked and unmasked servers."""
    
    print(f"\n{'='*60}")
    print(f"🧪 Testing {error_type}")
    print(f"{'='*60}")
    
    # Test on masked server
    print(f"\n🔒 MASKED Server (mask_error_details=True):")
    print("-" * 50)
    try:
        if error_type == "ToolError":
            await masked_client.call_tool("test_toolerror_masked")
        elif error_type == "Standard Exception":
            await masked_client.call_tool("test_standard_exception_masked")
        elif error_type == "Input Validation":
            await masked_client.call_tool("test_input_validation_masked", {"number": "invalid"})
    except Exception as e:
        print(f"❌ MASKED: {e}")
    
    # Test on unmasked server
    print(f"\n🔓 UNMASKED Server (mask_error_details=False):")
    print("-" * 50)
    try:
        if error_type == "ToolError":
            await unmasked_client.call_tool("test_toolerror_unmasked")
        elif error_type == "Standard Exception":
            await unmasked_client.call_tool("test_standard_exception_unmasked")
        elif error_type == "Input Validation":
            await unmasked_client.call_tool("test_input_validation_unmasked", {"number": "invalid"})
    except Exception as e:
        print(f"❌ UNMASKED: {e}")

async def compare_all_error_patterns():
    """Compare all 3 error patterns across masked vs unmasked servers."""
    
    print("🛡️ FastMCP Error Handling: Masked vs Unmasked Comparison")
    print("=" * 60)
    print("Testing 6 scenarios: 3 error types × 2 masking modes")
    
    # Connect to both servers
    try:
        async with Client("http://localhost:8000/mcp") as masked_client:
            try:
                async with Client("http://localhost:8001/mcp") as unmasked_client:
                    
                    # Test 1: ToolError on both servers
                    await test_error_type("ToolError", masked_client, unmasked_client)
                    
                    # Test 2: Standard Exception on both servers  
                    await test_error_type("Standard Exception", masked_client, unmasked_client)
                    
                    # Test 3: Input Validation on both servers
                    await test_error_type("Input Validation", masked_client, unmasked_client)
                    
                    # Summary
                    print(f"\n{'='*60}")
                    print("📊 COMPARISON SUMMARY")
                    print(f"{'='*60}")
                    print("1️⃣ ToolError: Should be IDENTICAL on both servers")
                    print("2️⃣ Standard Exception: Should be DIFFERENT (masked vs detailed)")  
                    print("3️⃣ Input Validation: Should be IDENTICAL on both servers")
                    print(f"{'='*60}")
                    
            except Exception as e:
                print(f"\n❌ Cannot connect to UNMASKED server (port 8001): {e}")
                print("💡 Start unmasked server with: python server.py unmasked")
                
    except Exception as e:
        print(f"\n❌ Cannot connect to MASKED server (port 8000): {e}")
        print("💡 Start masked server with: python server.py")

async def main():
    """Main function for comprehensive error handling comparison."""
    await compare_all_error_patterns()

if __name__ == '__main__':
    asyncio.run(main())
```

- `test_error_type()`: 특정 오류 유형을 마스킹/비마스킹 서버에서 동시에 테스트하는 핵심 함수
- 6가지 시나리오를 체계적으로 실행하여 실제 차이점을 시각적으로 비교
- 각 테스트마다 마스킹 서버와 비마스킹 서버의 결과를 나란히 표시
- 연결 오류 시 적절한 서버 실행 가이드 제공

## 🚀 실행

### 사전 요구사항

**1. Python 패키지 설치**
```bash
pip install fastmcp
```

### 실행 방법

**1. 마스킹 서버 실행**
```bash
# 터미널 1에서 마스킹 서버 실행 (포트 8000)
python server.py
```

**2. 비마스킹 서버 실행**
```bash  
# 터미널 2에서 비마스킹 서버 실행 (포트 8001)
python server.py unmasked
```

**3. A/B 테스트 클라이언트 실행**
```bash
# 터미널 3에서 비교 테스트 실행
python client.py
```

### 실행 결과

A/B 테스트 클라이언트를 실행하면 6가지 시나리오의 실제 결과를 직접 비교할 수 있습니다:

```bash
🛡️ FastMCP Error Handling: Masked vs Unmasked Comparison
============================================================
Testing 6 scenarios: 3 error types × 2 masking modes

============================================================
🧪 Testing ToolError
============================================================

🔒 MASKED Server (mask_error_details=True):
--------------------------------------------------
❌ MASKED: ToolError message from MASKED server

🔓 UNMASKED Server (mask_error_details=False):
--------------------------------------------------
❌ UNMASKED: ToolError message from UNMASKED server

============================================================
🧪 Testing Standard Exception
============================================================

🔒 MASKED Server (mask_error_details=True):
--------------------------------------------------
❌ MASKED: Error calling tool 'test_standard_exception_masked'

🔓 UNMASKED Server (mask_error_details=False):
--------------------------------------------------
❌ UNMASKED: Standard exception from UNMASKED server - should be visible!

============================================================
🧪 Testing Input Validation
============================================================

🔒 MASKED Server (mask_error_details=True):
--------------------------------------------------
❌ MASKED: Input validation error: 'invalid' is not of type 'integer'

🔓 UNMASKED Server (mask_error_details=False):
--------------------------------------------------
❌ UNMASKED: Input validation error: 'invalid' is not of type 'integer'

============================================================
📊 COMPARISON SUMMARY
============================================================
1️⃣ ToolError: Should be IDENTICAL on both servers
2️⃣ Standard Exception: Should be DIFFERENT (masked vs detailed)  
3️⃣ Input Validation: Should be IDENTICAL on both servers
============================================================
```

### 실제 검증된 오류 마스킹 패턴

위 A/B 테스트 결과를 통해 FastMCP의 오류 마스킹 동작을 명확히 확인할 수 있습니다:

**1. ToolError 패턴 (마스킹 무관)**: 두 서버 모두에서 `ToolError message from [SERVER_TYPE] server` 형태로 동일하게 표시됩니다. `mask_error_details` 설정과 무관하게 항상 명확한 메시지가 클라이언트에 전달되어 사용자가 이해해야 하는 비즈니스 로직 오류를 적절히 안내합니다.

**2. 표준 예외 패턴 (마스킹 적용)**: 가장 큰 차이를 보이는 패턴입니다. 마스킹 서버에서는 `Error calling tool 'test_standard_exception_masked'` 형태의 일반적인 메시지로 변환되어 내부 구현 세부사항을 숨기는 반면, 비마스킹 서버에서는 `Standard exception from UNMASKED server - should be visible!` 형태로 원본 예외 메시지가 그대로 노출됩니다.

**3. 입력 검증 패턴 (마스킹 무관)**: 두 서버 모두에서 `Input validation error: 'invalid' is not of type 'integer'` 형태로 동일하게 표시됩니다. 이는 API 사용법 안내를 위한 도움말 역할로서 마스킹 설정과 무관하게 항상 구체적인 타입 안내를 제공합니다.

**4. 보안 vs 디버깅 트레이드오프**: 마스킹 서버는 표준 예외에서만 내부 정보를 보호하면서도 `ToolError`와 입력 검증을 통해 필수적인 사용성은 유지합니다. 비마스킹 서버는 모든 오류 세부사항을 노출하여 개발 단계에서 디버깅 효율성을 높입니다.

## 📚 정리

이 A/B 테스트 예제는 FastMCP의 `mask_error_details` 설정이 실제로 어떤 오류 메시지를 마스킹하고 어떤 메시지는 그대로 노출하는지를 체계적으로 검증합니다. 두 개의 독립적인 서버 인스턴스(`mcp_masked`, `mcp_unmasked`)를 통해 동일한 오류 시나리오를 서로 다른 마스킹 설정에서 테스트하여 실제 차이점을 명확히 확인할 수 있습니다. 핵심 발견사항으로는 `ToolError`와 입력 검증 오류는 마스킹 설정과 무관하게 항상 동일한 메시지를 표시하여 사용자 경험을 보장하는 반면, 표준 예외(`ValueError`, `FileNotFoundError` 등)만 마스킹 적용 시 "Error calling tool" 형태로 숨겨져서 시스템 내부 정보를 보호한다는 점입니다. 클라이언트의 `test_error_type()` 함수는 각 오류 유형을 두 서버에서 동시에 테스트하여 차이점을 나란히 비교할 수 있게 하며, 이를 통해 개발자는 운영 환경에서 보안성과 디버깅 효율성 간의 적절한 균형점을 찾을 수 있습니다. 이러한 실증적 접근 방식은 FastMCP의 오류 처리 메커니즘을 이론이 아닌 실제 동작으로 이해할 수 있게 하여 더욱 효과적인 오류 처리 전략 수립에 도움을 줍니다.