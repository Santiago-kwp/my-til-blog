# 리눅스 시스템 구성 정보 확인하기

## 1.1 커널 정보 확인하기

### uname - 커널 버전 확인
```bash
$ uname -a
Linux server1-HW_NAME 7.0.0-28-generic #28~24.04.1-Ubuntu SMP PREEMPT_DYNAMIC Wed Jul  1 15:50:57 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
```

- `7.0.0-28-generic` : 커널 릴리스. `7.0.0`: 메인라인 버전, `-28`: Ubuntu 패치 빌드, `generic`: 범용 커널 플레이버(?)
- `#28~24.04.1-Ubuntu SMP PREEMPT_DYNAMIC Wed Jul  1 15:50:57 UTC 2`: 빌드 번호, 빌드 일시
- `SMP` : 멀티코어(대칭형 멀티프로세싱?) 지원 커널
- `PREEMPT_DYNAMIC` : 부팅 시 `preempt=`로 선점 수준(none/voluntary/full)을 바꿀 수 있는 동적 선점 커널(지연시간 튜닝 포인트)
- `x86_64` : x86계열 64비트 OS

### dmesg - 커널 디버그 메시지
> 커널이 부팅할 때/운영 중 발생시키는 메시지를 볼 수 있음.
메모리 인식 과정, 하드웨어,드라이버 인식, 부팅 시 적용된 커널 파라미터를 확인할 수 있음.
`dmesg`는 "display message" 또는 "driver message"를 의미하며, 대부분의 리눅스와 유닉스 기반 운영체제의 명령어로 커널의 메시지 버퍼를 출력함.

```bash
sudo dmesg | grep -i kernel | more
[    0.043007] Kernel command line: BOOT_IMAGE=/boot/vmlinuz-7.0.0-31-generic root=UUID=1965f7ea-146f-40e8-8214-3f90
c6064f75 ro quiet splash vt.handoff=7
[    0.128279] Memory: 14121392K/16497344K available (23168K kernel code, 4936K rwdata, 16692K rodata, 5424K init, 5
744K bss, 2360632K reserved, 0K cma-reserved)
...
```

1. Command line (부팅 시 적용된 커널 파라미터) : 부팅 때만 적용되는 옵션들
`/proc/cmdline`으로 동일하게 확인 가능

```bash
cat /proc/cmdline
BOOT_IMAGE=/boot/vmlinuz-7.0.0-28-generic root=UUID=ec~~~~~~~~ ro quiet splash vt.handoff=7
```

2. crashkernel : 커널 패닉에 대비해 crashkernel 이미지를 미리 로딩
패닉이 나면 이걸로 부팅해 디버깅 정보(크래시 덤프)를 저장, 원인 추적에 씁니다.

3. Memory : 부팅 시 커널이 인식한 메모리 정보
여기서 본 가용 메모리와 부팅 완료 후 `free`로 보는 값이 조금 다른데, 부팅 과정에서 쓰인 일부 메모리가 완료 후 반환되기 때문

* intel_idle.max_cstate 이야기
> 최신 CPU에는 C-State라는 옵션이 있어 Idle 상태가 되면 일부 코어를 잠자기 모드로 전환해 전력을 아낌. 하지만 트래픽이 급증할 대 잠든 코어를 다시 깨워야 해서 성능 저하(레이턴시 튐)가 생김.
그래서 성능이 중요한 서버는 C-State를 끄는데, 하드웨어 BIOS에서 꺼도 `intel_idle` 소프트웨어 모듈이 이를 무시하고 C-State를 동작시킬 수 있음. 
이 현상을 막으려면 부팅 파라미터로 `intel_idle.max_cstate=0`을 줘서 `intel_idle` 모듈을 쓰지 않게 해야 함.

### 커널 컴파일 옵션 확인
커널 기능 중 일부는 컴파일 옵션에 포함되어야만 쓸 수 있음.

```bash
cat /boot/config-$(uname -r) | head
#
# Automatically generated file; DO NOT EDIT.
# Linux/x86 7.0.14 Kernel Configuration
#
CONFIG_CC_VERSION_TEXT="x86_64-linux-gnu-gcc-13 (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0"
CONFIG_CC_IS_GCC=y
CONFIG_GCC_VERSION=130300
CONFIG_CLANG_VERSION=0
CONFIG_AS_IS_GNU=y
CONFIG_AS_VERSION=24200
```

> 맨 위에 이 커널을 빌드한 GCC 13.3.0 버전까지 기록되어 있습니다.
특정 기능이 켜져 있는지는 `grep -i <옵션>`으로 확인할 수 있습니다.
예를 들어 `ftrace` 같은 커널 함수 레벨 추적이 필요하면 아래 옵션이 켜져 있어야 합니다.

```bash
cat /boot/config-$(uname -r) | grep -i config_function_tracer
CONFIG_FUNCTION_TRACER=y
```

## 1.2 CPU 정보 확인하기
하드웨어 정보는 `dmidecode` 명령으로 확인할 수 있으며, 출력이 엄청 많기 때문에 `-t` 키워드로 필요한 것만 보는 것이 좋음.

> `dmidecode` 명령어는 컴퓨터의 메인보드에 있는 DMI(Desktop Management Interface, SMBIOS) 테이블의 정보를 사람이 읽을 수 있는 텍스트 형태로 해독(디코딩)한다는 의미임.

> 키워드는 총 9가지: bios, system, baseboard, chasssis, processor, memory, cache, connector, slot

CPU, BIOS 확인에는 **bios / system / processor** 3개를 주로 쓴다.

### bios 키워드 - BIOS 버전 확인
```bash
dmidecode -t bios
# dmidecode 3.5
Getting SMBIOS data from sysfs.
SMBIOS 3.3.0 present.

Handle 0x0000, DMI type 0, 26 bytes
BIOS Information
        Vendor: Intel Corp.
        Version: ATJSLCPX.0047.2025.0102.1252
        Release Date: 01/02/2025
        Address: 0xF0000
        Runtime Size: 64 kB
        ROM Size: 10 MB
        Characteristics:
                PCI is supported
                BIOS is upgradeable
                BIOS shadowing is allowed
                Boot from CD is supported
                Selectable boot is supported
                BIOS ROM is socketed
                EDD is supported
                5.25"/1.2 MB floppy services are supported (int 13h)
                3.5"/720 kB floppy services are supported (int 13h)
                3.5"/2.88 MB floppy services are supported (int 13h)
                Print screen service is supported (int 5h)
                Serial services are supported (int 14h)
                Printer services are supported (int 17h)
                ACPI is supported
                USB legacy is supported
                BIOS boot specification is supported
                Targeted content distribution is supported
                UEFI is supported
        BIOS Revision: 0.47
        Firmware Revision: 2.4

Handle 0x0020, DMI type 13, 22 bytes
BIOS Language Information
        Language Description Format: Long
        Installable Languages: 1
                en|US|iso8859-1
        Currently Installed Language: en|US|iso8859-1

Handle 0x003C, DMI type 13, 22 bytes
BIOS Language Information
        Language Description Format: Abbreviated
        Installable Languages: 1
                enUS
        Currently Installed Language: enUS
```

- 특정 BIOS 버전에 문제 보고가 있을 때, 내 서버가 해당 버전인지 확인하는 용도

### system 키워드 - 장비 모델명 확인
```bash
dmidecode -t system
# dmidecode 3.5
Getting SMBIOS data from sysfs.
SMBIOS 3.3.0 present.

Handle 0x0001, DMI type 1, 27 bytes
System Information
        Manufacturer: Intel(R) Client Systems
        Product Name: NUC11ATKC2
        Version: M53060-501
        Serial Number: G6AT349005SM
        UUID: 2e67777d-63a4-8ffb-6b1e-88aedd64bf2f
        Wake-up Type: Power Switch
        SKU Number: BNUC11ATKC2000
        Family: AT

Handle 0x002A, DMI type 15, 73 bytes
System Event Log
        Area Length: 4096 bytes
        Header Start Offset: 0x0000
        Header Length: 16 bytes
        Data Start Offset: 0x0010
        Access Method: Memory-mapped physical 32-bit address
        Access Address: 0xFF660000
        Status: Valid, Not Full
        Change Token: 0x00000001
        Header Format: Type 1
        Supported Log Type Descriptors: 25
        Descriptor 1: Single-bit ECC memory error
        Data Format 1: Multiple-event handle
        Descriptor 2: Multi-bit ECC memory error
        Data Format 2: Multiple-event handle
        Descriptor 3: Parity memory error
        Data Format 3: None
        Descriptor 4: Bus timeout
        Data Format 4: None
        Descriptor 5: I/O channel block
        Data Format 5: None
        Descriptor 6: Software NMI
        Data Format 6: None
        Descriptor 7: POST memory resize
        Data Format 7: None
        Descriptor 8: POST error
        Data Format 8: POST results bitmap
        Descriptor 9: PCI parity error
        Data Format 9: Multiple-event handle
        Descriptor 10: PCI system error
        Data Format 10: Multiple-event handle
        Descriptor 11: CPU failure
        Data Format 11: None
        Descriptor 12: EISA failsafe timer timeout
        Data Format 12: None
        Descriptor 13: Correctable memory log disabled
        Data Format 13: None
        Descriptor 14: Logging disabled
        Data Format 14: None
        Descriptor 15: System limit exceeded
        Data Format 15: None
        Descriptor 16: Asynchronous hardware timer expired
        Data Format 16: None
        Descriptor 17: System configuration information
        Data Format 17: None
        Descriptor 18: Hard disk information
        Data Format 18: None
        Descriptor 19: System reconfigured
        Data Format 19: None
        Descriptor 20: Uncorrectable CPU-complex error
        Data Format 20: None
        Descriptor 21: Log area reset/cleared
        Data Format 21: None
        Descriptor 22: System boot
        Data Format 22: None
        Descriptor 23: End of log
        Data Format 23: None
        Descriptor 24: OEM-specific
        Data Format 24: OEM-specific
        Descriptor 25: OEM-specific
        Data Format 25: OEM-specific

Handle 0x003B, DMI type 32, 11 bytes
System Boot Information
        Status: No errors detected
```

- 모델명(NUC11ATKC2)으로 장비가 어느정도 성능을 낼 수 있는지 가늠합니다.

### processor 키워드 - CPU 정보 확인
```bash
dmidecode -t processor
# dmidecode 3.5
Getting SMBIOS data from sysfs.
SMBIOS 3.3.0 present.

Handle 0x0033, DMI type 4, 48 bytes
Processor Information
        Socket Designation: U3E1
        Type: Central Processor
        Family: Celeron
        Manufacturer: Intel(R) Corporation
        ID: C0 06 09 00 FF FB EB BF
        Signature: Type 0, Family 6, Model 156, Stepping 0
        Flags:
                FPU (Floating-point unit on-chip)
                VME (Virtual mode extension)
                DE (Debugging extension)
                PSE (Page size extension)
                TSC (Time stamp counter)
                MSR (Model specific registers)
                PAE (Physical address extension)
                MCE (Machine check exception)
                CX8 (CMPXCHG8 instruction supported)
                APIC (On-chip APIC hardware supported)
                SEP (Fast system call)
                MTRR (Memory type range registers)
                PGE (Page global enable)
                MCA (Machine check architecture)
                CMOV (Conditional move instruction supported)
                PAT (Page attribute table)
                PSE-36 (36-bit page size extension)
                CLFSH (CLFLUSH instruction supported)
                DS (Debug store)
                ACPI (ACPI supported)
                MMX (MMX technology supported)
                FXSR (FXSAVE and FXSTOR instructions supported)
                SSE (Streaming SIMD extensions)
                SSE2 (Streaming SIMD extensions 2)
                SS (Self-snoop)
                HTT (Multi-threading)
                TM (Thermal monitor supported)
                PBE (Pending break enabled)
        Version: Intel(R) Celeron(R) N4505 @ 2.00GHz
        Voltage: 1.1 V
        External Clock: 100 MHz
        Max Speed: 2900 MHz
        Current Speed: 2900 MHz
        Status: Populated, Enabled
        Upgrade: Other
        L1 Cache Handle: 0x0030
        L2 Cache Handle: 0x0031
        L3 Cache Handle: 0x0032
        Serial Number: To Be Filled By O.E.M.
        Asset Tag: To Be Filled By O.E.M.
        Part Number: To Be Filled By O.E.M.
        Core Count: 2
        Core Enabled: 2
        Thread Count: 2
        Characteristics:
                64-bit capable
                Multi-Core
                Execute Protection
                Enhanced Virtualization
                Power/Performance Control
```

#### Socket vs Core vs Thread
- 소켓 : 물리적인 CPU 칩의 개수 (예제: 1개)
- 코어 : 한 소켓(CPU) 안에 들어 있는 물리 연산 코어 개수 (예제: 2개)
- 스레드 : 하이퍼스레딩(HT)으로 코어 하나가 논리적으로 여러 개처럼 동작 (예제: 2개)

> Ex. 현재 서버: 소켓 1 개 X 코어 2 개 = 물리 코어 2 개. HT 미지원으로로 소켓당 2 스레드 $\rarr$ 시스템 전체 2개 논리 코어
`nproc`, `lscpu`로 확인 가능
```ini
Intel Celeron N4505
├─ Socket 1개
├─ Core 2개
├─ Thread 2개
└─ HT(Hyper-Threading) 미지원
```

#### HT(Hyper-Threading) 이란?
> CPU 한 개의 물리 코어를 운영체제가 두 개의 논리 코어처럼 보도록 하는 기술
참고로, 현재 예제 CPU를 기준으로 보면 운영체제에서 2개 CPU로 인식하는 HT가 없는 경우임.

- HT가 없는 경우
예를 들어 2코어 CPU에서 프로그램 2개를 실행하면 
```
프로그램 A $\rarr$ Core 0
프로그램 B $\rarr$ Core 1
```
처럼 배치됨
그런데 실제 CPU 내부를 보면 연산장치(ALU), FPU, 캐시 등에 빈 시간이 자주 생김.
예를 들어:
```
1. 메모리 읽기
2. 메모리 응답 대기
3. 계산
```
과정에서 CPU가 메모리 응답을 기다리는 동안 일부 연산 유닛이 놀게 됨.

---
- HT가 있는 경우
인텔은 이런 빈 시간을 활용하려고 하나의 코어 안에 두 개의 실행 문맥(Thread Context)을 둔다.

> 실행 문맥(Execution Context) = 아키텍처 상태(Architectural State)
프로그램이 실행되려면 최소한으로 필요한 전용 하드웨어(PC/명령어 포인터, 범용 레지스터, 플래그 레지스터 등)만 복제한 것

> 물리 코어를 2개 만드는 것은 칩 면적과 전력 소모가 2배로 들지만, 하이퍼 스레딩은 **코어 면적을 약 5%만 늘리고도 논리 코어 2개를 만들어 15~30%의 추가 처리량(Throughput)** 을 얻는 기술

예를 들어:
```
물리 코어 1개
 ├─ 논리 CPU 0
 └─ 논리 CPU 1
```
운영체제는 이를 CPU 2개로 본다.
실제 구조는 대략:
```
            +----------------+
Logical #0  | 레지스터 집합 A  |
            +----------------+
                    │
                    │
            +----------------+
            |  연산장치 공유   |
            |  캐시 공유      |
            +----------------+
                    │
                    │
            +----------------+
Logical #1  | 레지스터 집합 B  |
            +----------------+
```
즉, 다음과 같이 정리할 수 있다.
|구성 요소|	상태	|이유|
|-|-|-|
|레지스터|	따로 가짐 (스레드별 복제)	|스레드의 독립된 상태(PC, 데이터)를 보존하고, 비용(면적)이 매우 작기 때문|
|연산 유닛	|공유	|어차피 단일 스레드가 다 못 쓰므로 빈 틈을 채워 효율(가성비)을 극대화하기 위함|
|캐시|	공유	|면적 한계 극복 및 작업량에 따라 용량을 동적으로 유연하게 나눠 쓰기 위함

> 1. 레지스터를 따로 가지는 이유
- 독립적인 상태 보존:
    - 레지스터에는 현재 실행 중인 코드의 주소(PC/IP), 연산 중인 임시 값(RAX, RBX 등), 상태 플래그 등이 들어감
    - 만약 레지스터를 공유한다면, 스레드 A가 계산하던 중간값을 스레드 B가 즉시 덮어써 버려 프로그램이 깨짐
    - OS 입장에서 "독립적인 2개의 CPU"로 인식하게 만들려면 **각 스레드의 상태가 완전히 분리**되어 있어야 함.
- 면적(비용)이 매우 작음:
    - 레지스터 세트를 하나 더 만드는 것은 CPU 코어 전체 면적의 약 1~5% 밖에 차지하지 않아 비용부담이 거의 없음

> 2.연산 유닛(ALU, FPU)를 공유하는 이유(자원 낭비 방지)
- 단일 스레드는 연산 유닛을 100% 다 쓰지 못함:
    - 최신 CPU는 내부에 여러 개의 정수 연산기(ALU), 부동소수점 연산기(FPU), 메모리 로드/스토어 유닛을 가지고 있음.
    - 하지만 일반적인 프로그램 코드는 명령어 간의 의존성(앞 계산이 끝나야 뒤 계산을 함) 때문에 한 사이클에 이 모든 연산기를 동시에 풀가동하지 못함.
    - 따라서 비어 있는 연산 유닛에 **다른 스레드의 명령어를 즉시 집어넣어 처리(동시 발행)** 하기 위해 공유함.
- 비용 절감: 연산 유닛을 2배로 늘리면 코어 크기, 발열, 전력 소모가 극심하게 커짐

> 3. 캐시(L1, L2)를 공유하는 이유 (유연성과 칩 크기)
- 면적 한계: 캐시 메모리는 CPU 다이(Die) 면적의 상당 부분을 차지한다. L1, L2 캐시마저 스레드별로 쪼개거나 2배로 늘리면 물리 코어를 하나 더 만드는 것과 다르지 않다.
- 동적 자원 할당 (유연성):
    - 만약 캐시를 반반씩 물리적으로 나누면, 스레드 A는 데이터가 적게 필요하고 스레드 B는 많이 필요할 때 자원이 낭비된다.
    - 공유 구조로 두면 상황에 따라 필요한 스레드가 캐시 용량을 유연하게 더 많이 쓸 수 있다.
    - 같은 프로세스 내의 멀티스레드 프로그램인 경우, 두 스레드가 같은 메모리 영역을 읽을 때 캐시를 공유하므로 메모리 접근 속도가 비약적으로 빨라진다.

---

#### HT 효과 예시
> 하이퍼 스레딩의 핵심은 **한 스레드가 멈칫(Stall)하거나 놀고 있을 때, 다른 스레드의 일을 대신 밀어 넣는 것**임. 

시나리오 1: 메모리 지연(Memory Stall) 숨기기 (가장 대표적)
CPU 연산 속도는 나노초 단위 이하이지만, RAM(메인 메모리)에서 데이터를 가져오는 데는 수백 사이클(수십 나노초)이 걸림.

- HT가 없는 경우:
```
Cycle 1~5   : 스레드 A - 연산 수행
Cycle 6     : 스레드 A - 캐시 미스 발생 (RAM에서 데이터 읽기 요청)
Cycle 7~100 : 스레드 A - 대기 (연산 유닛은 94사이클 동안 완전히 놂)
Cycle 101~  : 스레드 A - 도착한 데이터로 연산 재개
```

- HT가 있는 경우:
```
Cycle 1~5   : 스레드 A - 연산 수행
Cycle 6     : 스레드 A - 캐시 미스 발생 (RAM에 데이터 요청하고 대기 모드 진입)
Cycle 7~100 : [스위칭] 스레드 B가 즉시 연산 유닛을 이어받아 연산 수행!
Cycle 101~  : 스레드 A 데이터 도착 -> 스레드 B 연산 사이사이에 스레드 A 연산 투입
```

> 효과적인 작업: 웹 서버(Nginx, Spring), 데이터베이스(MySQL), I/O 작업이 잦은 엔터프라이즈 서버 등. (메모리 접근 및 I/O 대기 시간이 잦아 놀고 있는 연산 유닛을 알뜰하게 활용함)

--- 
시나리오 2: 서로 다른 연산기 사용 (명령어 혼합)
최신 코어 내부에는 `정수 연산기(ALU)`와 `실수/벡터 연산기(FPU/SIMD)` 등이 독립된 포트로 나뉘어 있음.
- 상황:
    - 스레드 A: 정수 조건문 및 루프 제어 (`ALU` 사용)
    - 스레드 B: 3D 그래픽 부동소수점 계산 (`FPU` 사용)
- 동작:
    - 두 스레드의 명령어가 **동일한 클록 사이클에 코어 내 서로 다른 연산 포트로 동시 투입**됨.
    - 물리 코어는 1개지만, 서로 다른 유닛을 쓰므로 병목 없이 2배에 가까운 연산 효율을 냄

---
#### HT가 효과가 없거나 손해인 경우

1. 연산 유닛을 100% 쥐어짜는 작업(연산 병목)
    - 두 스레드가 모두 무거운 AVX-512 벡터 연산이나 100% 정수 행렬 연산만 수행한다면, 어차피 연산 유닛이 하나뿐이므로 서로 자원을 차지하려고 줄을 섬. 이 경우 성능 향상은 0~5% 수준

2. 캐시 경쟁 (Cash Thrashing)
    - 스레드 A와 스레드 B가 둘 다 거대한 데이터 세트를 다루면, 서로의 데이터를 L1/L2 캐시에서 밀어내버려 캐시 미스(Cache Miss)가 폭증함. 이 경우 HT를 껐을 때보다 오히려 성능이 떨어질 수 있음
3. 지연 시간(Latency)이 극도로 중요한 작업
    - 한 스레드의 응답 속도 자체가 아주 중요한 고빈도 매매(HFT)나 일부 하이엔드 게임 환경에서는, 다른 스레드의 간섭으로 인한 미세한 지터(Jitter)를 방지하기 위해 의도적으로 하이퍼 스레딩을 끄기도 함.


