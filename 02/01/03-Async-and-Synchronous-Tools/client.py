import asyncio
import time
from fastmcp import Client


async def sync_client_task(client_id: int):
    """
    동기 도구를 호출하는 클라이언트 작업
    """
    print(f"동기 클라이언트 {client_id}: 시작")
    start_time = time.time()
    
    async with Client("http://0.0.0.0:9000/mcp") as client:
        result = await client.call_tool("sync_tool")
        end_time = time.time()
        elapsed = end_time - start_time
        print(f"동기 클라이언트 {client_id}: 완료 - 소요시간: {elapsed:.2f}초")
        print(f"동기 클라이언트 {client_id}: 결과 - {result}")
        return result


async def async_client_task(client_id: int):
    """
    비동기 도구를 호출하는 클라이언트 작업
    """
    print(f"비동기 클라이언트 {client_id}: 시작")
    start_time = time.time()
    
    async with Client("http://0.0.0.0:9000/mcp") as client:
        result = await client.call_tool("async_tool")
        end_time = time.time()
        elapsed = end_time - start_time
        print(f"비동기 클라이언트 {client_id}: 완료 - 소요시간: {elapsed:.2f}초")
        print(f"비동기 클라이언트 {client_id}: 결과 - {result}")
        return result


async def main():
    """
    동기/비동기 도구 성능 비교 테스트
    """
    print("동기/비동기 도구 성능 비교 테스트를 시작합니다...\n")
    
    # 동기 도구 테스트
    print("=" * 50)
    print("동기 도구 테스트 시작")
    print("=" * 50)
    
    sync_start = time.time()
    sync_tasks = [sync_client_task(i+1) for i in range(3)]
    sync_results = await asyncio.gather(*sync_tasks)
    sync_end = time.time()
    sync_elapsed = sync_end - sync_start
    
    print(f"\n동기 도구 테스트 완료! 총 소요시간: {sync_elapsed:.2f}초")
    
    # 테스트 사이 대기
    print("\n" + "="*50)
    print("잠깐 대기 중...")
    print("="*50)
    await asyncio.sleep(2)
    
    # 비동기 도구 테스트
    print("=" * 50)
    print("비동기 도구 테스트 시작")
    print("=" * 50)
    
    async_start = time.time()
    async_tasks = [async_client_task(i+1) for i in range(3)]
    async_results = await asyncio.gather(*async_tasks)
    async_end = time.time()
    async_elapsed = async_end - async_start
    
    print(f"\n비동기 도구 테스트 완료! 총 소요시간: {async_elapsed:.2f}초")
    
    # 결과 요약
    print("\n" + "="*60)
    print("테스트 결과 요약")
    print("="*60)
    print(f"동기 도구 소요시간: {sync_elapsed:.2f}초")
    print(f"비동기 도구 소요시간: {async_elapsed:.2f}초")
    print(f"성능 차이: {abs(sync_elapsed - async_elapsed):.2f}초")
    print("테스트 완료!")


if __name__ == '__main__':
    asyncio.run(main())