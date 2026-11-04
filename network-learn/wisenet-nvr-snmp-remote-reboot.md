# Wisenet NVR 원격 장애 진단·재부팅 가이드

> 대상: 한화 Wisenet XRN 시리즈 NVR (XRN-820S에서 확인)
> 작성일: 2026-11-04 (현장 장애 대응 결과 반영)
> 목적: 현장 NVR이 멈췄을 때 현장 PC(Ubuntu)에서 원격으로 진단하고 재부팅하는 방법, 그리고 원격 복구의 한계 공유

---

## 0. 요약

| 복구 경로 | 사전 조건 | 검증 결과 |
|---|---|---|
| ① SUNAPI 재부팅 | 웹 CGI 정상 | 웹 CGI가 멈춘 장애에서는 **사용 불가** |
| ② **SNMP 재부팅** | NVR에 SNMP v3를 **미리** 활성화 | 정상 장비에서 **재부팅 확인**. 웹 CGI가 멈춘 장애에서는 미검증 |
| ③ ONVIF 재부팅 | ONVIF 활성 (기본값) | 웹 CGI가 멈춘 장애에서 **명령은 접수됐지만 재부팅이 실행되지 않음** |
| ④ **전원 리셋** | 현장 방문 또는 원격 전원 장치 | 최종 수단 |

핵심 교훈:

1. **SNMP는 장애가 나기 전에 미리 켜 둬야 합니다.** 웹 UI가 멈추면 SNMP를 새로 켤 수 없습니다.
2. **재부팅 명령이 "접수"됐다고 실제로 재부팅된 것은 아닙니다.** 반드시 RTSP가 끊겼다가 돌아오는 구간이 있는지 확인하세요 (5절).
3. 내부 시스템 프로세스까지 멈춘 장애는 원격 소프트웨어로 복구할 수 없습니다. **원격 전원 리셋 장치를 함체 표준 구성에 넣을 것을 권장합니다.**
4. **장비는 IP가 아니라 MAC 주소나 시리얼 번호로 식별하세요.** 여러 현장이 같은 IP 대역을 쓰면 다른 장비를 같은 장비로 착각할 수 있습니다 (7절).

---

## 1. 장애 진단

### 1.1 상태 감시 루프

장애가 의심되거나 재부팅 명령을 보낼 때는 별도 터미널에서 이 루프를 먼저 실행하세요.

```bash
IP=<NVR_IP>; PORT=8000      # 웹 포트가 다르면 수정
while true; do
  root=$(curl -s -o /dev/null -w "%{http_code}" --max-time 3 http://$IP:$PORT/)
  cgi=$(curl -s -o /dev/null -w "%{http_code}/%{time_total}s" --max-time 5 \
        "http://$IP:$PORT/stw-cgi/system.cgi?msubmenu=deviceinfo&action=view")
  rtsp=$(timeout 2 bash -c "</dev/tcp/$IP/558" 2>/dev/null && echo up || echo down)
  echo "$(date +%T) root=$root cgi=$cgi rtsp=$rtsp"; sleep 2
done
```

> ⚠️ URL은 **반드시 따옴표로 감싸세요.** 따옴표가 없으면 URL 안의 `&`를 쉘이 백그라운드 실행 기호로 해석해서, 요청이 중간에 잘린 채 전송됩니다.

### 1.2 결과 해석

| root (웹 첫 페이지) | cgi (SUNAPI) | rtsp (영상) | 판단 |
|---|---|---|---|
| 401 | 401 | up | **정상** |
| 401 | `000/5.0s` (시간 초과) | up | **SUNAPI 멈춤.** 웹은 열리지만 로그인 후 무응답 |
| 000 | 000 (즉시) | down | 재부팅 중이거나 장비 다운 |
| 000 | 000 | up | 웹 포트가 틀렸거나 중간 경로에서 막힘 → 포트 확인 |

`000`은 "연결 실패"와 "응답 시간 초과" 모두에서 나옵니다. 그래서 `time_total`도 함께 봐야 합니다. 시간 제한(5초)에 정확히 걸렸다면 연결은 됐지만 응답이 없는 **멈춤** 상태입니다.

### 1.3 포트 정보

| 포트 | 용도 | 비고 |
|---|---|---|
| TCP 8000 | 웹 / SUNAPI / ONVIF (HTTP) | `https://`로 접속하면 TLS 오류 |
| TCP 443 | 웹 (HTTPS) | |
| TCP 558 | RTSP | 554 아님 |
| UDP 161 | SNMP | TCP 스캔으로는 확인 불가 → `sudo nmap -sU -p 161` |
| TCP 22 / 23 / 4520 | SSH / Telnet / 장치 포트 | 확인한 장비에서는 모두 닫혀 있음 |

---

## 2. 경로 ①: SUNAPI 재부팅 (웹 CGI가 정상일 때)

```bash
curl --digest -u admin --max-time 30 \
  "http://<NVR_IP>:8000/stw-cgi/system.cgi?msubmenu=power&action=control&Mode=Reboot"
```

웹 CGI가 멈춘 상태에서는 타임아웃만 나므로, 반복해서 시도하지 마세요.

---

## 3. 경로 ②: SNMP

### 3.1 SNMP 개념 요약

| 용어 | 의미 |
|---|---|
| Manager / Agent | 상태를 묻는 쪽(현장 PC) / 장비 안에서 응답하는 프로그램(NVR) |
| MIB / OID | 장비가 제공하는 항목 목록 / 각 항목의 숫자 주소 |
| GET / SET / Trap | 조회 / 변경 / 장비가 먼저 보내는 알림 |

버전은 **v3(인증 + 암호화)** 를 사용합니다.

### 3.2 NVR 설정 (정상일 때 미리)

NVR 웹 UI의 네트워크 메뉴 아래 SNMP 항목에서 설정합니다.

1. **SNMP v3 사용** 체크, 사용자 `admin`
2. 비밀번호: **영문과 숫자만, 8자 이상**

   > ⚠️ **특수문자(`!` 등)를 넣으면 SNMP 인증이 실패합니다.** 웹 UI에서는 정상적으로 저장되기 때문에 원인을 찾기 어렵습니다.

3. 재부팅 기능을 쓰려면 **쓰기(SET) 권한**을 허용
4. 저장 후 SNMP를 껐다가 다시 켜서 확실히 적용

확인된 인증 조합: **`authPriv` / 인증 SHA-256 / 암호화 AES**, 인증·암호화 비밀번호는 같은 값

### 3.3 현장 PC 설정

```bash
sudo apt install -y snmp
mkdir -p ~/.snmp && chmod 700 ~/.snmp
nano ~/.snmp/snmp.conf
```

```
defVersion        3
defSecurityLevel  authPriv
defSecurityName   admin
defAuthType       SHA-256
defAuthPassphrase <SNMP_비밀번호>
defPrivType       AES
defPrivPassphrase <SNMP_비밀번호>
```

```bash
chmod 600 ~/.snmp/snmp.conf
snmpwalk <NVR_IP> 1.3.6.1.2.1.1      # 연결 확인
```

> 비밀번호를 명령줄에 직접 입력했다면 `history | grep <일부>` → `history -d <줄번호>` → `history -w`로 지우세요.

### 3.4 연결 문제 해결

| 오류 | 원인 |
|---|---|
| `Timeout` | SNMP 비활성(포트 `closed`), 설정 파일 누락, 접근 허용 IP 문제 |
| `Unknown user name` | 사용자명 오류 |
| `authorizationError` (인증 없이 요청 시) | 사용자명은 맞음. 인증 정보만 맞추면 됨 |
| `Authentication failure` | 비밀번호 또는 인증 방식 불일치. **모든 방식이 실패하면 비밀번호 문제** (특수문자 확인) |
| `Decryption error` | 암호화 비밀번호 또는 암호화 방식 불일치 |

설정 파일 없이 SNMP 에이전트가 살아 있는지만 확인하는 방법:

```bash
snmpget -v3 -l noAuthNoPriv -u testxyz -r 1 -t 3 <NVR_IP> 1.3.6.1.2.1.1.1.0
# "Unknown user name" → 에이전트 살아 있음 / "Timeout" → 응답 없음
```

### 3.5 주요 OID

```
B = 1.3.6.1.4.1.36849.1.9      (36849 = 한화 기업 번호)
```

**실제 장비로 확인된 항목**

| OID | 이름 | 예시 값 | 권한 |
|---|---|---|---|
| `B.1.0` | 모델명 | XRN-820S | RO |
| `B.2.1.1.0` | 펌웨어 버전 | 5.30.72_231107202437 | RO |
| `B.2.1.2.0` | NVR 시각 | 2026-11-04 07-34-09 | RW |
| `B.2.1.3.0` | **reboot** | NO | **RW** |
| `B.2.1.4.0` | **factoryReset** ⚠️ | NO | **RW** |
| `B.2.1.5.0` | 네트워크 인터페이스 수 | 2 | RO |
| `B.2.1.6.0` / `B.2.1.7.0` | 알람 입력 / 출력 수 | 4 / 2 | RO |
| `B.2.1.9.0` | 시리얼 번호 | | RO |
| `B.2.2.1.N.0` | 채널별 영상 방식 | NTSC | RW |
| `B.2.2.2.N.0` | 채널별 오디오 코덱 | UNKNOWN (오디오 미사용) | RO |
| `B.3.1.1.0` | coldPowerOnDate | 2026-11-04 08-04-46 | RO |
| `B.3.1.2.0` | warmPowerOnDate | | RO |
| `B.3.1.3.0` | shutDownDate | | RO |
| `B.3.1.4.0` | abnormalStartDate | | RO |
| `1.3.6.1.2.1.1.3.0` | sysUpTime (SNMP 에이전트 가동 시간) | | RO |
| `1.3.6.1.2.1.25.1.1.0` | hrSystemUptime (**OS 전체** 가동 시간) | | RO |

> ⏰ **NVR 시각은 UTC로 표시됩니다.** 한국 시간으로 보려면 9시간을 더하세요.

**MIB 가이드 기준 감시 후보** (위치는 장비에서 재확인 필요)

| 경로 | 항목 | 정상 값 | 경보 조건 |
|---|---|---|---|
| `B.3.2.N.0` | 채널별 영상 상태 | On | Vloss |
| `B.3.3.1.0` | 녹화 상태 | On | Off / Fail |
| `B.3.3.2.0` | 팬 상태 | OK | Fail |
| `B.6.N.*` | HDD 상태 | Installed / Not Full | 미인식 또는 고장 |
| `B.8.*` | RAID 상태 | Active | Degraded / Fail |

> MIB 가이드의 HDD 항목은 값 설명에 오기가 있습니다. 실제 장비가 돌려주는 값을 기준으로 판단하세요.

### 3.6 SNMP 재부팅

> ⚠️ **reboot(`B.2.1.3.0`) 바로 옆 항목(`B.2.1.4.0`)이 공장 초기화입니다.** 숫자 하나만 잘못 입력해도 원격 현장 NVR의 설정이 모두 지워집니다. OID를 직접 입력하지 말고 반드시 아래 스크립트로만 실행하세요.

`~/nvr-reboot.sh`

```bash
#!/bin/bash
# 사용법: ./nvr-reboot.sh <NVR_IP>
# OID 고정 — factoryReset(…2.1.4.0) 오입력 방지
set -e
IP=${1:?usage: nvr-reboot.sh <NVR_IP>}

echo "[대상 확인]"
snmpget "$IP" 1.3.6.1.4.1.36849.1.9.1.0       # 모델명
snmpget "$IP" 1.3.6.1.4.1.36849.1.9.2.1.1.0   # 펌웨어
snmpget "$IP" 1.3.6.1.4.1.36849.1.9.2.1.9.0   # 시리얼 번호
snmpget "$IP" 1.3.6.1.2.1.25.1.1.0            # 현재 OS 가동 시간

read -p "위 장비를 재부팅합니다. 계속할까요? (yes 입력): " ans
[ "$ans" = "yes" ] || { echo "취소"; exit 1; }

snmpset "$IP" 1.3.6.1.4.1.36849.1.9.2.1.3.0 s "OK"
echo "재부팅 명령 전송. 5절의 방법으로 실제 재부팅 여부를 확인하세요."
```

**재부팅 값은 `"OK"`입니다.** `"YES"`는 `wrongLength`로 거부됩니다. MIB 가이드에 적힌 "GMT+hh:mm"는 오기로 보입니다.

SNMP 재부팅은 `coldPowerOnDate`가 갱신되는 콜드부팅으로 기록됩니다.

---

## 4. 경로 ③: ONVIF 재부팅

SNMP를 켜지 않은 장비도 ONVIF가 살아 있으면 재부팅 명령을 보낼 수 있습니다. 다만 **명령이 접수돼도 실제로는 실행되지 않을 수 있습니다** (6절 사례 참고).

### 4.1 ONVIF 응답 확인 (인증 불필요)

```bash
curl -s --max-time 10 -X POST "http://<NVR_IP>:8000/onvif/device_service" \
  -H 'Content-Type: application/soap+xml' \
  -d '<?xml version="1.0"?><s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope"><s:Body><GetSystemDateAndTime xmlns="http://www.onvif.org/ver10/device/wsdl"/></s:Body></s:Envelope>' | head -c 300; echo
```

XML이 돌아오면 ONVIF가 살아 있는 것입니다. 확인한 장비에서는 80번 포트는 응답이 없었고 **8000번 포트**에서 응답했습니다.

### 4.2 스크립트: `~/onvif.sh`

ONVIF 표준 인증(WS-Security, PasswordDigest)을 사용합니다.

```bash
#!/bin/bash
# 사용법: ./onvif.sh <IP:PORT> info|reboot
set -e
TARGET=${1:?usage: onvif.sh <IP:PORT> info|reboot}; ACTION=${2:?info|reboot}
case $ACTION in
  info)   BODY='<GetDeviceInformation xmlns="http://www.onvif.org/ver10/device/wsdl"/>' ;;
  reboot) BODY='<SystemReboot xmlns="http://www.onvif.org/ver10/device/wsdl"/>' ;;
  *) echo "info|reboot"; exit 1 ;;
esac
read -sp "admin 비밀번호: " PW; echo
[ "$ACTION" = reboot ] && { read -p "$TARGET 재부팅합니다. yes 입력: " a; [ "$a" = yes ] || exit 1; }

N=$(mktemp); openssl rand 16 > "$N"
NONCE=$(base64 -w0 "$N")
CREATED=$(date -u +%Y-%m-%dT%H:%M:%SZ)
DIGEST=$( (cat "$N"; printf '%s%s' "$CREATED" "$PW") | openssl sha1 -binary | base64 -w0 )
rm -f "$N"

curl -s --max-time 20 -X POST "http://$TARGET/onvif/device_service" \
 -H 'Content-Type: application/soap+xml; charset=utf-8' -d "<?xml version=\"1.0\"?>
<s:Envelope xmlns:s=\"http://www.w3.org/2003/05/soap-envelope\"><s:Header>
<Security s:mustUnderstand=\"1\" xmlns=\"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd\"><UsernameToken>
<Username>admin</Username>
<Password Type=\"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest\">$DIGEST</Password>
<Nonce EncodingType=\"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary\">$NONCE</Nonce>
<Created xmlns=\"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd\">$CREATED</Created>
</UsernameToken></Security></s:Header><s:Body>$BODY</s:Body></s:Envelope>"
echo
```

### 4.3 사용 순서

```bash
chmod +x ~/onvif.sh
~/onvif.sh <NVR_IP>:8000 info      # 1) 인증 확인 (모델, 펌웨어 출력)
~/onvif.sh <NVR_IP>:8000 reboot    # 2) 재부팅 → "Rebooting in 30 seconds." 응답
```

- `NotAuthorized` 오류: 비밀번호가 틀렸거나 PC와 NVR의 시각 차이가 큰 경우입니다.
- **응답이 왔더라도 반드시 5절의 방법으로 실제 재부팅 여부를 확인하세요.**

---

## 5. 재부팅 실행 검증 (모든 경로 공통)

재부팅 명령을 보내기 **전에** 1.1의 감시 루프를 실행해 두고, 다음을 확인합니다.

| 관찰 결과 | 판단 | 조치 |
|---|---|---|
| root와 rtsp가 1분 정도 `000`/`down`이었다가 복귀하고, 이후 `cgi=401` | **재부팅 후 정상 복구** | 완료 |
| down 구간은 있었는데, 복귀 후에도 `cgi=000/5.0s` | **부팅하자마자 다시 멈춤** | 현장 점검 (HDD 등, 8절) |
| root=401, rtsp=up이 계속 유지됨 | **재부팅이 실행되지 않음** | 명령 반복 금지, 전원 리셋 |

**추가 확인 방법 (SNMP가 켜져 있을 때)**

```bash
snmpget <NVR_IP> 1.3.6.1.2.1.25.1.1.0           # OS 가동 시간이 수 분 이내로 초기화됐는지
snmpget <NVR_IP> 1.3.6.1.4.1.36849.1.9.3.1.1.0  # coldPowerOnDate가 명령 시각(UTC)으로 바뀌었는지
```

> 핑만으로는 판단하지 마세요. SNMP 재부팅 시험에서 RTSP는 67초간 중단됐지만, 핑은 120개 중 1개만 유실됐습니다.

---

## 6. 사례 기록 (2026-11-04)

### 6.1 NVR-A: SUNAPI 멈춤 → 원격 복구 실패

- 현장 PC: `MINIPC-PN42`
- NVR: 192.168.2.200, MAC `E4:30:22:F1:BB:57`, 펌웨어 5.34.42
- SNMP: **비활성**

| 시각 (KST) | 내용 |
|---|---|
| 오전 | 웹 UI 로그인 후 무응답. `root=401`, SUNAPI 시간 초과 확인. SUNAPI 재부팅 시도 → 타임아웃 |
| (재부팅 경위 미상) | 일시 복구 |
| 17:2x | **같은 증상 재발.** SUNAPI 시간 초과 |
| 17:28 | SNMP 시도 → UDP 161 `closed` (SNMP 비활성) |
| 17:3x | ONVIF 8000번 포트 응답 확인 → `GetDeviceInformation` 인증 성공 → `SystemReboot` 응답 **"Rebooting in 30 seconds."** |
| 17:36 ~ 17:39 | 감시 결과 root=401, rtsp=up이 계속 유지되고 cgi는 시간 초과 → **재부팅이 실행되지 않음.** ONVIF 재부팅을 반복해도 결과 동일 |
| 결론 | 원격 경로 모두 실패 → **현장 전원 리셋 필요** |

**분석**: ONVIF 서비스는 살아 있어서 요청을 접수하지만, 실제 재부팅 처리는 멈춘 내부 시스템 관리 프로세스에 넘겨지는 구조로 보입니다. 이 경우 SNMP를 켜 뒀더라도 같은 이유로 재부팅이 실행되지 않았을 가능성이 있습니다 (미검증).

### 6.2 NVR-C: SNMP 재부팅 시험 성공

- 현장 PC: `DESKTOP-ATRHAF7`
- NVR: 192.168.0.100 (중간에 라우터 있음, `ttl=63`), 펌웨어 5.30.72
- 정상 상태에서 시험

| 시각 (KST) | 내용 |
|---|---|
| 17:05 | `snmpset reboot "OK"` → 접수. OS 가동 시간 초기화, coldPowerOnDate가 08:04:46(UTC) = 17:04:46(KST)로 갱신 |
| 17:12:13 ~ 17:13:19 | 재시험. **RTSP 약 67초 중단 후 복귀** → 실제 재부팅 확인 |

- 이 장비는 8000번 포트로 웹 응답이 없었습니다 (`web=000`). 웹 포트 확인 필요.
- 과거 비정상 시작 기록: `abnormalStartDate` 2026-04-23 17:12:36(UTC). 정전 등으로 추정됩니다.

---

## 7. 장비 식별


**확인 방법**

```bash
sudo nmap -sU -p 161 <NVR_IP>      # 출력에 MAC 주소 표시 (같은 LAN일 때)
ip neigh | grep <NVR_IP>           # 같은 LAN에서 MAC 확인
```

- SNMP 시리얼 번호(`B.2.1.9.0`), ONVIF `info` 결과(모델·펌웨어), HTTPS 인증서 CN(MAC 기반)으로도 식별할 수 있습니다.
- **현장별 장비 대장**에 현장 PC 이름, NVR MAC, 시리얼, 펌웨어, SNMP 활성 여부를 기록해 두세요.
- 재부팅 스크립트는 실행 전에 대상 정보를 출력하므로, 대장과 대조한 뒤 `yes`를 입력하세요.

---

## 8. 복구 후 조치 / 현장 점검

전원 리셋으로 복구한 뒤:

1. SUNAPI가 `401`로 응답하는지, 웹 로그인이 되는지 확인
2. **SNMP v3 활성화** (3.2절)
3. 시스템 로그 내보내기, HDD 상태 확인
4. **같은 장비가 반복해서 멈추면** 근본 원인을 의심하세요.
   - 전원을 완전히 차단했다가 다시 켜기 (콜드 부팅)
   - **HDD를 분리한 상태로 부팅해 보기.** 정상이면 HDD가 원인
   - HDD 교체, 펌웨어 변경 검토, 한화 기술지원 문의
5. 자동 재부팅 스케줄 설정 검토

---

## 9. 참고: RTSP 영상 확인

```bash
ffprobe -v error -show_entries stream=codec_name,width,height \
  -rtsp_transport tcp -timeout 10000000 \
  "rtsp://admin:<비밀번호>@<NVR_IP>:558/LiveChannel/0/media.smp"
```

NVR은 `/LiveChannel/<채널번호>/media.smp` 경로를 씁니다. 카메라용 경로(`/profile2/media.smp`)는 404가 납니다.

---

## 10. 향후 계획

- [ ] **NVR-A 현장 전원 리셋**, 복구 후 SNMP 활성화 및 원인 조사 (로그, HDD)
- [ ] 웹 CGI가 멈춘 상태에서 SNMP 재부팅이 통하는지 검증 (SNMP가 켜진 장비에서 장애 발생 시)
- [ ] NVR-C 웹 포트 확인 후 재부팅 시 웹 재시작 여부 확인
- [ ] **모든 현장 NVR에 SNMP v3 활성화** (특수문자 없는 비밀번호)
- [ ] **현장별 장비 대장 작성** (MAC, 시리얼, 펌웨어, SNMP 상태)
- [ ] **함체 표준 구성에 원격 전원 리셋 장치(IP 릴레이 / 스마트 PDU) 포함 검토**
- [ ] 현장 PC 감시 스크립트: 녹화·영상·HDD 상태 감시, 장애 시 SNMP 재부팅 → 실행 검증 → 실패 시 전원 리셋 장치 제어 및 알림
- [ ] NVR 펌웨어 버전 통일 검토