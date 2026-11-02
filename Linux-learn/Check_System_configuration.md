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


### /proc/cpuinfo 와 lscpu

CPU 정보는 `/proc/cpuinfo` 파일로도 볼 수 있습니다.
```bash
# cat /proc/cpuinfo | head -30
processor       : 0
vendor_id       : GenuineIntel
cpu family      : 6
model           : 156
model name      : Intel(R) Celeron(R) N4505 @ 2.00GHz
stepping        : 0
microcode       : 0x24000026
cpu MHz         : 799.991
cache size      : 4096 KB
physical id     : 0
siblings        : 2
core id         : 0
cpu cores       : 2
apicid          : 0
initial apicid  : 0
fpu             : yes
fpu_exception   : yes
cpuid level     : 27
wp              : yes
flags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc cpuid aperfmperf tsc_known_freq pni pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 sdbg cx16 xtpr pdcm sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave rdrand lahf_lm 3dnowprefetch cpuid_fault epb cat_l2 cdp_l2 ssbd ibrs ibpb stibp ibrs_enhanced tpr_shadow flexpriority ept vpid ept_ad fsgsbase tsc_adjust smep erms rdt_a rdseed smap clflushopt clwb intel_pt sha_ni xsaveopt xsavec xgetbv1 xsaves split_lock_detect dtherm ida arat pln pts hwp hwp_notify hwp_act_window hwp_epp hwp_pkg_req vnmi umip waitpkg gfni rdpid movdiri movdir64b md_clear flush_l1d arch_capabilities
vmx flags       : vnmi preemption_timer posted_intr invvpid ept_x_only ept_ad flexpriority apicv tsc_offset vtpr mtf vapic ept vpid unrestricted_guest vapic_reg vid ple shadow_vmcs ept_violation_ve ept_mode_based_exec tsc_scaling usr_wait_pause
bugs            : spectre_v1 spectre_v2 spec_store_bypass swapgs srbds mmio_stale_data rfds bhi spectre_v2_user
bogomips        : 3993.60
clflush size    : 64
cache_alignment : 64
address sizes   : 39 bits physical, 48 bits virtual
power management:

processor       : 1
vendor_id       : GenuineIntel
```

> `flags`에 `hypervisor`가 보이면 가상 머신이라는 증거입니다.
`bugs` 줄에는 이 CPU가 노출된 CPU 취약점(meltdown/spectre 등)이 나열됩니다.
`lscpu`의 Vulnerabilities 섹션과 같은 내용
`lscpu`는 요약해서 한눈에 보여주고 **NUMA** 정보까지 함께 표시해줍니다.


```bash
lscpu
Architecture:                x86_64
  CPU op-mode(s):            32-bit, 64-bit
  Address sizes:             39 bits physical, 48 bits virtual
  Byte Order:                Little Endian
CPU(s):                      2
  On-line CPU(s) list:       0,1
Vendor ID:                   GenuineIntel
  Model name:                Intel(R) Celeron(R) N4505 @ 2.00GHz
    CPU family:              6
    Model:                   156
    Thread(s) per core:      1
    Core(s) per socket:      2
    Socket(s):               1
    Stepping:                0
    CPU(s) scaling MHz:      28%
    CPU max MHz:             2900.0000
    CPU min MHz:             800.0000
    BogoMIPS:                3993.60
    Flags:                   fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mm
                             x fxsr sse sse2 ss ht tm pbe syscall nx rdtscp lm constant_tsc art arch_perfmon pebs bts re
                             p_good nopl xtopology nonstop_tsc cpuid aperfmperf tsc_known_freq pni pclmulqdq dtes64 moni
                             tor ds_cpl vmx est tm2 ssse3 sdbg cx16 xtpr pdcm sse4_1 sse4_2 x2apic movbe popcnt tsc_dead
                             line_timer aes xsave rdrand lahf_lm 3dnowprefetch cpuid_fault epb cat_l2 cdp_l2 ssbd ibrs i
                             bpb stibp ibrs_enhanced tpr_shadow flexpriority ept vpid ept_ad fsgsbase tsc_adjust smep er
                             ms rdt_a rdseed smap clflushopt clwb intel_pt sha_ni xsaveopt xsavec xgetbv1 xsaves split_l
                             ock_detect dtherm ida arat pln pts hwp hwp_notify hwp_act_window hwp_epp hwp_pkg_req vnmi u
                             mip waitpkg gfni rdpid movdiri movdir64b md_clear flush_l1d arch_capabilities
Virtualization features:
  Virtualization:            VT-x
Caches (sum of all):
  L1d:                       64 KiB (2 instances)
  L1i:                       64 KiB (2 instances)
  L2:                        1.5 MiB (1 instance)
  L3:                        4 MiB (1 instance)
NUMA:
  NUMA node(s):              1
  NUMA node0 CPU(s):         0,1
Vulnerabilities:
  Gather data sampling:      Not affected
  Ghostwrite:                Not affected
  Indirect target selection: Not affected
  Itlb multihit:             Not affected
  L1tf:                      Not affected
  Mds:                       Not affected
  Meltdown:                  Not affected
  Mmio stale data:           Mitigation; Clear CPU buffers; SMT disabled
  Old microcode:             Not affected
  Reg file data sampling:    Mitigation; Clear Register File
  Retbleed:                  Not affected
  Spec rstack overflow:      Not affected
  Spec store bypass:         Mitigation; Speculative Store Bypass disabled via prctl
  Spectre v1:                Mitigation; usercopy/swapgs barriers and __user pointer sanitization
  Spectre v2:                Mitigation; Enhanced / Automatic IBRS; IBPB conditional; PBRSB-eIBRS Not affected; BHI SW l
                             oop, KVM SW loop
  Srbds:                     Vulnerable: No microcode
  Tsa:                       Not affected
  Tsx async abort:           Not affected
  Vmscape:                   Not affected
```

`lscpu`의 강점:
- `Virtualization features` $\rarr$ `Hypervisor vendor: Xen` : 이 서버가 Xen 위의 VM임을 lscpu가 바로 알려준다.
- `Vulnerabilities` 섹션: Meltdown/Spectre/Mds 등 **CPU 취약점별 완화(mitigation) 적용 여부를 한눈에 볼 수 있다. 패치 상태 점검할 때 유용하다.

## 1.3 메모리 정보 확인하기
`dmidecode -t memory`로 각 메모리 슬롯의 정보(용량, 제조사)를 확인할 수 있습니다.

크게 **Physical Memory Array**(꽂을 수 있는 슬롯 그룹)와 **Memory Device**(실제 꽂힌 메모리)로 나뉩니다.

```bash
# sudo dmidecode -t memory
# dmidecode 3.5
Getting SMBIOS data from sysfs.
SMBIOS 3.3.0 present.

Handle 0x0026, DMI type 16, 23 bytes
Physical Memory Array
        Location: System Board Or Motherboard
        Use: System Memory
        Error Correction Type: None
        Maximum Capacity: 32 GB
        Error Information Handle: Not Provided
        Number Of Devices: 2

Handle 0x0034, DMI type 17, 100 bytes
Memory Device
        Array Handle: 0x0026
        Error Information Handle: Not Provided
        Total Width: 64 bits
        Data Width: 64 bits
        Size: 8 GB
        Form Factor: SODIMM
        Set: None
        Locator: Controller0-ChannelA
        Bank Locator: BANK 0
        Type: DDR4
        Type Detail: Synchronous
        Speed: 3200 MT/s
        Manufacturer: Samsung
        Serial Number: 41ABC2DF
        Asset Tag: 9876543210
        Part Number: M471A1K43EB1-CWE
        Rank: 1
        Configured Memory Speed: 2933 MT/s
        Minimum Voltage: 1.2 V
        Maximum Voltage: 1.2 V
        Configured Voltage: 1.2 V
        Memory Technology: DRAM
        Memory Operating Mode Capability: Volatile memory
        Firmware Version: Not Specified
        Module Manufacturer ID: Bank 1, Hex 0xCE
        Module Product ID: Unknown
        Memory Subsystem Controller Manufacturer ID: Unknown
        Memory Subsystem Controller Product ID: Unknown
        Non-Volatile Size: None
        Volatile Size: 8 GB
        Cache Size: None
        Logical Size: None

Handle 0x0035, DMI type 17, 100 bytes
Memory Device
        Array Handle: 0x0026
        Error Information Handle: Not Provided
        Total Width: 64 bits
        Data Width: 64 bits
        Size: 8 GB
        Form Factor: SODIMM
        Set: None
        Locator: Controller0-ChannelB
        Bank Locator: BANK 1
        Type: DDR4
        Type Detail: Synchronous
        Speed: 3200 MT/s
        Manufacturer: Samsung
        Serial Number: 41ABBC14
        Asset Tag: 9876543210
        Part Number: M471A1K43EB1-CWE
        Rank: 1
        Configured Memory Speed: 2933 MT/s
        Minimum Voltage: 1.2 V
        Maximum Voltage: 1.2 V
        Configured Voltage: 1.2 V
        Memory Technology: DRAM
        Memory Operating Mode Capability: Volatile memory
        Firmware Version: Not Specified
        Module Manufacturer ID: Bank 1, Hex 0xCE
        Module Product ID: Unknown
        Memory Subsystem Controller Manufacturer ID: Unknown
        Memory Subsystem Controller Product ID: Unknown
        Non-Volatile Size: None
        Volatile Size: 8 GB
        Cache Size: None
        Logical Size: None
```

- **Physical Memory Array**: 이 서버는 소켓이 1개(`lscpu | grep "Socket"`), Physical Memory Array 1개. 각 Array에 최대 2개, 최대 32GB까지 장착 가능
- **Memory Device**: 실제 꽂힌 메모리. 용량, 타입, 속도 등
- Memory Array 수: 1개
    - Handle 0x0026
- Memory 슬롯(Device) 수: 2개
    - ChannelA
    - ChannelB
- 현재 장착: 8GB × 2 = 16GB
- 최대 지원: 32GB
- 따라서 슬롯당 최대: 16GB × 2개 = 32GB

## 1.4 디스크 정보 확인하기

### df - 파티션/마운트/디스크 타입

```bash
# df -h
파일 시스템     크기  사용  가용 사용% 마운트위치
tmpfs           1.6G  3.0M  1.6G    1% /run
/dev/nvme0n1p2  468G   80G  365G   18% /
tmpfs           7.7G   13M  7.7G    1% /dev/shm
tmpfs           5.0M  8.0K  5.0M    1% /run/lock
efivarfs        192K   82K  106K   44% /sys/firmware/efi/efivars
/dev/nvme0n1p1  1.1G  6.2M  1.1G    1% /boot/efi
tmpfs           1.6G  152K  1.6G    1% /run/user/1000
```

```bash
hydrosem@hydrosem-NUC11ATKC21:~$ lsblk
NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
loop0         7:0    0     4K  1 loop /snap/bare/5
loop1         7:1    0  44.7M  1 loop /snap/snapd/28254
loop2         7:2    0  66.8M  1 loop /snap/core24/2124
loop3         7:3    0  66.8M  1 loop /snap/core24/1643
loop4         7:4    0    74M  1 loop /snap/core22/2955
loop5         7:5    0 283.9M  1 loop /snap/firefox/9113
loop6         7:6    0 615.3M  1 loop /snap/gnome-46-2404/168
loop7         7:7    0    12M  1 loop /snap/snap-store/1447
loop8         7:8    0 531.4M  1 loop /snap/gnome-42-2204/247
loop9         7:9    0 614.5M  1 loop /snap/gnome-46-2404/164
loop10        7:10   0 531.5M  1 loop /snap/gnome-42-2204/263
loop11        7:11   0   395M  1 loop /snap/mesa-2404/1165
loop12        7:12   0  12.7M  1 loop /snap/firmware-updater/258
loop13        7:13   0  91.7M  1 loop /snap/gtk-common-themes/1535
loop14        7:14   0   402M  1 loop /snap/mesa-2404/1839
loop15        7:15   0  12.7M  1 loop /snap/firmware-updater/262
loop16        7:16   0    74M  1 loop /snap/core22/2437
loop17        7:17   0  50.1M  1 loop
loop18        7:18   0   828K  1 loop /snap/snapd-desktop-integration/387
loop19        7:19   0   828K  1 loop /snap/snapd-desktop-integration/391
loop20        7:20   0  50.3M  1 loop /snap/snapd/27738
loop21        7:21   0 283.8M  1 loop /snap/firefox/9057
loop22        7:22   0  11.6M  1 loop /snap/snap-store/1468
nvme0n1     259:0    0 476.9G  0 disk
├─nvme0n1p1 259:1    0     1G  0 part /boot/efi
└─nvme0n1p2 259:2    0 475.9G  0 part /
```

- 현재 서버는 NVMe SSD
```
NVMe SSD
 └─ nvme0n1
     ├─ p1 (EFI 부트 파티션)
     └─ p2 (Linux 루트 파티션)
```
- 리눅스 디스크 이름 규칙은 보통 다음과 같음

|디스크명|인터페이스|
|-|-|
|`/dev/sda`, `/dev/sdb`|SATA SSD 또는 SATA HDD, SAS 디스크|
|`/dev/nvme0n1`|NVMe SSD(PCIe)|
|`/dev/mmcblk0`|eMMC, SD 카드|
|`/dev/vda`|가상머신 VirtIO 디스크|

### smartctl - 물리 디스크 상세 정보
```bash
sudo smartctl -a /dev/nvme0
smartctl 7.4 2023-08-01 r5530 [x86_64-linux-7.0.0-28-generic] (local build)
Copyright (C) 2002-23, Bruce Allen, Christian Franke, www.smartmontools.org

=== START OF INFORMATION SECTION ===
Model Number:                       SOLIDIGM SSDPFKNU512GZH
Serial Number:                      BTEH41600NGN512A
Firmware Version:                   HPS3
PCI Vendor/Subsystem ID:            0x025e
IEEE OUI Identifier:                0xc8d6b7
Controller ID:                      1
NVMe Version:                       1.4
Number of Namespaces:               1
Namespace 1 Size/Capacity:          512,110,190,592 [512 GB]
Namespace 1 Formatted LBA Size:     512
Local Time is:                      Mon Nov  2 10:14:02 2026 KST
Firmware Updates (0x14):            2 Slots, no Reset required
Optional Admin Commands (0x0017):   Security Format Frmw_DL Self_Test
Optional NVM Commands (0x00df):     Comp Wr_Unc DS_Mngmt Wr_Zero Sav/Sel_Feat Timestmp Verify
Log Page Attributes (0x16):         Cmd_Eff_Lg Ext_Get_Lg Pers_Ev_Lg
Maximum Data Transfer Size:         128 Pages
Warning  Comp. Temp. Threshold:     83 Celsius
Critical Comp. Temp. Threshold:     88 Celsius

Supported Power States
St Op     Max   Active     Idle   RL RT WL WT  Ent_Lat  Ex_Lat
 0 +     3.50W       -        -    0  0  0  0        0       0
 1 +     2.70W       -        -    1  1  1  1     4000    5000
 2 +     2.00W       -        -    2  2  2  2    22000   37000
 3 -   0.0250W       -        -    3  3  3  3      225    2000
 4 -   0.0040W       -        -    4  4  4  4     3000   11999

Supported LBA Sizes (NSID 0x1)
Id Fmt  Data  Metadt  Rel_Perf
 0 +     512       0         0
 1 -    4096       0         0

=== START OF SMART DATA SECTION ===
SMART overall-health self-assessment test result: PASSED

SMART/Health Information (NVMe Log 0x02)
Critical Warning:                   0x00
Temperature:                        22 Celsius
Available Spare:                    100%
Available Spare Threshold:          10%
Percentage Used:                    0%
Data Units Read:                    1,554,879 [796 GB]
Data Units Written:                 3,129,547 [1.60 TB]
Host Read Commands:                 10,871,745
Host Write Commands:                27,834,500
Controller Busy Time:               397
Power Cycles:                       37
Power On Hours:                     2,395
Unsafe Shutdowns:                   4
Media and Data Integrity Errors:    0
Error Information Log Entries:      4
Warning  Comp. Temperature Time:    0
Critical Comp. Temperature Time:    0

Error Information (NVMe Log 0x01, 16 of 256 entries)
No Errors Logged

Self-test Log (NVMe Log 0x06)
Self-test status: No self-test in progress
Num  Test_Description  Status                       Power_on_Hours  Failing_LBA  NSID Seg SCT Code
 0   Short             Completed without error                   1            -     -   -   -    -
```

1. 디스크 모델 및 규격
```
Model Number: SOLIDIGM SSDPFKNU512GZH
NVMe Version: 1.4
Namespace 1 Size/Capacity: 512 GB
```
- 제조사: Solidigm (SK hynix 계열)
- 인터페이스: NVMe SSD
- NVMe 규격: 1.4
- 용량: 512GB
- 현재 서버의 시스템 디스크

2. 디스크 건강 상태
```
SMART overall-health self-assessment test result: PASSED
Critical Warning: 0x00
```
- 현재 시점 디스크 이상 징후 없음

3. SSD 수명 확인
```
Percentage Used: 0%
```
- Percentage Used = SSD 수명 소모율
```
0%  → 새 제품 수준
10% → 수명 90% 남음
50% → 수명 절반 사용
100% → 제조사 보증수명 도달
```

4. 총 읽기/쓰기량
[읽기량]
```
Data Units Read: 1,554,879 [796 GB]
```
[쓰기량]
```
Data Units Written: 3,129,547 [1.60 TB]
```
보통 NVMe SSD는 수백 TB ~ 수천 TB 까지 기록 가능함. 따라서 수명 거의 소모 안 됨

5. 사용 시간
```
Power On Hours: 2395
```
약 100일 정도 전원이 켜져 있었음

6. 전원 ON/OFF 횟수
```
Power Cycles: 37
```

7. 비정상 종료 여부
```
Unsafe Shutdowns: 4
```
강제 전원 차단, 정전, 전원 뽑기, 커널 패닉 등이 4번

8. 실제 오류 여부
```
Media and Data Integrity Errors: 0
```
불량 블록, 데이터 손상, 읽기 오류, 쓰기 오류 발생 횟수가 0회

9. 온도
```
Temperature: 22 Celsius
```

10. 에러 로그
```
Error Information Log Entries: 4
No Errors Logged
```
- 과거에 에러 이벤트 카운트가 증가한 적은 있으나, 현재 SMART에 기록된 실제 오류는 없음

`smartctl` 결과에서 실무적으로 가장 중요하게 보는 값은:
```
SMART overall-health = PASSED
Percentage Used = 0%
Media and Data Integrity Errors = 0
Temperature = 22℃
Unsafe Shutdowns = 4
Data Units Written = 1.6TB
```

## 1.5 네트워크 정보 확인하기

### lspci - 네트워크 카드 모델 확인

```bash
# lspci | grep -i ether
02:00.0 Ethernet controller: Realtek Semiconductor Co., Ltd. RTL8111/8168/8211/8411 PCI Express Gigabit Ethernet Controller (rev 15)
```

1. NIC(Network Interface Card) 모델 - 칩셋: Realtek RTL8111 계열
2. 최대 링크 속도 - Gigabit Ethernet Controller = 1Gbps = 110 ~ 120 MB/s
3. PCIe 기반 랜카드
    - USB 랜카드 아님
    - PCIe 버스에 직접 연결, 즉 메인보드 온보드 NIC
```
CPU
 └ PCIe
     └ Realtek RTL8111
         └ RJ45 LAN 포트
```
4. 현재 실제 링크 속도 확인 : `sudo ethtool eno1`
```bash
# sudo ethtool eno1
Settings for eno1:
        Supported ports: [ TP    MII ]
        Supported link modes:   10baseT/Half 10baseT/Full
                                100baseT/Half 100baseT/Full
                                1000baseT/Full
        Supported pause frame use: Symmetric Receive-only
        Supports auto-negotiation: Yes
        Supported FEC modes: Not reported
        Advertised link modes:  10baseT/Half 10baseT/Full
                                100baseT/Half 100baseT/Full
                                1000baseT/Full
        Advertised pause frame use: Symmetric Receive-only
        Advertised auto-negotiation: Yes
        Advertised FEC modes: Not reported
        Link partner advertised link modes:  10baseT/Half 10baseT/Full
                                             100baseT/Half 100baseT/Full
                                             1000baseT/Full
        Link partner advertised pause frame use: Symmetric
        Link partner advertised auto-negotiation: Yes
        Link partner advertised FEC modes: Not reported
        Speed: 1000Mb/s
        Duplex: Full
        Auto-negotiation: on
        master-slave cfg: preferred slave
        master-slave status: slave
        Port: Twisted Pair
        PHYAD: 0
        Transceiver: external
        MDI-X: Unknown
        Supports Wake-on: pumbg
        Wake-on: g
        Link detected: yes
```
- 링크 속도: 1Gbps
- Full Duplex: 송신/수신 동시 가능
- 물리 연결 상태: 정상
- 즉, 
    - LAN 케이블 정상스위치 정상
    - NIC 정상
    - 최대 속도(1Gbps)로 연결 중
- Wake-on-LAN(WOL)
    - Wake-on: g
    - 즉, 네트워크로 Magic Packet을 보내면 원격 부팅 가능
    ```bash
    # sudo ethtool eno1 | grep Wake-on
        Supports Wake-on: pumbg
        Wake-on: g
    ```

### 인터페이스 목록 확인 (ip)

```bash
# ip -br a
lo               UNKNOWN        127.0.0.1/8 ::1/128
eno1             UP             192.168.1.200/24 fe80::8395:7b76:f1ea:b906/64
wlp0s20f3        UP             192.168.50.107/24 fe80::9af8:cc42:86ac:9d33/64
tailscale0       UNKNOWN        100.125.166.12/32 fd7a:115c:a1e0::9f32:a60d/128 fe80::63f3:9441:d08f:ba53/64
```

1. lo (Loopback)
- 자기 자신과 통신하기 위한 가상 인터페이스
- 127.0.0.1 = localhost
- 항상 존재
- UNKNOWN은 정상

2. eno1 (유선 LAN)
- 현재 케이블이 연결되어 있고 동작 중(UP)

3. wlp0s20f3 (Wi-Fi)
- 무선 랜 장치
- 현재 Wi-Fi 연결 중
- IP 주소: 192.168.50.107

### ethtool - 연결 상태 확인

`ethtool eno1`: 유선 랜카드(eno1)의 물리적 링크 상태와 협상 결과를 확인하는 명령어

```bash
$ sudo ethtool eno1
Settings for eno1:
        Supported ports: [ TP    MII ]
        Supported link modes:   10baseT/Half 10baseT/Full
                                100baseT/Half 100baseT/Full
                                1000baseT/Full
        Supported pause frame use: Symmetric Receive-only
        Supports auto-negotiation: Yes
        Supported FEC modes: Not reported
        Advertised link modes:  10baseT/Half 10baseT/Full
                                100baseT/Half 100baseT/Full
                                1000baseT/Full
        Advertised pause frame use: Symmetric Receive-only
        Advertised auto-negotiation: Yes
        Advertised FEC modes: Not reported
        Link partner advertised link modes:  10baseT/Half 10baseT/Full
                                             100baseT/Half 100baseT/Full
                                             1000baseT/Full
        Link partner advertised pause frame use: Symmetric
        Link partner advertised auto-negotiation: Yes
        Link partner advertised FEC modes: Not reported
        Speed: 1000Mb/s
        Duplex: Full
        Auto-negotiation: on
        master-slave cfg: preferred slave
        master-slave status: slave
        Port: Twisted Pair
        PHYAD: 0
        Transceiver: external
        MDI-X: Unknown
        Supports Wake-on: pumbg
        Wake-on: g
        Link detected: yes
```

```
Speed: 1000Mb/s
Duplex: Full
Link detected: yes
Auto-negotiation: on
```
- 속도: 1Gbps
- Full Duplex: 송신과 수신을 동시에 가능
- 케이블 연결됨
- 자동 협상 사용 중

### ethtool 성능 옵션 3종
`-g` / `-G` : **Ring Buffer 크기 조회/설정**

- Ring Buffer는 NIC(랜카드)가 패킷을 임시 저장하는 하드웨어 큐이다.
- 수신(RX) 패킷은 NIC의 RX Ring Buffer에 등록된 메모리 버퍼로 DMA 전송된 후 커널 네트워크 스택이 처리한다.
- 트래픽이 순간적으로 몰릴 때 버퍼가 너무 작으면 패킷 드롭이 발생할 수 있다.
- 버퍼를 크게 하면 드롭 감소에 도움이 될 수 있지만 메모리 사용량과 지연시간(latency)이 증가할 수 있다.
- ~~보통 `maximum` = `current` 가 되도록 맞춘다.~~ 고부하 환경이 아니라면 기본값을 사용하는 경우가 많다.

```bash
ethtool -g eno1
Ring parameters for eno1:
Pre-set maximums:
RX:                     256
RX Mini:                n/a
RX Jumbo:               n/a
TX:                     256
TX push buff len:       n/a
Current hardware settings:
RX:                     256
RX Mini:                n/a
RX Jumbo:               n/a
TX:                     256
RX Buf Len:             n/a
CQE Size:               n/a
TX Push:                off
RX Push:                off
TX push buff len:       n/a
TCP data split:         n/a
```

- `-g` : Ring Buffer 조회
- `-G` : Ring Buffer 변경

#### 네트워크 패킷 전체 흐름

```
[케이블]

    ↓

[랜카드(NIC)]

    ↓

[RX Ring]

    ↓ (DMA)

[RAM의 수신 버퍼]

    ↓

[커널 네트워크 스택]

    ↓

[응용프로그램]
```

#### RX Ring이란?
- RX는 Receive(수신)의 약자
- RX Ring은 랜카드가 사용할 수 있는 수신 버퍼 목록(queue)
- 예를 들어 RX Ring 크기가 256이면 아래와 같이 256개의 버퍼를 관리한다.
        ```
        RX Ring

        [0]
        [1]
        [2]
        ...
        [255]
        ```

- 정확히 말하면 RX Ring 안에 실제 패킷 데이터가 들어있는 것이 아니라 "RAM의 어느 위치에 패킷을 저장해라"라는 정보(포인터)가 들어 있음.

        RX Ring Entry 0 → RAM 주소 A
        RX Ring Entry 1 → RAM 주소 B
        RX Ring Entry 2 → RAM 주소 C
        ...
- 랜카드는 이 목록을 보면서 "패킷이 오면 A에 저장", "다음 패킷은 B에 저장"처럼 동작함.
- 그래서 이름이 Ring(원형 버퍼)임. 끝까지 가면 다시 처음으로 돌아옴

#### DMA
DMA = Direct Memory Access

> 직접 메모리 접근으로, 예전 방식이라면 
NIC $\rarr$ CPU $\rarr$ RAM, 순서로 이동해야 함.
즉 CPU가 패킷 하나하나를 복사하는 식임.

> 하지만 네트워크 트래픽이 많아지면 CPU가 너무 바빠지기 때문에 DMA를 사용함.

DMA 사용 시 NIC $\rarr$ RAM으로 바로 감.
CPU는 "버퍼 주소는 여기야", "패킷 오면 여기에 써"만 알려주고 나머지는 랜카드가 직접 처리함.

#### RX Ring이 작으면?

만약 RX = 4라고 가정했을 때 갑자기 패킷이 많이 들어오면 CPU가 처리하지 못한 상태에서 패킷5가 오면 저정할 공간이 없음 $\rarr$ 패킷 유실 발생

--- 

`-k` / `-K` : **NIC 오프로드(Offload) 기능**

- `-k`: 랜카드가 CPU 대신 수행하는 기능 조회
- `-K`: 기능 활성화/비활성화

#### Offload란?
- 원래는 CPU가 해야 할 작업을 NIC로 넘기는 기술
- 즉, CPU 사용률 감소, 처리량 증가가 목적이다.

```bash
$ ethtool -k eno1
Features for eno1:
rx-checksumming: on
tx-checksumming: on
        tx-checksum-ipv4: on
        tx-checksum-ip-generic: off [fixed]
        tx-checksum-ipv6: on
        tx-checksum-fcoe-crc: off [fixed]
        tx-checksum-sctp: off [fixed]
scatter-gather: on
        tx-scatter-gather: on
        tx-scatter-gather-fraglist: off [fixed]
tcp-segmentation-offload: on
        tx-tcp-segmentation: on
        tx-tcp-ecn-segmentation: off [fixed]
        tx-tcp-mangleid-segmentation: off
        tx-tcp6-segmentation: on
        tx-tcp-accecn-segmentation: off [fixed]
generic-segmentation-offload: on
generic-receive-offload: on
large-receive-offload: off [fixed]
rx-vlan-offload: on
tx-vlan-offload: on
ntuple-filters: off [fixed]
receive-hashing: off [fixed]
highdma: on [fixed]
rx-vlan-filter: off [fixed]
vlan-challenged: off [fixed]
tx-gso-robust: off [fixed]
tx-fcoe-segmentation: off [fixed]
tx-gre-segmentation: off [fixed]
tx-gre-csum-segmentation: off [fixed]
tx-ipxip4-segmentation: off [fixed]
tx-ipxip6-segmentation: off [fixed]
tx-udp_tnl-segmentation: off [fixed]
tx-udp_tnl-csum-segmentation: off [fixed]
tx-gso-partial: off [fixed]
tx-tunnel-remcsum-segmentation: off [fixed]
tx-sctp-segmentation: off [fixed]
tx-esp-segmentation: off [fixed]
tx-udp-segmentation: off [fixed]
tx-gso-list: off [fixed]
tx-nocache-copy: off
loopback: off [fixed]
rx-fcs: off
rx-all: off
tx-vlan-stag-hw-insert: off [fixed]
rx-vlan-stag-hw-parse: off [fixed]
rx-vlan-stag-filter: off [fixed]
l2-fwd-offload: off [fixed]
hw-tc-offload: off [fixed]
esp-hw-offload: off [fixed]
esp-tx-csum-hw-offload: off [fixed]
rx-udp_tunnel-port-offload: off [fixed]
tls-hw-tx-offload: off [fixed]
tls-hw-rx-offload: off [fixed]
rx-gro-hw: off [fixed]
tls-hw-record: off [fixed]
rx-gro-list: off
macsec-hw-offload: off [fixed]
rx-udp-gro-forwarding: off
hsr-tag-ins-offload: off [fixed]
hsr-tag-rm-offload: off [fixed]
hsr-fwd-offload: off [fixed]
hsr-dup-offload: off [fixed]
```

#### Checksum Offload
- 패킷이 깨졌는지 확인하는 무결성 값
- 원래는 CPU가 계산한다

#### TX Checksum Offload
```
Application
 ↓
Kernel
 ↓
NIC
```
- CPU가 계산하지 않고 NIC가 패킷 전송 직전에 계산

#### RX Checksum Offload
- 패킷 수신 시 정상/비정상 결과를 커널에 전달
```
NIC
 └─ 체크섬 검사
```

#### TSO (TCP Segmentation Offload)
현재 `tcp-segmentation-offload: on`
- 원래 TCP는 `MTU` 때문에 `64KB 데이터`를 여러 패킷으로 나눠야 한다.
    - `MTU`: **Maximum Transmission Unit**의 약자로, 네트워크 인터페이스가 한 번에 전송할 수 있는 최대 바이트 수
    - 이더넷의 일반적인 MTU는 1500 bytes
    - VPN, 터널링, MPLS 등을 사용할 경우 MTU가 더 작아질 수 있음(ex. 1400, 1300 등)
- 예
```
64KB

↓

1500 Byte
1500 Byte
1500 Byte
...
```
- 원래는 CPU가 패킷 분할을 수행
- TSO 활성화 시
```
CPU
 └─ 큰 데이터 전달

NIC
 └─ 실제 TCP 패킷 분할
```
- CPU 부하 감소
- 고속 네트워크에서 성능 향상

#### GSO(Generic Segmentation Offload)
- 현재 `generic-segmentation-offload: on`
- TSO의 소프트웨어 버전
- TSO를 지원하지 않는 NIC에서도 커널이 큰 패킷 단위로 처리
```
Application
 ↓
Kernel
 ↓
큰 패킷 유지
 ↓
마지막 순간에 분할
```
- 분할 작업은 여전히 CPU가 하지만,
    - 네트워크 스택 내부에서 최대한 늦게
    - 큰 단위로 처리하기 때문에 효율이 좋아짐.

#### GRO (Generic Receive Offload)
- 현재 `generic-receive-offload: on`
- 수신 측 기술로 NIC에서 들어온 패킷을 커널이 하나처럼 묶어서 처리
```
1500
1500
1500
1500
=> 6000 Byte
```
- 인터럽트 감소 및 CPU 사용률 감소

#### SG (Scatter Gather)
- 현재 `scatter-gather: on`
- 원래는 
```
Buffer A
Buffer B
Buffer C
```
- 에 흩어져 있는 데이터를 `큰 버퍼`로 복사한 뒤 전송해야 함
- SG 사용 시 NIC가 A, B, C를 직접 읽어 전송
- 비연속 메모리 조각들을 하나의 논리적 버퍼로 묶어 한 번의 DMA 전송으로 처리하는 기법
- 메모리 복사 감소, CPU 절약

#### VLAN Offload
- 현재 `rx-vlan-offload: on`, `tx-vlan-offload: on`
- VLAN 태그 삽입/제거를 CPU 대신 NIC가 수행
- VLAN 환경에서 CPU 절약

---

`-i` : NIC 커널 드라이버 정보
- 현재 NIC 가 사용 중인 커널 드라이버(driver)와 펌웨어(firmware) 정보를 확인한다.
- 드라이버 문제 분석, 커널 업그레이드 영향 확인, 제조사 드라이버 적용 여부 확인 시 사용한다.
- 성능보다는 호환성 및 장애 분석에 자주 사용된다.

```bash
$ ethtool -i eno1
driver: r8169
version: 7.0.0-28-generic
firmware-version: rtl8168h-2_0.0.2 02/26/15
expansion-rom-version:
bus-info: 0000:02:00.0
supports-statistics: yes
supports-test: no
supports-eeprom-access: no
supports-register-dump: yes
supports-priv-flags: no
```

#### driver
- `driver: r8169` : Realtek RTL8111/8168 계열용 오픈소스 드라이버
- 랜카드를 Linux가 r8169 드라이버로 제어하고 있다는 의미
- 장애 발생 시 가장 먼저 확인하는 항목 중 하나

#### verion
- `version: 7.0.0-28-generic` : 현재 로드된 커널 버전

#### firmware-version
- NIC 내부 펌웨어 버전
- NIC도 작은 임베디드 장치이므로 자체 펌웨어를 가진다.
- 문제 발생 시, 드라이버 버전 + 펌웨어 버전 조합을 보고 제조사 이슈를 확인하기도 한다.

#### bus-info
- `bus-info: 0000:02:00.0` PCIe 장치 주소
```
PCI Bus 02
Device 00
Function 0
```
- 에 위치한 랜카드라는 뜻이다.

#### supports-statistics
- `supports-statistics: yes` : NIC 통계 정보 조회 기능
- 따라서 다음 명령 사용 가능 `ethtool -S eno1`
- 네트워크 장애 분석 때 중요하다
```bash
$ ethtool -S eno1
NIC statistics:
     tx_packets: 218745531
     rx_packets: 535529893
     tx_errors: 0
     rx_errors: 0
     rx_missed: 0
     align_errors: 0
     tx_single_collisions: 0
     tx_multi_collisions: 0
     unicast: 535444395
     broadcast: 55
     multicast: 85443
     tx_aborted: 0
     tx_underrun: 0
```
- 송신 2.1억 패킷, 수신 5.3억 패킷으로 장시간 운용된 서버라면 자연스러운 수치
- `tx_errors: 0`, `rx_errors:0` : 전송, 수신 오류 없음
    - 만약 증가한다면 다음을 의심함
    - 케이블 불량
    - 커넥터 접촉 불량
    - NIC 문제
    - 스위치 포트 문제
    - 드라이버 문제
- `rx_missed: 0` : NIC가 패킷을 받았지만 버퍼 부족 때문에 버린 횟수
    - 예: 패킷 도착 $\rarr$ RX Ring 가득 참 $\rarr$ 패킷 폐기
    - 보통 RX Ring 부족, CPU 과부하를 의미함
- `align_errors: 0` : 이더넷 프레임 형식이 비정상인 경우
    - 케이블 문제, 전기적 노이즈, 하드웨어 문제
- `tx_single_collisions: 0`, `tx_multi_collisions: 0` : 요즘은 거의 0, 과거 Hub 환경에서는 충돌 발생하는 경우가 있으나 현재는 스위치 환경이라 거의 발생하지 않는다.
- `tx_aborted: 0`, `tx_underrun: 0`: 송신 포기, 보낼 데이터가 부족하여 전송 실패
    - 주로 NIC 이상, 드라이버 이상에서 나타남.

#### supports-test
- `supports-test: no` : NIC 자체 진단 테스트 기능 미지원
- 지원하는 드라이버는 `ethtool -t eno1`로 하드웨어 진단 가능하다.

#### supports-eeprom-access
- `supports-eeprom-access: no` : NIC EEPROM 읽기 기능 미지원
- EEPROM에서는 보통 MAC 주소, 제조 정보, 하드웨어 설정 등이 저장된다.

#### supports-register-dump
- `supports-register-dump: yes`
- NIC 레지스터 덤프 가능 : `ethtool -d eno1` 사용 가능

#### supports-priv-flags
- `supports-priv-flags: no`
- 드라이버 전용(private) 옵션 없음
- 지원하는 NIC는 `ethtool --show-priv-flags eno1` 으로 벤더 전용 기능을 조회할 수 있다.


### 실제 장애 분석 예시
#### 1. 케이블 또는 포트 불량
- 증상 : 간헐적 통신 끊김, 속도 저하
- 확인 : `ethtool eno1` $\rarr$ `Speed: 100Mb/s` 로 떨어짐
- `ethtool -S eno1`에서 
    - `rx_errors`, `crc_errors`, `align_errors` 증가

#### 2. 트래픽 폭주
- 증상 : 패킷 손실, 응답 지연
- 확인 : `ethtool -S eno1`에서 
    - `rx_missed`, `rx_dropped` 증가

#### 3. 드라이버 문제
- 증상 : 갑자기 통신 중단
- 확인 : `dmesg | grep eno1` or `journalctl -k` 에서 `link down`, `link up` 반복 확인

#### 4. 스위치 포트 문제
- 증상: 랜선 교체해도 계속 오류
- 확인: `rx_errors` 증가