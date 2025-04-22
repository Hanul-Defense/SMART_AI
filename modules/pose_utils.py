import math

def calculate_angle(p1, p2, p3):
    # 항상 [id, x, y, z] 또는 [x, y]라고 가정할 수 없으니 방어코드 추가
    try:
        x1, y1 = p1[1], p1[2]
        x2, y2 = p2[1], p2[2]
        x3, y3 = p3[1], p3[2]
    except IndexError:
        return 0  # 값 부족하면 angle 계산 못하니까 0 리턴

    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                         math.atan2(y1 - y2, x1 - x2))
    angle = abs(angle)
    if angle > 180:
        angle = 360 - angle
    return angle