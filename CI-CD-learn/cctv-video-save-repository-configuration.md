> MinIO로 새로 구축하는 것은 권하지 않는 이유와 대안, OS 선택, 설치 순서

## 1. 오브젝트 스토리지란? (MinIO가 하던 일)

**일반 파일 서버(NAS, 공유 폴더)** 는 `D:\영상\하천A\2026호우\cam1.mp4`처럼 폴더 트리에 파일을 두고, Windows 공유(SMB)로 네트워크 드라이브를 연결해서 씁니다. 익숙하지만 Linux 서버, Jenkins, 엣지 PC, Python 코드가 여러 곳에서 동시에 접근하려면 마운트, 권한, 경로 문제가 계속 생깁니다.

**오브젝트 스토리지**는 파일을 HTTP로 주고받는 창고라고 생각하면 됩니다. 개념은 세 가지뿐입니다.

- **버킷(bucket)**: 최상위 창고입니다. 예: `river-videos`
- **키(key)**: 파일 이름이고, 폴더처럼 보이는 문자열입니다. 예: `siteA/2026-07-15_event/cam1.mp4`
- **오브젝트(object)**: 실제 파일 내용과 메타데이터입니다.

이 창고에 접근하는 표준 규약이 AWS의 **S3 API**입니다. S3 호환 서버를 사내에 설치하면 Python(`boto3`), Jenkins, 엣지 PC 어디서든 같은 코드로 업로드와 다운로드를 할 수 있습니다. 사용자별 접근 키도 발급할 수 있습니다. MinIO는 이 S3 호환 서버를 사내에 직접 설치할 수 있게 해 주는 대표적인 오픈소스였습니다.

## 2. MinIO를 지금 쓰면 안 되는 이유

2025년 5월 커뮤니티 버전 웹 UI에서 관리 기능 대부분이 빠져 유료 제품으로 옮겨졌고, 같은 해 10월에는 커뮤니티 버전용 Docker 이미지와 바이너리 배포가 아예 중단됐습니다. 2025년 12월에 유지보수 모드가 선언됐고, 2026년 4월 25일에는 서버 저장소가 보관(archived) 처리됐습니다. 이 때문에 신뢰할 수 있는 공식 바이너리가 없어서, 보안 패치가 나올 때마다 사용자가 직접 소스에서 빌드해야 하는 부담이 생깁니다. 혼자 운영하는 상황에서 이 부담까지 지는 것은 맞지 않습니다.

**대안 비교** (모두 S3 API를 지원하므로 Python 코드는 동일합니다)

| 후보          | 특징                                   | 추천 상황                   |
| ------------- | -------------------------------------- | --------------------------- |
| **SeaweedFS** | 성숙도가 가장 높고 Apache 2.0 라이선스 | 기본 추천                   |
| **Garage**    | 가볍고 여러 대 복제에 강함             | 나중에 PC 2~3대로 분산할 때 |
| **RustFS**    | MinIO와 가장 비슷하고 웹 UI 있음       | 성숙도를 지켜본 뒤 고려     |

MinIO 대신 SeaweedFS를 택하는 경우가 가장 많고, Kubeflow Pipelines도 기본 스토리지를 SeaweedFS로 바꿨습니다. 반면 RustFS는 알파 단계 소프트웨어로 평가되기도 합니다. 원본 하천 영상은 다시 구할 수 없는 데이터이므로, 검증된 쪽을 고르는 게 맞습니다.

## 3. 하드웨어: 미니 PC보다 남는 데스크탑

여기서 가장 중요한 것은 소프트웨어보다 **디스크 이중화**입니다. 한 대짜리 서버에 디스크가 하나면 그 디스크가 고장 나는 순간 호우 사상 영상이 전부 사라집니다.

- **데스크탑 추천**: SATA 포트가 여러 개라서 같은 용량의 HDD 2개를 미러(RAID1)로 구성할 수 있습니다. 미니 PC는 보통 디스크 슬롯이 1~2개뿐이고, USB 외장 디스크로 RAID를 구성하는 것은 불안정합니다.
- **디스크**: NAS용 HDD(WD Red Plus, Seagate IronWolf 등) 2개를 쓰고, OS는 별도 SSD에 설치합니다.
- **보너스**: 데스크탑 CPU가 괜찮다면 이 PC를 Jenkins 평가 agent로도 같이 씁니다. 데이터가 있는 곳에서 연산하면 대용량 영상을 네트워크로 옮길 필요가 없습니다.
- **백업**: 미러는 디스크 고장 대비일 뿐 실수로 삭제한 것은 막지 못합니다. 원본 영상은 주기적으로 외장 디스크나 클라우드에 따로 복사해 두세요.

## 4. OS 선택

**추천: Ubuntu Server 24.04 LTS**

- 자료와 예제가 가장 많아서 막혔을 때 검색으로 해결하기 쉽습니다.
- Docker, Jenkins agent, ZFS를 모두 공식적으로 지원합니다.
- 화면 없이 SSH로 원격 관리하는 서버용 구성입니다.

다른 선택지와 비교하면 다음과 같습니다.

- **TrueNAS SCALE**: NAS 전용 OS라서 웹 화면으로 디스크 미러, 스냅샷, 공유 폴더를 클릭으로 설정할 수 있습니다. 리눅스 명령어가 부담스럽다면 좋은 선택이지만, Jenkins agent처럼 자유롭게 쓰기에는 제약이 있습니다.
- **Debian**: Ubuntu와 거의 같고 더 보수적입니다. 차이가 크지 않으니 자료가 많은 Ubuntu를 권합니다.
- **Windows**: 서버 용도로는 비추천입니다. Docker, 파일 권한, 자동 업데이트 재부팅 문제가 계속 생깁니다.

## 5. 설치 순서 (Ubuntu + SeaweedFS)

**① OS 설치와 고정 IP**
Ubuntu Server를 SSD에 설치합니다. 설치 중에 OpenSSH 서버를 체크하고, 공유기나 사내 망에서 고정 IP(예: `192.168.0.50`)를 지정합니다.

**② 디스크 미러 구성 (ZFS)**

```bash
sudo apt install zfsutils-linux
lsblk            # HDD 장치 이름 확인 (예: sdb, sdc)
sudo zpool create -o ashift=12 storage mirror /dev/sdb /dev/sdc
sudo zfs create storage/seaweedfs
```

이렇게 하면 `/storage/seaweedfs`가 두 디스크에 똑같이 기록되는 폴더가 됩니다. 실제로는 `/dev/sdb` 대신 `/dev/disk/by-id/...` 경로를 쓰는 것이 안전합니다(재부팅 시 장치 이름이 바뀔 수 있기 때문).

**③ Docker 설치**

```bash
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER   # 로그아웃 후 재로그인
```

**④ 접근 키 설정 파일** (`~/seaweed/s3.json`)

```json
{
  "identities": [
    {
      "name": "admin",
      "credentials": [
        { "accessKey": "admin-key", "secretKey": "길고-복잡한-비밀번호" }
      ],
      "actions": ["Admin", "Read", "Write", "List", "Tagging"]
    },
    {
      "name": "jenkins",
      "credentials": [
        { "accessKey": "jenkins-key", "secretKey": "또-다른-비밀번호" }
      ],
      "actions": ["Read", "List"]
    }
  ]
}
```

사람이나 용도별로 키를 나눠 두면, 평가용 Jenkins는 읽기만 하고 원본 영상을 지우지 못하게 할 수 있습니다.

**⑤ SeaweedFS 실행** (`~/seaweed/docker-compose.yml`)

```yaml
services:
  seaweedfs:
    image: chrislusf/seaweedfs
    command: server -dir=/data -s3 -s3.config=/etc/seaweedfs/s3.json
    ports:
      - "8333:8333" # S3 API
      - "9333:9333" # 관리 상태 페이지
    volumes:
      - /storage/seaweedfs:/data
      - ./s3.json:/etc/seaweedfs/s3.json:ro
    restart: unless-stopped
```

```bash
cd ~/seaweed && docker compose up -d
```

**⑥ Windows PC에서 동작 확인 (Python)**

```python
import boto3

s3 = boto3.client(
    "s3",
    endpoint_url="http://192.168.0.50:8333",
    aws_access_key_id="admin-key",
    aws_secret_access_key="길고-복잡한-비밀번호",
)
s3.create_bucket(Bucket="river-videos")
s3.upload_file(r"D:\영상\siteA\event01\cam1.mp4",
               "river-videos", "siteA/2026-07-15_event01/cam1.mp4")
print([o["Key"] for o in s3.list_objects_v2(Bucket="river-videos")["Contents"]])
```

기존 로컬 영상을 한꺼번에 옮길 때는 `rclone`(무료 동기화 도구)을 쓰면 폴더 단위로 이어서 업로드할 수 있어 편합니다.

## 6. 솔직한 대안: 처음엔 공유 폴더로 시작해도 됩니다

서버가 한 대이고 사용자가 몇 명뿐이라면, 같은 Ubuntu와 ZFS 미러 위에 **Samba 공유 폴더**만 열어도 1단계 목표(영상 한곳에 모으기)는 달성됩니다. 다만 S3로 시작하면 이후 엣지 PC의 자동 업로드, Jenkins 평가, 다른 사람의 접근 권한 관리까지 같은 방식으로 이어지기 때문에, 처음부터 SeaweedFS로 가는 것을 권합니다. 저장된 파일 위치(ZFS 미러)는 어느 쪽이든 같으므로, 나중에 바꾸는 것도 어렵지 않습니다.

남는 데스크탑의 사양(CPU, 디스크 슬롯 수, 메모리)을 알려주시면 그에 맞춰 디스크 구성과 Jenkins agent 겸용 여부를 구체적으로 정리해 드리겠습니다.

Sources:

- [MinIO Is Done With Open Source, What Are Your Options? (It's FOSS)](https://itsfoss.com/news/minio-moves-away-from-open-source/)
- [MinIO CE in 2026: Retired Upstream, Source-Only, and What to Use](https://glukhov.org/data-infrastructure/object-storage/minio-dead/)
- [How MinIO Community Edition Ended — Timeline](https://www.youngju.dev/blog/2026-07-17-minio-archived-garage-seaweedfs-ceph-rgw.en)
- [MinIO is archived: self-hosted S3-compatible storage compared (WZ-IT)](https://wz-it.com/en/blog/minio-successor-s3-storage-comparison/)
- [RustFS vs SeaweedFS vs Garage (Elestio)](https://blog.elest.io/rustfs-vs-seaweedfs-vs-garage-which-minio-alternative-should-you-pick/)
