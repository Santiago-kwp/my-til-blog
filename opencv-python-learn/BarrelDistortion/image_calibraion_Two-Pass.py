import cv2
import os
import numpy as np
import glob

"""
size: 행열 개수 => (row, col)
path: 이미지가 있는 폴더 위치 
savePath: 이미지가 저장되는 폴더 경로
ext: 이미지의 확장자 => .png 
patternType: 보정에서 사용하는 보드 타입 (True: 체크보드 / False: 원 모양 zigzag)

return 
    retval: calibration 품질 정도. 값이 낮을수록 보정이 잘 되었다는 뜻
    cameraMatrix: 3x3 형태의 카메라 내부 행렬 값
    distCoeff: 렌즈 왜곡 계수
    rvecs: 3x1 회전 벡터. 벡터의 방향은 회전 축을 지정, 크기는 회전 각을 지정
    tvecs: 3x1 이동 벡터
"""


def imageCalibration(patternSize: tuple, path: str, savePath: str, ext=".jpg", patternType=True):
    os.makedirs(savePath, exist_ok=True)

    objpoints = [] 
    imgpoints = [] 
    valid_filenames = [] # 성공한 파일명 저장

    imagePath = os.path.join(path, f"*{ext}")
    images = glob.glob(imagePath)

    objp = np.zeros((1, patternSize[0] * patternSize[1], 3), np.float32)
    objp[0, :, :2] = np.mgrid[0:patternSize[0], 0:patternSize[1]].T.reshape(-1, 2)

    print(f"이미지 로딩 및 코너 탐지 중... (총 {len(images)}장)")
    for frame_c in images:
        arr = np.fromfile(frame_c, dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

        name = os.path.splitext( os.path.basename(frame_c) )[0]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        
        ret, corners = False, None
        if patternType:
            ret, corners = cv2.findChessboardCorners(gray, patternSize,
                                            cv2.CALIB_CB_ADAPTIVE_THRESH
                                            + cv2.CALIB_CB_FAST_CHECK
                                            + cv2.CALIB_CB_NORMALIZE_IMAGE)
        else:    
            ret, corners = cv2.findCirclesGrid(gray, patternSize,
                                            flags=cv2.CALIB_CB_ASYMMETRIC_GRID)
            
        if ret:
            valid_filenames.append(name)
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (10, 10), (-1, -1),
                                        (cv2.TERM_CRITERIA_EPS
                                        + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
            imgpoints.append(corners2)

            drawIamge = cv2.drawChessboardCorners(img, patternSize, corners2, ret)
            saveName = os.path.join(savePath, f"{name}_save{ext}")

            type = os.path.splitext(saveName)[1] 
            rst, img_arr = cv2.imencode(type, drawIamge)
            if rst:
                with open(saveName, mode='w+b') as f:                
                    img_arr.tofile(f)


    # =========================================================
    # [1차 캘리브레이션] 전체 데이터로 일단 계산
    # =========================================================
    print("\n" + "="*50)
    print(" 🛠️ [1단계] 1차 캘리브레이션 수행 및 불량 데이터 필터링")
    print("="*50)
    
    # 기존 코드
    # ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    # 수정된 코드 (끝에 flags 추가)
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None, flags=cv2.CALIB_FIX_K3
    )
    
    # 우량 데이터만 골라 담을 새로운 리스트
    good_objpoints = []
    good_imgpoints = []
    
    ERROR_THRESHOLD = 0.7 # 이 수치 이상인 이미지는 버림
    drop_count = 0

    mean_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
        mean_error += error
        
        # 필터링 로직: 에러가 기준치 미만이면 합격(good), 이상이면 탈락
        if error < ERROR_THRESHOLD:
            good_objpoints.append(objpoints[i])
            good_imgpoints.append(imgpoints[i])
        else:
            print(f" 🚨 [제외됨] {valid_filenames[i]}{ext} (오차: {error:.4f})")
            drop_count += 1

    print(f" -> 총 {len(objpoints)}장 중 오차가 {ERROR_THRESHOLD} 이상인 {drop_count}장 제외 완료.\n")

    # =========================================================
    # [2차 캘리브레이션] 걸러진 '우량 데이터'로만 다시 정밀 계산!!!
    # =========================================================
    if drop_count > 0:
        print("="*50)
        print(" 🚀 [2단계] 우량 데이터만 사용하여 2차 정밀 캘리브레이션 수행")
        print("="*50)
        
        # 필터링된 데이터(good_objpoints, good_imgpoints)로 재계산 - 기존 코드
        # ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(good_objpoints, good_imgpoints, gray.shape[::-1], None, None)
        # 수정된 코드 (끝에 flags 추가)
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
            good_objpoints, good_imgpoints, gray.shape[::-1], None, None, flags=cv2.CALIB_FIX_K3
        )
        
        # 2차 보정 후의 재투영 오차 다시 계산 확인
        mean_error2 = 0
        for i in range(len(good_objpoints)):
            imgpoints2, _ = cv2.projectPoints(good_objpoints[i], rvecs[i], tvecs[i], mtx, dist)
            error = cv2.norm(good_imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
            mean_error2 += error
        
        final_reproj_error = mean_error2 / len(good_objpoints)
        
        print(f"[최종 결과] 전체 RMS 오차율 (ret) : {ret:.4f} 픽셀")
        print(f"[최종 결과] 평균 재투영 오차      : {final_reproj_error:.4f} 픽셀")
    else:
        print("[결과] 제외할 데이터가 없어 1차 결과(ret: {ret:.4f})를 그대로 사용합니다.")


    return ret, mtx, dist, rvecs, tvecs

def createCalibImage(path: str, ext: str, savePath: str, mtx: list, dist: list):
    # [수정됨] 결과를 저장할 'calib-results' 폴더를 강제로 생성합니다.
    os.makedirs(savePath, exist_ok=True)
    
    # 주어진 디렉터리에 저장된 개별 이미지의 경로 추출
    imagePath = os.path.join(path, f"*{ext}")
    images = glob.glob(imagePath)
    

    for frame_c in images:
        arr = np.fromfile(frame_c, dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

        # img = cv2.imread(frame_c)
        name = os.path.splitext( os.path.basename(frame_c) )[0]
        saveName = os.path.join(savePath, f"{name}_calibresult{ext}")

        h,  w = img.shape[:2]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

        mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w,h), 5)
        dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR) # 속도는 빠르지만 화질은 보통
        # dst = cv2.remap(img, mapx, mapy, cv2.INTER_CUBIC)  # 보간법 변경으로 테두리 화질 선명 but 느림
        # dst = cv2.remap(img, mapx, mapy, cv2.INTER_LANCZOS4)  
        
        # 주석 처리 
        # x, y, w, h = roi
        # dst = dst[y:y+h, x:x+w]

        type = os.path.splitext(saveName)[1] 
        rst, img_arr = cv2.imencode(type, dst)
        if rst:
            with open(saveName, mode='w+b') as f:                
                img_arr.tofile(f)
        # cv2.imwrite(f"{name}", dst)
    


#입력값 예제

patternSize = (7, 4) # 가로 8칸, 세로 5칸짜리 체커보드
path = r"C:\Users\HydroSEM\dev\santiago\my-til-blog\opencv-python-learn\BarrelDistortion\images"
savePath = r"C:\Users\HydroSEM\dev\santiago\my-til-blog\opencv-python-learn\BarrelDistortion\calibrations"
clibSavePath = r"C:\Users\HydroSEM\dev\santiago\my-til-blog\opencv-python-learn\BarrelDistortion\calib-results"
ext = ".jpg" # default = png
patternType = True # defalut = checkboard

ret, mtx, dist, rvecs, tvecs = imageCalibration(patternSize, path, savePath, ext, patternType)
createCalibImage(path, ext, clibSavePath, mtx, dist)
