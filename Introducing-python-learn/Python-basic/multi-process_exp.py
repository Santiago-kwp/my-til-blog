import time
from concurrent.futures import ProcessPoolExecutor

def cpu_task(n):                       # 최상위 함수여야 다른 프로세스로 전달(pickle)할 수 있다
    s = 0
    for i in range(n):
        s += i * i
    return s

if __name__ == "__main__":             # spawn/forkserver에서는 필수
    work = [6_000_000] * 4

    t = time.perf_counter()
    [cpu_task(n) for n in work]
    print("순차    ", time.perf_counter() - t)

    t = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as ex:   # 프로세스마다 별도의 GIL
        list(ex.map(cpu_task, work))
    print("프로세스", time.perf_counter() - t)
# 측정(코어 2개, 3.13): 순차 0.91s / 스레드 0.99s / 프로세스 0.53s