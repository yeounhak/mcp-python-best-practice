import asyncio
import time
from fastmcp import Client


async def open_resource_client_task(client_id: int):
    """
    open() 기반 리소스를 호출하는 클라이언트 작업
    """
    print(f"open() 클라이언트 {client_id}: 시작")
    start_time = time.time()
    
    async with Client("http://0.0.0.0:9000/mcp") as client:
        result = await client.read_resource("file://log-sync.txt")
        end_time = time.time()
        elapsed = end_time - start_time
        print(f"open() 클라이언트 {client_id}: 완료 - 소요시간: {elapsed:.2f}초")
        print(f"open() 클라이언트 {client_id}: 결과 길이 - {len(result)}자")
        return result


async def aiofiles_resource_client_task(client_id: int):
    """
    aiofiles 기반 리소스를 호출하는 클라이언트 작업
    """
    print(f"aiofiles 클라이언트 {client_id}: 시작")
    start_time = time.time()
    
    async with Client("http://0.0.0.0:9000/mcp") as client:
        result = await client.read_resource("file://log.txt")
        end_time = time.time()
        elapsed = end_time - start_time
        print(f"aiofiles 클라이언트 {client_id}: 완료 - 소요시간: {elapsed:.2f}초")
        print(f"aiofiles 클라이언트 {client_id}: 결과 길이 - {len(result)}자")
        return result


async def main():
    """
    open() vs aiofiles 리소스 성능 비교 테스트
    """
    print("open() vs aiofiles 리소스 성능 비교 테스트를 시작합니다...\n")
    
    # open() 리소스 테스트
    print("=" * 50)
    print("open() 리소스 테스트 시작")
    print("=" * 50)
    
    open_start = time.time()
    open_tasks = [open_resource_client_task(i+1) for i in range(3)]
    open_results = await asyncio.gather(*open_tasks)
    open_end = time.time()
    open_elapsed = open_end - open_start
    
    print(f"\nopen() 리소스 테스트 완료! 총 소요시간: {open_elapsed:.2f}초")
    
    # 테스트 사이 대기
    print("\n" + "="*50)
    print("잠깐 대기 중...")
    print("="*50)
    await asyncio.sleep(2)
    
    # aiofiles 리소스 테스트
    print("=" * 50)
    print("aiofiles 리소스 테스트 시작")
    print("=" * 50)
    
    aiofiles_start = time.time()
    aiofiles_tasks = [aiofiles_resource_client_task(i+1) for i in range(3)]
    aiofiles_results = await asyncio.gather(*aiofiles_tasks)
    aiofiles_end = time.time()
    aiofiles_elapsed = aiofiles_end - aiofiles_start
    
    print(f"\naiofiles 리소스 테스트 완료! 총 소요시간: {aiofiles_elapsed:.2f}초")
    
    # 결과 요약
    print("\n" + "="*60)
    print("테스트 결과 요약")
    print("="*60)
    print(f"open() 리소스 소요시간: {open_elapsed:.2f}초")
    print(f"aiofiles 리소스 소요시간: {aiofiles_elapsed:.2f}초")
    print(f"성능 차이: {abs(open_elapsed - aiofiles_elapsed):.2f}초")
    
    if open_elapsed > aiofiles_elapsed:
        print("aiofiles가 더 효율적입니다!")
    elif aiofiles_elapsed > open_elapsed:
        print("open()이 더 빨랐습니다!")
    else:
        print("두 방식의 성능이 비슷합니다.")
    
    print("테스트 완료!")


if __name__ == '__main__':
    asyncio.run(main())