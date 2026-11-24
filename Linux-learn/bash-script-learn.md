# 쉘 스크립트

> BASH 쉘 스크립트 문법 학습 내용 정리

---

> 실무에서 쓰는 스크립트를 이해해보자.

### 1. 스크립트 선언과 안전장치

```bash
#!/usr/bin/env bash
# 현장 PC 최초 1회 준비: ...
set -euo pipefail
cd "$(dirname "$0")/.."
```

- `#!/usr/bin/env bash` (셔뱅, Shebang)
    - 이 파일을 실행할 때 `bash` 프로그램으로 해석하라는 뜻. `/bin/bash`라고 직접 적지 않고 `env`를 거치면, 시스템마다 `bash` 설치 경로가 달라도 알아서 찾아 실행해줌
- `set -euo pipefail` (엄격 모드 3종)
    - 쉘 스크립트는 기본적으로 중간에 에러가 나도 무시하고 끝까지 실행하는 성질이 있음. 이를 막는 안전장치임.
    - `-e`: 명령어가 하나라고 실패(에러)하면 **즉시 스크립트를 중단** 함.
    - `-u`: 선언하지 않은 **빈 변수를 쓰려고 하면 에러** 를 내고 멈춤(오타 방지)
    - `-o pipefail`: 파이프(`|`)로 여러 명령어를 연결했을 때, 중간 명령어 중 하나라도 실패하면 전체가 실패한 것으로 처리함.
- `cd "$(dirname "$0")/..` (작업 폴더 고정)
    - `$0`: 현재 실행된 스크립트 파일의 경로 (예: `./scripts/host-setup.sh`)
    - `dirname "$0"`: 파일명을 떼고 폴더 경로만 추출 (예: `./scripts`)
    - `"$( ... )`: 괄호 안의 명령어를 실행한 결과 텍스트를 그 자리에 끼워 넣으라는 뜻(명령어 치환)
    - 결국 `cd "./scripts/.."` 즉, 어느 위치에서 이 스크립트를 실행하든 프로젝트 최상위 루트 폴더로 이동하게 만들어 이후의 상대 경로(`.env`, `config/site.yaml`)가 꼬이지 않도록 만든다.

---

### 2. command, >/dev/null, ||

> 필수 프로그램(Docker) 설치 확인

```bash
command -v docker >/dev/null || { echo "✗ Docker 가 필요합니다: ..."; exit 1; }
docker compose version >/dev/null 2>&1 || { echo "✗ docker compose 플러그인이 필요합니다."; exit 1; }
```
- `command -v docker` : `docker`라는 명령어가 시스템에 설치되어 있는지 확인하고 경로를 출력함.
- `>/dev/null` 과 `>/dev/null 2>&1`
    - 화면에 지저분한 출력이 나오지 않게 버리는 문법
    - `/dev/null`은 리눅스의 **블랙홀(휴지통)**. `>`는 일반 출력(표준 출력, 1번)을 그리로 보냄.
    - `2>&1`은 **에러 메시지(표준 에러, 2번)도 일반 출력(1번)이 가는 곳(`/dev/null`)으로 함께 버려라** 는 뜻
- `|| { 명령1; 명령2; }`
    - `A || B`: **"A가 실패하면 B를 실행해라"** 라는 논리 연산. 
    (반대로 `&&` 는 "A가 성공하면 B를 실행해라")
    - `{ ... }`: 여러 명령을 하나로 묶음. 주의할 점은 닫는 중괄호 `}` 앞에 반드시 세미콜론(`;`)이나 줄바꿈이 있어야 함.
    - `exit 1`: 실패 상태 코드(`1`)를 반환하며 스크립트를 즉시 종료함. (리눅스에서 `0`은 성공, `1`은 실패)

---

### 3. if, sed 
> `.env` 설정 파일 자동 생성

```bash
if [ ! -f .env ]; then
  cp .env.example .env
  sed -i "s/^SHARK_UID=.*/SHARK_UID=$(id -u)/; s/^SHARK_GID=.*/SHARK_GID=$(id -g)/" .env
  echo "✓ .env 를 만들었습니다 → ..."
fi
```
- `if [ ! -f .env ]; then ... fi`
    - `[ ... ]` 는 조건문 테스트 기호. (대괄호 안쪽 양옆에 공백이 꼭 있어야 함.)
    - `-f .env`: `.env`라는 파일이 존재하는가?
    - `!`: 부정(NOT)임. 즉 ".env 파일이 아직 없다면" 실행함.
- `sed -i "s/찾을패턴/바꿀내용/" .env
    - `sed`는 파일을 열지 않고 텍스트를 찾아 바꾸는 도구. `-i`(in-place) 옵션은 결과를 화면에 띄우지 않고 원본 파일을 직접 수정함.
    - `^SHARK_UID=.*:`:`^`는 줄의 맨 앞, `.*`는 뒤따르는 모든 글자를 뜻함. 즉 `SHARK_UID=`로 시작하는 줄 전체를 찾음.
    - `$(id -u)`, `$(id -g)`: 현재 리눅스 로그인 계정의 **사용자 ID(UID)** 와 **그룹 ID(GID)** 번호를 가져옴. Docker 컨테이너가 호스트 폴더에 파일을 쓸 때 권한 충돌이 나지 않도록 내 PC 계정 번호를 넣는 작업.
    - 세미콜론(`;`)으로 구분해서 `SHARK_UID` 와 `SHARK_GID` 두 줄을 한 번에 수정

---

### 4. get() , 기본값 문법

> `.env`에서 안전하게 값 읽어오기
```bash
# .env 를 source 하지 않고 값만 읽는다 (비밀번호에 특수문자가 있어도 안전)
get() { grep -E "^$1=" .env | head -1 | cut -d= -f2- | sed 's/[[:space:]]*#.*$//'; }
DATA_DIR="$(get SHARK_DATA_DIR)"; STATE_DIR="$(get SHARK_STATE_DIR)"; MOUNT="$(get SHARK_CAMERA_MOUNT)"
STATE_DIR="${STATE_DIR:-./state}"; MOUNT="${MOUNT:-/mnt/shark_output}"
```

- 왜 `source .env`를 안 할까?
    - 보통은 `source .env`로 변수를 한 번에 불러오지만, 비밀번호에 `$`, `!`, 따옴표 같은 특수문자가 있으면 쉘이 이를 명령어나 변수로 오해해 오류가 나거나 해킹 위험이 생긴다. 그래서 단순 텍스트로 한 줄씩 뜯어오는 `get` 함수를 만든 것
- `get() { ... }` 함수 분석 (파이프라인 `|` 흐름)
    - 함수 안에서 `$1`은 함수에 넘겨준 첫 번째 인자. (예: `get SHARK_DATA_DIR`이면 `$1`은 `SHARK_DATA_DIR`)
    1. `grep -E "^$1=" .env`: `.env`에서 `SHARK_DATA_DIR`으로 시작하는 줄을 찾음.
    2. `| head -1`: 혹시 중복된 줄이 있더라도 맨 첫 번째 줄 1개만 취함.
    3. `| cut -d= -f2-`: `=` 기호를 구분자(`-d=`)로 쪼갠 뒤, 2번째 조각부터 끝까지(`-f2-`) 가져옴. (`-f2`가 아니라 `-f2-`를 쓴 이유는 비밀번호 자체에 `=`가 포함되어 있을 때 잘리지 않게 하기 위해서)
    4. `| sed 's/[[:space:]]*#.*$//'`: 값 뒤에 주석(예: `8080 # 포트번호`)이 달려 있을 경우, 공백(`[[:space:]]`)과 `#`부터 줄 끝(`$`)까지를 빈칸으로 지워 순수 값만 남김.
- `${STATE_DIR:-./state}` (기본값 문법)
    - **파라미터 확장** 이라는 문법
    - "`STATE_DIR` 변수가 비어있거나 설정되지 않았다면(`:-`), 대신 `./state`라는 기본값을 넣어라"라는 뜻

### 5. mkdir -p, [ -d | -z ]

> 폴더 생성 및 환경 사전 점검

```bash
mkdir -p "$DATA_DIR" "$STATE_DIR"
echo "✓ 폴더 준비: $DATA_DIR , $STATE_DIR"

if [ ! -d "$MOUNT/vnir" ]; then
  echo "! 카메라 공유 폴더($MOUNT)가 마운트되어 있지 않은 것 같습니다 ..."
fi
[ -f config/site.yaml ] || { echo "✗ config/site.yaml 이 없습니다."; exit 1; }

if [ -z "$(get SHARK_UI_PASSWORD)" ]; then
  echo "! .env 의 SHARK_UI_PASSWORD 가 비어 있습니다. 설정 후 다시 실행하세요."; exit 1
fi
```

* **`mkdir -p "$DATA_DIR" "$STATE_DIR"`**
  * `-p` 옵션은 두 가지 아주 유용한 역할을 한다: ① 중간 상위 폴더가 없어도 한꺼번에 다 만들어주고, ② **폴더가 이미 존재해도 에러를 내지 않고 조용히 넘어갑니다.**
  * 변수를 `"..."` 큰따옴표로 감싼 이유는 폴더 경로에 띄어쓰기가 있어도 하나의 경로로 인식시키기 위해서입니다. (쉘 스크립트에서 변수엔 항상 따옴표를 붙이는 게 정석입니다.)
* **`[ ! -d "$MOUNT/vnir" ]`**
  * `-d`는 **디렉토리(폴더)가 존재하는지** 검사한다. 앞서 본 `-f`(파일 검사)의 폴더 버전.
  * 여기서는 `exit 1`이 없으므로 경고 메시지만 띄우고 계속 진행한다.
* **`[ -f config/site.yaml ] || { ... }`**
  * `if`문을 한 줄로 줄여 쓴 형태입니다. `config/site.yaml` 파일이 없으면 에러 출력 후 종료한다.
* **`[ -z "$(get SHARK_UI_PASSWORD)" ]`**
  * `-z`는 **문자열의 길이가 0인지(비어있는지)** 확인합니다. (Zero의 z로 기억하면 쉽습니다.)
  * 비밀번호가 비어있으면 안내 문구를 띄우고 종료한다.

### 6. docker compose config -q, hostname -I, 

> Docker 설정 검증 및 다음 단계 안내

```bash
docker compose config -q && echo "✓ compose 설정 검증 완료"
echo "다음: docker compose up -d --build   →   http://$(hostname -I | awk '{print $1}'):$(get SHARK_PORT)"
```

* **`docker compose config -q`**
  * `docker-compose.yml`과 `.env` 파일의 문법에 틀린 곳이 없는지 검사합니다. `-q`(quiet)는 이상 없을 때 전체 설정 내용을 화면에 쫙 출력하지 않고 조용히 검사만 하라는 옵션.
  * `&& echo ...`: 앞의 검사가 성공했을 때만 완료 메시지를 출력한다.
* **`$(hostname -I | awk '{print $1}')`**
  * `hostname -I`: 현재 PC에 할당된 모든 IP 주소를 띄어쓰기로 구분해 출력한다.
  * `awk '{print $1}'`: 공백으로 나뉜 텍스트 중 첫 번째 조각(메인 IP 주소)만 쏙 뽑아옴.
  * 결과적으로 사용자가 바로 복사해서 브라우저에 붙여넣을 수 있는 접속 주소(`http://192.168.0.10:8000` 형태)를 화면에 조립해 보여준다.