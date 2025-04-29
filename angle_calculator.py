import cv2
import numpy as np
import mediapipe as mp

# 각도 계산 함수
def calculate_angle(a, b, c):
    a = np.array(a)  # 어깨
    b = np.array(b)  # 팔꿈치
    c = np.array(c)  # 손목

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

# MediaPipe 초기 설정
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# 반복 횟수 변수
counter = 0
stage = None
is_visible = False

# 웹캠 열기
cap = cv2.VideoCapture(0)

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

        if results.pose_landmarks:
            is_visible = True
            landmarks = results.pose_landmarks.landmark

            # 왼쪽 팔 좌표 추출
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            # 각도 계산
            angle = calculate_angle(shoulder, elbow, wrist)

            # 화면에 각도 표시
            cv2.putText(image, f"{int(angle)}°",
                        tuple(np.multiply(elbow, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

            # 운동 상태 및 카운트
            if angle > 160:
                stage = "down"
            if angle < 90 and stage == 'down':
                stage = "up"
                counter += 1
                print(f"[🔥 Count] {counter}")

        else:
            # 포즈를 못 찾으면 사람 없는 걸로 간주
            is_visible = False
            stage = None  # 새로 들어오면 다시 초기화


        # UI 박스
        cv2.rectangle(image, (0, 0), (225, 80), (0, 0, 0), -1)
        cv2.putText(image, 'REPS', (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter),
                    (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.putText(image, 'STAGE', (100, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(image, stage if stage else '-',
                    (100, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 2, cv2.LINE_AA)

        # 랜드마크 시각화
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # 결과 출력
        cv2.imshow('Bicep Curl Counter', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()