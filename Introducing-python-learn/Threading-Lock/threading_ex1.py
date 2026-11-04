import threading
import time

def worker(worker_id):
    print(f"[작업자 {worker_id}] 작업 시작")
    # 네트워크 요청이나 파일 I/O를 흉내 내는 대기 시간
    time.sleep(2)
    print(f"[작업자 {worker_id}] 작업 완료!")

if __name__ == "__main__":
    start_time = time.time()

    threads = []
    # 3개의 스레드 생성
    for i in range(1, 4):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start() # 스레드 실행 시작 (비동기)

    # 모든 스레드가 끝날 때까지 메인 스레드가 대기(join)
    for t in threads:
        t.join()

    # (예상) 2초 / (결과) 2초
    print(f"총 소요 시간: {time.time() - start_time:.2f}초")

