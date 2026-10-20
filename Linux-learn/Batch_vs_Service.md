# 배치 vs 서비스

### 배치와 서비스의 핵심 차이

|구분|서비스 (Service / Daemon)| 배치 (Batch Job / 일괄처리)|
|-|-|-|
|핵심 목적|요청에 즉각 응답하거나 상태를 항시 유지|정해진 작업을 몰아서 한 번에 처리하고 끝냄|
|실행 상태 (생명주기)|상시 실행(Long-running) (OS 부팅 시 켜져서 끌 때까지 계속 떠 있음)|일시적 실행 (Trigger & Exit) (트리거되면 시작해서 작업 완료 후 종료)|
|트리거 방식|외부 요청(HTTP, SSH 등), 시스템 이벤트|시간 기반(스케쥴링: 매일 밤 2시 등), 데이터 적재량|
|종료 여부|비정상 종료(Crash)되지 않는 한 종료되지 않음|작업이 끝나면 정상적으로 프로세스가 종료(Exit 0)됨|
|비정상 종료 시|보통 **자동 재시작(Restart)** 되도록 설정함|실패 로그를 남기고 알림을 보냄(필요 시 재시도)|
|대표적인 예시|Nginx, MySQL, SSH 서버, 메시지 브로커(Kafka)|DB 일일 백업, 매시간 로그 압축/삭제, 월말 정산 정기 실행|

- 서비스: 가게의 문지기나 편의점 점원과 같음. 손님이 언제올지 모르기 때문에 24시간 문을 열고 기다림.
- 배치: 가게의 청소 대행업체와 같음. 매일 밤 12시에 와서 청소를 하고 돌아감.

### 사용 방법 및 구현 시 구분 기준

#### A. 서비스로 구현해야 하는 경우
- 조건: 네트워크 포트를 열고 클라이언트 접속을 기다리거나, 시스템 자원을 24시간 감시해야 할 때.
- 관리 도구: `systemd` (일반적)
- 우분투에서의 사용 방식:
    1. `/etc/systemd/system/myService.service` 파일 작성
    ```Ini
    [Unit]
    Description=My API Server
    After=network.target

    [Service]
    ExecStart=/usr/bin/python3 /app/server.py
    # 죽으면 자동으로 재시작
    Restart=always 
    User=www-data

    [Install]
    WantedBy=multi-user.target
    ```
    2. 등록 및 실행
    ```bash
    sudo systemctl daemon-reload # 서비스 파일을 만들거나 고친 뒤에 필요
    sudo systemctl enable myService # 부팅 시 자동 시작
    sudo systemctl start myService # 지금 실행
    sudo systemctl enable --now myService # 위에 두 줄 합친 명령어
    ```

#### B. 배치(Batch)로 구현해야 하는 경우
- 조건: 특정 주기로 대량의 데이터를 수집/가공하거나, 백업/정리 스크립트를 수행하고 프로세스가 끝나야 할 때.
- 관리 도구:
    1. `cron` (가장 전통적이고 대중적임)
    2. `systemd timer` (모던 리눅스 표준 배치 관리 방식)
    ```bash
    crontab -e
    ```
- 내용 작성 예시 (매일 새벽 3시에 백업 스크립트 실행 후 종료):
    ```text
    0 3 * * * /home/ubuntu/scripts/backup.sh >> /var/log/backup.log 2>&1
    ```
- 단발성 서비스(`backup.service`):`Type=oneshot`으로 설정하여 끝나면 바로 종료되도록 함.
    ```ini
    [Service]
    Type=oneshot
    ExecStart=/home/ubunu/scripts/backup.sh
    ```
    - 타이머(`backup.timer`): 실행 주기를 지정
    ```ini
    [Timer]
    OnCalendar=*-*-* 03:00:00 # 매일 새벽 3시
    Persistent=true

    [Install]
    WantedBy=timers.target
    ```

#### 햇갈리기 쉬운 경계 사례 (Worker/Consumer 등)
- 질문 : "메시지 큐(RabbitMQ, Kaffa 등)에서 데이터를 100건씩 묶어서 (배치로) 처리하는 워커는 서비스인가요, 배치인가요?
    - 답변: '배치 처리 로직'을 담은 서비스
    - 데이터 처리는 묶음 단위(배치)로 하지만, 프로그램 자체는 계속 살아있으면서 큐를 지속적으로 감시(Listening)해야 하므로 프로세스 관리 관점에서는 서비스로 등록하여 `Restart=always` 옵션을 넣어 운영해야 함.

## systemd 서비스 파일 작성법

### 0. 기본 개념

#### 유닛(Unit)이란?
- `systemd`가 관리하는 모든 대상의 단위. 확장자로 종류를 구분함.
    - `.service` (프로세스), `.timer` (스케쥴), `.target` (유닛 묶음/부팅 단계), `.socket`, `.mount` 등

#### 파일 위치 (위쪽일수록 우선순위 높음)
|경로|용도|
|-|-|
|`/etc/systemd/system/`|관리자가 직접 작성하는 서비스(**직접 만드는 서비스는 여기**)|
|`/run/systemd/system/`|런타임 생성 (재부팅 시 사라짐)|
|`/lib/systemd/system/`|apt 등 패키지가 설치한 서비스 (직접 수정 X)|
|`~/.config/systemd/user/`|사용자 서비스 (`systemctl --user`로 관리, 로그인 세션에 종속)|

#### 기본 문법 규칙
- `[섹션]` 아래에 `Key=Value` 형식으로 작성.
- 주석은 **줄 맨 앞**의 `#` 또는 `;`만 인정됨. 값 뒤에 붙인 주석은 값의 일부로 읽혀 오류가 남.
- `Environment=`, `ExecStartPre=` 등 일부 키는 여러 번 쓰면 누적됨.
- 경로는 절대경로로 작성.

#### 의존성과 순서 개념
- 기준: **A = 지금 작성하는 서비스 파일**, B = 그 안에 적는 대상 유닛

|구분|키|의미|
|-|-|-|
|의존성 (켤지 말지)|`Wants=`, `Requires=`|A를 켤 때 B도 같이 켠다 (순서는 정하지 않음 $\rarr$ 동시 시작)|
|순서 (언제 켤지)|`After=`, `Before=`|B가 다 켜진 다음에 A를 켠다 (B를 켜주지는 않음)|

- `Wants=`만 쓰면: B는 켜지지만 A와 동시에 시작됨 → A가 B 준비 전에 실행될 수 있음.
- `After=`만 쓰면: B를 아무도 안 켜면 기다릴 대상이 없어서 A가 바로 시작됨.
- 그래서 "B를 반드시 켜고, B 준비가 끝난 뒤 A 실행"이 필요하면 **`Wants=` + `After=`를 같이 씀**.
    - 예: `Wants=network-online.target` + `After=network-online.target`
    - `network-online.target`은 기본적으로 아무도 켜지 않는 타깃이라 `After=`만 쓰면 대기 효과가 없음.
- 두 개념을 분리한 이유: 기본은 전부 병렬로 켜서 부팅을 빠르게 하고, 꼭 필요한 곳에만 순서를 지정하기 위함.

```
① Wants=B 만          ② After=B 만               ③ Wants=B + After=B
                      (아무도 B를 안 켜는 경우)

  A ████████            A ████████                 B ████
  B ████████            B (실행 안 됨)              A      ████████
  ↑ 동시 시작           ↑ 기다릴 대상이 없어           ↑ B가 확실히 켜지고,
  A가 B 준비 전에         A가 바로 시작                 B 준비 완료 후 A 시작
  실행될 수 있음
  ```

`network-online.target`이 대표 예시인 이유

`network-online.target`은 기본적으로 아무도 켜지 않는 수동형 타깃. 그래서 다음과 같이 됨.

- `After=network-online.target`만 쓰면: 이 타깃이 부팅 작업 목록에 없으니 기다릴 게 없어서 즉시 실행됨. 네트워크 대기 효과가 사실상 없음.
- `Wants=`를 추가하면: 이 타깃이 활성화되면서 `NetworkManager-wait-online` 같은 “IP 잡힐 때까지 기다리는” 서비스가 실제로 돌고, `After=` 덕분에 그게 끝난 뒤 `A`가 시작됩니다.



---

### 1. [Unit] 섹션
- 서비스 종류와 상관없이 모든 유닛에 공통으로 쓰는 섹션
- 설명, 의존성, 실행 순서, 실행 조건을 정의함.

|인자|의미|예시|
|-|-|-|
|`Description=`|서비스 설명. `systemctl status`와 로그에 표시됨|`Description=RiverQ Service`|
|`Documentation=`|관련 문서 위치|`Documentation=https://...`|
|`After=`|나열한 유닛이 **시작 완료된 뒤**에 실행|`After=network-online.target`|
|`Before=`|나열한 유닛보다 **먼저** 실행|`Before=nginx.service`|
|`Wants=`|같이 시작 요청 (약한 의존). 상대가 실패해도 나는 실행됨|`Wants=network-online.target`|
|`Requires=`|같이 시작 (강한 의존). 상대가 실패하거나 중지되면 나도 중지됨|`Requires=postgresql.service`|
|`BindsTo=`|`Requires`보다 강함. 상대가 갑자기 사라져도 나도 중지됨 (USB 장치 등)|`BindsTo=dev-ttyUSB0.device`|
|`PartOf=`|상대를 stop/restart하면 나도 같이 stop/restart|`PartOf=myapp.target`|
|`Conflicts=`|동시에 실행될 수 없음. 하나가 켜지면 다른 하나는 꺼짐|`Conflicts=old-app.service`|
|`ConditionPathExists=`|해당 경로가 없으면 조용히 건너뜀 (실패로 처리 안 함)|`ConditionPathExists=/opt/app/config.yaml`|
|`StartLimitIntervalSec=`<br>`StartLimitBurst=`|N초 안에 M번 넘게 재시작하면 포기함 (기본 10초/5회). `0`이면 제한 없음. **[Service]가 아니라 [Unit]에 써야 함**|`StartLimitIntervalSec=0`|
|`OnFailure=`|최종 실패 시 실행할 유닛 (알림 발송 등)|`OnFailure=notify-fail@%n.service`|

- 자주 쓰는 target
    - `network.target`: 네트워크 장치가 준비됨 (IP 할당은 보장 안 됨). 서버가 포트를 여는 용도면 충분함.
    - `network-online.target`: IP가 할당된 온라인 상태. 외부로 접속하는 프로그램(CCTV, DB, API 클라이언트)이면 이걸 씀.
    - `multi-user.target`: 일반 부팅이 완료된 상태 (CLI 기준).
    - `graphical.target`: 로그인 화면까지 뜬 상태. **사용자 데스크톱 세션이 준비됐다는 뜻은 아님.**


---

### 2. [Service] 섹션
- `.service` 유닛에만 있는 섹션. 실제 프로세스 실행 방법을 정의함.

#### 2-1. 실행 유형 (`Type=`)
- systemd가 "시작 완료"를 언제로 판단할지 결정함.
- `After=`로 이 서비스를 기다리는 다른 서비스의 실행 시점에도 영향을 줌.

|Type|시작 완료로 판단하는 시점|용도|
|-|-|-|
|`simple` (기본값)|프로세스를 띄운 즉시|일반적인 상시 실행 프로그램|
|`exec`|실행 파일이 실제로 exec된 직후 (실행 파일이 없으면 바로 실패로 잡힘)|`simple`보다 엄격하게 확인하고 싶을 때|
|`forking`|부모 프로세스가 fork 후 종료됐을 때|전통적인 데몬 (구형 nginx, apache 등). `PIDFile=` 같이 지정|
|`oneshot`|프로세스가 **종료됐을 때**|배치, 초기화 스크립트|
|`notify`|프로그램이 `sd_notify("READY=1")`을 보냈을 때|준비 완료 시점을 프로그램이 직접 알림|
|`idle`|다른 job이 다 끝난 뒤 실행|부팅 로그와 출력이 섞이지 않게 할 때 (드묾)|

#### 2-2. 실행 명령
|인자|의미|
|-|-|
|`ExecStart=`|실행할 명령 (필수). **셸을 거치지 않음**: `|`, `>`, `&&`, `*` 등은 해석되지 않음. 필요하면 `ExecStart=/bin/bash -c "명령 | 명령"`|
|`ExecStartPre=` / `ExecStartPost=`|본 실행 전/후에 실행할 명령. 여러 줄 가능. 앞에 `-`를 붙이면 실패해도 무시 (`ExecStartPre=-/bin/mkdir -p /var/run/app`)|
|`ExecReload=`|`systemctl reload` 시 실행할 명령 (예: `/bin/kill -HUP $MAINPID`)|
|`ExecStop=`|중지 시 실행할 명령. 생략하면 SIGTERM을 보냄|
|`RemainAfterExit=`|`oneshot`이 끝난 뒤에도 "active" 상태로 표시할지 (초기화 작업용)|

#### 2-3. 실행 환경
|인자|의미|
|-|-|
|`User=` / `Group=`|실행할 계정. 생략하면 **root로 실행**되므로 가급적 지정|
|`WorkingDirectory=`|작업 디렉터리. 프로그램이 상대경로로 설정 파일이나 모델을 읽는다면 필수|
|`Environment=`|환경변수 (`Environment="KEY=value"`). 여러 줄 가능|
|`EnvironmentFile=`|환경변수 파일 경로. API 키 등을 서비스 파일과 분리할 때 사용 (`-`를 붙이면 파일이 없어도 무시)|
|`UMask=`|생성 파일 권한 마스크|

- systemd 서비스는 `.bashrc`, `.profile`을 읽지 않음. 터미널에서는 되는데 서비스로는 안 되는 문제의 대부분이 PATH나 환경변수 차이 때문임.

#### 2-4. 재시작 정책
- `Restart=`: 어떤 상황에서 재시작할지 지정.

|Restart 값|정상 종료(exit 0)|에러 종료(exit≠0)|시그널로 죽음(segfault 등)|타임아웃/워치독|
|-|-|-|-|-|
|`no` (기본값)|-|-|-|-|
|`always`|O|O|O|O|
|`on-failure`|-|O|O|O|
|`on-abnormal`|-|-|O|O|
|`on-abort`|-|-|O|-|
|`on-success`|O|-|-|-|

- 상시 실행 서비스는 `always`, 일 끝나면 종료되는 프로그램은 `on-failure`가 일반적임.
- `RestartSec=`: 재시작 전 대기 시간 (기본 100ms). 너무 짧으면 재시작 폭주가 일어나 위의 StartLimit에 걸림. 보통 5~10초.
- `systemctl stop`으로 직접 끈 경우에는 `always`여도 재시작하지 않음.

#### 2-5. 시작/종료 제어
|인자|의미|
|-|-|
|`TimeoutStartSec=`|시작 완료까지 허용 시간 (기본 90초). 초과하면 실패 처리|
|`TimeoutStopSec=`|stop 시 SIGTERM 후 기다리는 시간 (기본 90초). 초과하면 SIGKILL로 강제 종료|
|`KillMode=`|종료 대상. `control-group`(기본값, 자식 프로세스 포함 전부) / `mixed` / `process`(메인만)|
|`KillSignal=`|종료 시 보낼 시그널 (기본 SIGTERM). 앱이 SIGINT에서만 정리 작업을 한다면 `SIGINT`로 지정|

#### 2-6. 로그
|인자|의미|
|-|-|
|`StandardOutput=` / `StandardError=`|출력 위치. 기본값은 `journal`. `append:/var/log/app.log`처럼 파일 지정도 가능|
|`SyslogIdentifier=`|로그 태그 이름 (`journalctl -t 이름`으로 필터링)|

- Python은 출력 버퍼링 때문에 로그가 늦게 찍힘.
    - `Environment="PYTHONUNBUFFERED=1"` 또는 `python3 -u` 사용.

#### 2-7. 리소스 제한
|인자|의미|
|-|-|
|`LimitNOFILE=`|열 수 있는 파일/소켓 수 한도 (기본 soft 1024)|
|`MemoryMax=`|메모리 상한. 초과하면 OOM으로 종료 (메모리 누수 방어)|
|`CPUQuota=`|CPU 사용률 상한 (`CPUQuota=200%` = 코어 2개분)|
|`Nice=`|CPU 스케줄링 우선순위 (-20 ~ 19, 높을수록 양보)|

#### 2-8. 헬스체크 / 보안 (선택)
|인자|의미|
|-|-|
|`WatchdogSec=`|프로그램이 이 시간 안에 `sd_notify("WATCHDOG=1")`을 안 보내면 멈춘 것으로 보고 재시작. **프로세스는 살아 있는데 멈춘(hang) 상태**를 잡을 때 사용|
|`NoNewPrivileges=yes`|프로세스가 권한 상승(sudo 등)을 못 하게 막음|
|`ProtectSystem=full`|`/usr`, `/etc` 등을 읽기 전용으로 마운트|
|`PrivateTmp=yes`|서비스 전용 `/tmp` 사용|

---

### 3. [Install] 섹션: 
> `enable` 했을 때 부팅 어디에 끼워 넣을 것인가

- **`systemctl enable`/`disable` 할 때만 읽힘.** 서비스 실행 중에는 아무 영향이 없음.
- `[Install]`이 없으면 enable할 수 없음 (`static` 상태). 다른 유닛이 불러줄 때만 실행됨.

|인자|의미|
|-|-|
|`WantedBy=`|어느 target에 붙일지. **가장 많이 씀**|
|`RequiredBy=`|`WantedBy`의 강한 버전 (Requires 관계로 붙임)|
|`Alias=`|별칭 (`systemctl start 별칭`으로도 실행 가능)|
|`Also=`|이 유닛을 enable할 때 같이 enable할 유닛|

- `enable`의 실제 동작은 심볼릭 링크 생성임.
```bash
    $ sudo systemctl enable myService
    Created symlink /etc/systemd/system/multi-user.target.wants/myService.service
                  → /etc/systemd/system/myService.service
```
    - 부팅 중 `multi-user.target`에 도달하면 `.wants/` 폴더 안의 유닛들을 같이 켜는 구조임.

- WantedBy 선택 기준

|값|용도|
|-|-|
|`multi-user.target`|일반 서버/백그라운드 서비스 (대부분 이것)|
|`graphical.target`|디스플레이 매니저 단계에 붙일 때 (GUI 앱이라도 사용자 세션이 필요하면 사용자 서비스 + `graphical-session.target` 권장)|
|`timers.target`|`.timer` 유닛|
|`default.target`|사용자 서비스(`--user`)의 기본값|

- 주의: `After=graphical.target` + `WantedBy=graphical.target`처럼 **같은 target에 "뒤에 실행"과 "붙이기"를 동시에 걸면 순서 순환(ordering cycle)이 발생함.** 타깃은 자기가 Wants하는 유닛이 끝난 뒤에 완료되도록 자동 설정되기 때문임.

---

### 4. 실전 템플릿 (상시 실행 서비스)

```ini
[Unit]
Description=My Data Collector
# 외부로 접속하므로 IP 할당까지 대기
Wants=network-online.target
After=network-online.target
# 재시작 횟수 제한 해제 (현장 장비에서 영구 포기 방지)
StartLimitIntervalSec=0

[Service]
Type=simple
User=appuser
WorkingDirectory=/opt/myapp
EnvironmentFile=-/opt/myapp/.env
Environment="PYTHONUNBUFFERED=1"
ExecStart=/opt/myapp/venv/bin/python main.py

Restart=always
RestartSec=10
TimeoutStopSec=15

LimitNOFILE=65536
SyslogIdentifier=myapp

[Install]
WantedBy=multi-user.target
```

### 5. 작성 → 적용 → 확인 명령어

```bash
# 문법/경로 오류 검사
sudo systemd-analyze verify /etc/systemd/system/myapp.service

# 서비스 파일 변경 사항 반영 (파일을 만들거나 고칠 때마다 필수)
sudo systemctl daemon-reload

# 부팅 자동 시작 등록 + 즉시 실행
sudo systemctl enable --now myapp

# 상태 확인 / 재시작 / 중지
systemctl status myapp
sudo systemctl restart myapp
sudo systemctl stop myapp

# 로그 확인 (-f 실시간, -b 이번 부팅 이후, --since 시간 지정)
journalctl -u myapp -f
journalctl -u myapp -b --since "10 min ago"

# 실제 적용된 최종 설정 확인
systemctl cat myapp
systemctl show myapp -p Restart,User,LimitNOFILE

# 패키지가 설치한 서비스는 원본을 고치지 말고 덮어쓰기(drop-in)로 수정
sudo systemctl edit nginx   # /etc/systemd/system/nginx.service.d/override.conf 생성
```

### 6. 서비스 vs 배치 설정 비교 요약

|항목|상시 서비스|배치 (oneshot + timer)|
|-|-|-|
|`Type=`|`simple` / `notify`|`oneshot`|
|`Restart=`|`always`|보통 없음 (실패 시 `OnFailure=`로 알림)|
|`[Install]`|`WantedBy=multi-user.target`|service에는 없음. timer에 `WantedBy=timers.target`|
|enable 대상|`myapp.service`|`backup.timer`|
|다음 실행 확인|-|`systemctl list-timers`|