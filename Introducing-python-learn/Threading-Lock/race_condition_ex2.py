import threading

shared_counter = 0 

# 1. 락 개체 생성
lock = threading.Lock()

def safe_increase():
    global shared_counter
    for _ in range(100000):
        # 2. 'with lock'을 쓰면 자동으로 acquire()(락 획득)과 release()(락 해제)를 처리해 준다.
        # 예외가 발생해도 안전하게 락이 해제되므로 가장 권장되는 패턴
        with lock:
            shared_counter += 1

if __name__ == "__main__":
    t1 = threading.Thread(target=safe_increase)
    t2 = threading.Thread(target=safe_increase)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(f"기대 결과: 200000")
    print(f"실제 결과: {shared_counter}")
