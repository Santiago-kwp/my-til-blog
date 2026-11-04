import threading
import time

shared_counter = 0

def increase():
    global shared_counter
    for _ in range(100000):
        # 파이썬 내부에서 `shared_counter += 1`은
        # (1) 값 읽기 -> (2) 1 더하기 -> (3) 저장하기의 과정을 거침
        # 이 과정 중간에 다른 스레드로 제어권이 넘어가면 값이 유실됨
        # shared_counter += 1 # 이것만 하면 계속 200,000이 나옴
        # 아래와 같이 해야 매번 다른 값이 나온다
        tmp = shared_counter
        time.sleep(0)
        shared_counter = tmp + 1



if __name__ == "__main__":
    t1 = threading.Thread(target=increase)
    t2 = threading.Thread(target=increase)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(f"기대 결과: 200000")
    print(f"실제 결과: {shared_counter}")