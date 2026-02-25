import numpy as np, cv2, math

def calc_hsi(bgr):
    # B, G, R = bgr.astype(float) # float 형 변환
    B, G, R = float(bgr[0]), float(bgr[1]), float(bgr[2]) # float 형 변환
