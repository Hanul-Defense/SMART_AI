from angle_calculator import calculate_angle
import cv2
import numpy as np
import mediapipe as mp

category = input("숫자를 입략해주세요.(1. pushup 2. situp)")

# MediaPipe 초기 설정
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# 반복 횟수 변수
counter = 0
stage = None


# 웹캠 열기
# 기본 값: 0, 외부 카메라 연결: 1
# cap = cv2.VideoCapture(1)
cap = cv2.VideoCapture("./res/right1.mov")

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
            ]
            right_shoulder = [
                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y,
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
                (200, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                1,
                cv2.LINE_AA,
            )
            cv2.putText(
                image,
                f"{int(right_angle)}°",
                (200, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (0, 255, 255),
                2,
                cv2.LINE_AA,
            )

            # 운동 상태 및 카운트
            if left_angle > 115 or right_angle > 115:
                stage = "down"
            if (left_angle < 35 or right_angle < 35) and stage == "down":
                stage = "up"
                counter += 1
                print(f"[🔥 Count] {counter}")
                print(f"left shoulder: {left_shoulder[0]} , {left_shoulder[1]}")

        except:
            pass

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
