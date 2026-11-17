import sys
import threading
import time


def run(label, make_worker, n_threads=4, n=20_000):
    state = {"counter": 0}
    lock = threading.Lock()
    worker = make_worker(state, lock)
    ts = [threading.Thread(target=worker, args=(n,)) for _ in range(n_threads)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    print(f"{label:<40} 결과 {state['counter']:>9,} / 기대 {n_threads * n:,}")


def naive(state, lock):
    def w(n):
        for _ in range(n):
            state["counter"] += 1
    return w


def forced_switch(state, lock):
    def w(n):
        for _ in range(n):
            tmp = state["counter"]       # LOAD
            time.sleep(0)                # GIL을 놓는 지점 (컨텍스트 스위칭 흉내)
            state["counter"] = tmp + 1   # INCR + STORE
    return w


def forced_switch_locked(state, lock):
    def w(n):
        for _ in range(n):
            with lock:
                tmp = state["counter"]
                time.sleep(0)
                state["counter"] = tmp + 1
    return w


if __name__ == "__main__":
    sys.setswitchinterval(1e-6)
    gil = sys._is_gil_enabled() if hasattr(sys, "_is_gil_enabled") else True
    print(f"python {sys.version.split()[0]} | GIL enabled: {gil}")
    for trial in range(3):
        run("1) counter += 1 (그냥)", naive, n=200_000)
    for trial in range(3):
        run("2) LOAD 뒤에 GIL 놓는 지점이 있음", forced_switch)
    run("3) 2)에 threading.Lock 적용", forced_switch_locked)