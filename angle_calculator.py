import numpy as np


# 각도 계산 함수
def calculate_angle(start, center, end):
    start = np.array(start)  # 어깨
    center = np.array(center)  # 팔꿈치
    end = np.array(end)  # 손목

    radians = np.arctan2(end[1] - center[1], end[0] - center[0]) - np.arctan2(
        start[1] - center[1], start[0] - center[0]
    )
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle
