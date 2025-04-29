import cv2
import numpy as np
import mediapipe as mp


def draw_ui_box(image, counter, stage):
    # UI 박스
    cv2.rectangle(image, (0, 0), (200, 80), (0, 0, 0), -1)
    cv2.putText(
        image,
        "REPS",
        (10, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        1,
        cv2.LINE_AA,
    )
    cv2.putText(
        image,
        str(counter),
        (10, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (0, 255, 0),
        2,
        cv2.LINE_AA,
    )

    cv2.putText(
        image,
        "STAGE",
        (100, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        1,
        cv2.LINE_AA,
    )
    cv2.putText(
        image,
        stage if stage else "-",
        (100, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (0, 255, 255),
        2,
        cv2.LINE_AA,
    )


def draw_angle(image, left_angle, right_angle, left_hip):
    # 화면에 각도 표시
    cv2.putText(
        image,
        f"{int(left_angle)}°",
        tuple(np.multiply(left_hip, [640, 480]).astype(int)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )

    cv2.putText(
        image,
        "Right_Angle",
        (300, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        1,
        cv2.LINE_AA,
    )
    cv2.putText(
        image,
        f"{float(round(right_angle,5))}°",
        (300, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (0, 255, 255),
        2,
        cv2.LINE_AA,
    )
