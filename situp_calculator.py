import cv2
import numpy as np
import mediapipe as mp
import time

from angle_calculator import calculate_angle
from utils.ui_utils import draw_ui_box, draw_angle
from enum import Enum


class FacingDirection(Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    UNKNOWN = "UNKNOWN"


category = input("숫자를 입략해주세요.(1. pushup 2. situp)")

# MediaPipe 초기 설정
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# 반복 횟수 변수
counter = 0
stage = None
angle_list = []
frame_angles = []

# 웹캠 열기
# 기본 값: 0, 외부 카메라 연결: 1
# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("./res/right1.mov")
last_log = time.time()
with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # BGR → RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # 포즈 감지
        results = pose.process(image)

        # 다시 RGB → BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark
            # 왼쪽 팔 좌표 추출
            left_shoulder = [
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].z,
            ]
            right_shoulder = [
                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y,
                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].z,
            ]
            left_hip = [
                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y,
            ]
            right_hip = [
                landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y,
            ]
            left_elbow = [
                landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y,
            ]
            right_elbow = [
                landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y,
            ]
            left_knee = [
                landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y,
            ]
            right_knee = [
                landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y,
            ]

            # 각도 계산
            left_angle = calculate_angle(left_shoulder, left_hip, left_knee)
            right_angle = calculate_angle(right_shoulder, right_hip, right_knee)

            left_relative_x = round(left_elbow[0] - left_knee[0], 3)
            left_relative_y = round(left_elbow[1] - left_knee[1], 3)
            right_relative_x = round(right_elbow[0] - right_knee[0], 3)
            right_relative_y = round(right_elbow[1] - right_knee[1], 3)

            current_time = time.time()
            if current_time - last_log >= 0.1:
                frame_angles.append(round(right_angle, 4))
                if len(frame_angles) == 10:
                    angle_list.append(frame_angles)
                    frame_angles = []
                    # print(right_relative_x)

            draw_angle(
                image=image,
                left_angle=round(left_angle, 2),
                right_angle=round(right_angle, 2),
                left_hip=left_hip,
            )

            # 발 방향
            feet_direction = (
                FacingDirection.RIGHT
                if (left_shoulder[2] - right_shoulder[2]) > 0
                else FacingDirection.LEFT
            )

            # 운동 상태 및 카운트
            if left_angle > 115 or right_angle > 115:
                stage = "down"

            # 좌표 기반
            if (
                (-0.03 <= left_relative_x <= 0.03 or -0.03 <= right_relative_x <= 0.03)
                and (left_angle < 30 or right_angle < 30)
                and stage == "down"
            ):
                stage = "up"
                counter += 1
                print(f"[🔥 Count] {counter}")
                print(f"left touch (rel): {left_relative_x:.3f}, {left_relative_y:.3f}")
                print(f"{left_shoulder[2]:.3f}  {right_shoulder[2]:.3f}")
                print(
                    f"right touch (rel): {right_relative_x:.3f}, {right_relative_y:.3f}"
                )

        except:
            pass

        # ui box 그리기
        draw_ui_box(image=image, counter=counter, stage=stage)

        # 랜드마크 시각화
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
        )

        # 결과 출력
        cv2.imshow("Bicep Curl Counter", image)
        if cv2.waitKey(10) & 0xFF == ord("q"):
            break


cap.release()
cv2.destroyAllWindows()
