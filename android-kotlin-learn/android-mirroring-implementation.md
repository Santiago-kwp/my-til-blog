# 안드로이드 미러링 상세 구현 리포트 (Phase 1 ~ 4 종합)

본 문서는 태블릿 화면의 실시간 미러링 및 원격 제어 기능을 위한 기술적 설계와 세부 구현 내역을 기록합니다.

## 1. 시스템 아키텍처 개요

본 미러링 시스템은 별도의 외부 서버 없이 태블릿 자체를 임베디드 서버로 활용하는 P2P(Peer-to-Peer) 구조로 설계되었습니다.

- **Embedded Web Server (Ktor CIO)**:
  - 포트 `8080` 및 `0.0.0.0` 바인딩으로 로컬 네트워크 내 모든 기기의 접속 허용.
  - `assets/index.html` 배포 및 시그널링용 WebSocket 경로(`ws/signaling`) 제공.
- **WebRTC Stack (Signaling & Streaming)**:
  - **Signaling**: JSON 포맷의 `SignalingMessage`를 통한 Offer/Answer/ICE 교환.
  - **Video**: `MediaProjection` API와 `ScreenCapturerAndroid`를 결합하여 시스템 화면 캡처.
  - **Control**: WebRTC `DataChannel`을 활용하여 브라우저의 터치 이벤트를 태블릿 명령으로 변환.

## 2. 세부 구현 내역

### 2.1 실시간 화면 캡처 및 송출 (MirroringService & WebRtcManager)

- **캡처 엔진**: `ScreenCapturerAndroid`를 사용하여 태블릿 전체 화면을 720p(1280x720) 20fps로 인코딩.
- **포그라운드 서비스**: 안드로이드 보안 정책에 따라 `mediaProjection` 타입의 포그라운드 서비스로 실행하여 백그라운드에서도 송출 유지.
- **미러링 호환성**: `CameraX` 프리뷰가 공유 화면에서 검게 보이는 문제를 해결하기 위해 `PreviewView.ImplementationMode.COMPATIBLE` (TextureView) 강제 적용.

### 2.2 원격 제어 인터페이스 (MainActivity & DataChannel)

- **이벤트 주입**: 브라우저에서 전송된 상대 좌표(0.0~1.0)를 태블릿의 물리 해상도로 환산하여 `dispatchTouchEvent`를 통해 시스템 이벤트 주입.
- **모달 윈도우 대응**: `AlertDialog` 등이 팝업될 때 터치 이벤트가 유실되지 않도록 `activeDialogDecorView` 추적 로직 구현.
  - `SettingFragment`에서 다이얼로그 `onShow` 시 타겟 뷰를 동적으로 변경.
- **다이얼로그 단순화**: 안드로이드 14+ 대응을 위해 `MediaProjectionConfig`를 적용, 불필요한 선택 단계를 생략하고 즉시 전체 화면 공유 시작.

### 2.3 네트워크 및 연결 자동화 (NsdHelper & MirroringService)

- **자동 감지**: `NsdHelper`를 통해 `_http._tcp` 타입으로 네트워크에 서비스를 등록, 향후 브라우저에서 IP 입력 없이 태블릿 자동 검색 기반 마련.
- **IPv4/IPv6 하이브리드**: 아이폰 핫스팟 등 다양한 네트워크 환경에서 접속 가능하도록 IPv4 바인딩을 우선하되 IPv6 스택도 수용.

### 2.4 클라이언트 인터페이스 최적화 (index.html)

- **반응형 레이아웃**: CSS Media Query를 통한 가로/세로 모드 최적화.
  - **세로 모드**: 영상을 중앙에 배치하여 터치 조작성 강화, 로그 창 하단 배치.
  - **가로 모드**: 상단 네비게이션 바를 최소화하고 로그 창을 우측 슬림 영역(`140px`)으로 이동시켜 미러링 화면 영역 극대화.
- **연결 상태 동기화**: 앱 종료 시 `onTaskRemoved` 콜백을 통해 서비스를 종료하고, 브라우저에서 `resetUI`를 트리거하여 스트리밍 중단 및 재연결 안내 표시.

## 3. 핵심 코드 스니펫

### 3.1 Ktor 시그널링 서버 설정 (MirroringService.kt)

```kotlin
server = embeddedServer(CIO, port = 8080, host = "0.0.0.0") {
    install(WebSockets)
    routing {
        get("/") { /* index.html 배포 */ }
        webSocket("/ws/signaling") {
            // WebRTC Offer/Answer 교환 및 원격 Command 핸들링
            for (frame in incoming) { /* ... */ }
        }
    }
}.start(wait = false)
```

### 3.2 WebRTC 화면 캡처 엔진 (WebRtcManager.kt)

```kotlin
fun startScreenStreaming(projectionData: Intent) {
    screenCapturer = ScreenCapturerAndroid(projectionData, mediaProjectionCallback)
    surfaceTextureHelper = SurfaceTextureHelper.create("CaptureThread", eglContext)
    val videoSource = factory.createVideoSource(true)
    screenCapturer?.initialize(surfaceTextureHelper, context, videoSource.capturerObserver)
    screenCapturer?.startCapture(1280, 720, 20) // HD 해상도 송출
}
```

### 3.3 원격 터치 주입 로직 (MainActivity.kt)

```kotlin
private fun injectTouchToTopView(xRatio: Float, yRatio: Float) {
    val x = xRatio * metrics.widthPixels
    val y = yRatio * metrics.heightPixels
    // AlertDialog가 떠있을 경우 해당 DecorView로 타겟팅 변경
    val targetView = activeDialogDecorView ?: window.decorView

    val downEvent = MotionEvent.obtain(time, time, MotionEvent.ACTION_DOWN, x, y, 0)
    targetView.dispatchTouchEvent(downEvent)
    // 50ms 지연 후 ACTION_UP 전송하여 클릭 시뮬레이션
}
```

### 3.4 안드로이드 14+ 동의 창 간소화 (SettingFragment.kt)

```kotlin
private fun requestScreenCapturePermission() {
    val manager = getSystemService(Context.MEDIA_PROJECTION_SERVICE) as MediaProjectionManager
    val intent = if (Build.VERSION.SDK_INT >= 34) {
        // "앱 하나 공유" 선택지 생략 후 바로 전체 화면 공유로 유도
        manager.createScreenCaptureIntent(MediaProjectionConfig.createConfigForDefaultDisplay())
    } else {
        manager.createScreenCaptureIntent()
    }
    projectionLauncher.launch(intent)
}
```

### 3.5 웹 클라이언트 좌표 계산 (index.html)

```javascript
// 비디오의 실제 출력 크기와 여백(Letterbox)을 고려한 정밀 좌표 계산
const rect = remoteVideo.getBoundingClientRect();
const videoRatio = 1280 / 720;
const elementRatio = rect.width / rect.height;

let actualWidth,
  actualHeight,
  offsetX = 0,
  offsetY = 0;
if (elementRatio > videoRatio) {
  actualHeight = rect.height;
  actualWidth = actualHeight * videoRatio;
  offsetX = (rect.width - actualWidth) / 2;
} else {
  /* ... 반대 경우 처리 ... */
}

const x = (e.clientX - rect.left - offsetX) / actualWidth;
const y = (e.clientY - rect.top - offsetY) / actualHeight;
```

## 4. 핵심 트러블슈팅 요약

|          문제점           | 원인                          | 해결 방안                                                    |
| :-----------------------: | :---------------------------- | :----------------------------------------------------------- |
| **카메라 화면 검게 나옴** | SurfaceView의 오버레이 방식   | `TextureView` 방식 강제 사용으로 캡처 레이어 통합            |
| **다이얼로그 클릭 불가**  | Activity 윈도우 범위를 벗어남 | 다이얼로그의 `DecorView`를 직접 참조하여 이벤트 주입         |
|  **미러링 중단 시 잔상**  | 스트림 종료 핸들링 누락       | `onconnectionstatechange` 감지로 브라우저 소켓/영상 초기화   |
|   **동의 창 번거로움**    | API 34+의 공유 선택 옵션      | `MediaProjectionConfig.createConfigForDefaultDisplay()` 적용 |

## 5. 향후 로드맵

- **성능 최적화**: H.264 하드웨어 가속 인코딩 파라미터 튜닝.
- **보안**: 접속용 6자리 PIN 번호 인증 시스템 도입.
- **제스처 확장**: 롱클릭 및 드래그 기능을 위한 `MotionEvent` 시퀀스 제어 추가.
