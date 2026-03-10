import numpy as np, cv2

while True:
    no = int(input("차량 영상 번호( 0:종료) : "))
    if no == 0: break

    frame = "images/test_car/{0:02d}.jpg".format(no)    # 영상파일 이름 구성
    img = cv2.imread(frame, cv2.IMREAD_COLOR)
    if img is None:
        print(str(no) + "번 영상 파일이 없습니다.")
        continue

    mask = np.ones((5, 17), np.uint8) # 닫힘 연산 마스크
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 명암도 영상 변환
    gray = cv2.blur(gray, (5, 5)) # 블러링
    gray = cv2.Sobel(gray, cv2.CV_8U, 1, 0, 5)  # 소벨 에지 검출

    # 이진화 및 닫힘 연산 수행
    th_img = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)[1]
    morph = cv2.morphologyEx(th_img, cv2.MORPH_CLOSE, mask, iterations=3)

    cv2.imshow("image", img)
    cv2.imshow("binary image", th_img)
    cv2.imshow("opening", morph)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
