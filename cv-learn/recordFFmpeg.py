# 영상 녹화 (VideoRecord 클래스 메서드 - 기존 recordFFmpeg 대체)
    def recordFFmpeg(self, REC_DURATION, bEcho=False):
        stime = datetime.now().strftime("%Y%m%d_%H%M%S")  # ※ 분석 코드의 파일명 파싱 패턴 확인 필요
        self.MP4_FILE = os.path.join(self.DIR_VIDEO, f"{self.CAM_NAME}_{stime}.mp4")
        ffmpegPath = getResourcePath("ffmpeg")

        cmd = [
            f"{ffmpegPath}/ffmpeg",
            "-nostdin",                    # 백그라운드/cron 실행 시 stdin 대기 방지
            "-rtsp_transport", "tcp",
            # "-timeout", "10000000",      # RTSP 소켓 타임아웃 10초(µs). FFmpeg 5 이상에서만!
            #                              # FFmpeg 4.x 이하는 "-stimeout" 사용 (-timeout은 listen 모드로 오동작)
            "-probesize", "5M",
            "-analyzeduration", "5M",
            "-fflags", "+genpts",          # CCTV 타임스탬프 누락 대비 (MP4 먹서는 TS보다 엄격)
            "-i", self.RTSP_URL,
            "-t", str(REC_DURATION),       # FFmpeg이 스스로 정상 종료 → moov 정상 기록
            "-c:v", "copy",
            "-an",
            "-loglevel", "error",
            "-y",
            self.MP4_FILE,
        ]

        self.__log.info(f"RTSP 녹화 시작 (길이: {REC_DURATION}초) -> '{self.MP4_FILE}'")

        try:
            proc = subprocess.Popen(
                cmd,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
            )
        except Exception as e:
            self.__log.error(f"FFmpeg 실행 실패: {e}")
            self.MP4_FILE = None
            return None

        try:
            # 연결·분석 지연을 고려한 여유 시간
            _, stderr = proc.communicate(timeout=REC_DURATION + 20)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.communicate()
            self.__log.error("FFmpeg 응답 없음 - 강제 종료")
            self.fileRemove(self.MP4_FILE)   # 깨진 부분 파일 정리
            self.MP4_FILE = None
            return None

        err = stderr.decode("utf-8", errors="replace").strip()

        if proc.returncode != 0 or not self.confirmFile(self.MP4_FILE):
            self.__log.error(f"녹화 실패 (return code: {proc.returncode}): {err}")
            self.fileRemove(self.MP4_FILE)
            self.MP4_FILE = None
            return None

        # 성공했지만 FFmpeg이 남긴 메시지(예: DTS 관련 경고성 에러)
        if err and bEcho:
            self.__log.info(f"FFmpeg 메시지: {err}")

        self.__log.info(
            f"녹화 완료: '{self.MP4_FILE}' (크기: {os.path.getsize(self.MP4_FILE)} bytes)"
        )
        return self.MP4_FILE