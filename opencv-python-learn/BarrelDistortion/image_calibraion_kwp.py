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
    # [추가된 부분] 저장할 폴더가 없으면 자동으로 생성합니다.
    os.makedirs(savePath, exist_ok=True)
    objpoints = [] # 알려진 3D 점(objpoints) 값
    imgpoints = [] # 감지된 코너의 해당 픽셀 좌표

    # 주어진 디렉터리에 저장된 개별 이미지의 경로 추출
    imagePath = os.path.join(path, f"*{ext}")
    images = glob.glob(imagePath)

    #object point 생성 = 0값
    objp = np.zeros((1, patternSize[0] * patternSize[1], 3), np.float32)
    objp[0, :, :2] = np.mgrid[0:patternSize[0], 0:patternSize[1]].T.reshape(-1, 2)
    valid_filenames = [] # [추가] 인식이 성공한 파일의 이름을 기억해둘 리스트

    for frame_c in images:
        arr = np.fromfile(frame_c, dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

        # img = cv2.imread(frame_c)
        name = os.path.splitext( os.path.basename(frame_c) )[0]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 그레이 스케일로 변환
        
        # 이미지에서 원하는 개수의 코너가 발견되면 ret = true
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
            valid_filenames.append(name) # [추가] 성공한 파일명 저장
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


            # cv2.imwrite(saveName, drawIamge)

    # 카메라 캘리브레이션 수행
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints,
                                                    imgpoints,
                                                    gray.shape[::-1],
                                                    None, None)
    
    # ---------------------------------------------------------
    # [추가 코드] 1. 전체 RMS 오차율 확인
    print("\n" + "="*50)
    print(f"[결과] 전체 캘리브레이션 RMS 오차율 (ret): {ret:.4f} 픽셀")
    if ret < 1.0:
        print("  -> 👍 오차가 1.0 미만이므로 캘리브레이션이 매우 훌륭합니다!")
    else:
        print("  -> ⚠️ 오차가 1.0 이상입니다. (체커보드 이미지가 흐릿하거나, 각도가 다양하지 않을 수 있습니다.)")
    print("="*50)

    # [추가 코드] 2. 더 정밀한 검증: 재투영 오차(Re-projection Error) 계산
    # (우리가 구한 파라미터로 3D 좌표를 2D로 다시 변환했을 때, 실제 찍힌 코너와 얼마나 차이나는지 계산)
    mean_error = 0
    for i in range(len(objpoints)):
        # objpoints를 이용해 이미지 상의 좌표로 다시 투영해봄
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        
        # 실제 찾은 코너(imgpoints)와 다시 투영한 코너(imgpoints2)의 거리 차이 계산
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
        mean_error += error
        # print(f" - 이미지 {i+1} 오차: {error:.4f}") # (선택) 각 이미지별 오차를 보려면 주석 해제
        # [수정된 부분] 파일명과 함께 출력 (오차가 0.7 이상인 녀석들만 콕 집어서 빨간펜 선생님처럼 출력!)
        if error >= 0.7:
            print(f" 🚨 [삭제 권장] {valid_filenames[i]}{ext} -> 오차: {error:.4f}")
        else:
            print(f" - [정상] {valid_filenames[i]}{ext} -> 오차: {error:.4f}")

    total_error = mean_error / len(objpoints)
    print(f"[결과] 재투영 오차 (Re-projection Error) 평균: {total_error:.4f} 픽셀\n")
    # ---------------------------------------------------------

    print("Camera matrix : \n", mtx)  
    print("\ndist : \n", dist)  

    print("Camera matrix : \n\n", mtx)  # 내부 카메라 행렬
    print("dist : \n\n", dist)  # 렌즈 왜곡 계수(Lens distortion coefficients)
    print("rvecs : \n\n", rvecs)  # 회전 벡터
    print("tvecs : \n\n", tvecs)  # 이동 벡터
    
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
