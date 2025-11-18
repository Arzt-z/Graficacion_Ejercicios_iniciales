import cv2
import mediapipe as mp
import numpy as np
from pythonosc import udp_client

# === CONFIGURATION ===
VMC_IP = "127.0.0.1"   # same PC
#VMC_IP = "169.254.83.107" 
VMC_PORT = 39543       # default VMC OSC port

# === INITIALIZE ===
client = udp_client.SimpleUDPClient(VMC_IP, VMC_PORT)
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.6, min_tracking_confidence=0.6)
mp_drawing = mp.solutions.drawing_utils

# === Landmark to VMC bone mapping ===
landmark_to_bone = {
    mp_pose.PoseLandmark.NOSE: "Head",
    mp_pose.PoseLandmark.LEFT_SHOULDER: "LeftShoulder",
    mp_pose.PoseLandmark.RIGHT_SHOULDER: "RightShoulder",
    mp_pose.PoseLandmark.LEFT_ELBOW: "LeftArm",
    mp_pose.PoseLandmark.RIGHT_ELBOW: "RightArm",
    mp_pose.PoseLandmark.LEFT_WRIST: "LeftHand",
    mp_pose.PoseLandmark.RIGHT_WRIST: "RightHand",
    mp_pose.PoseLandmark.LEFT_HIP: "LeftUpperLeg",
    mp_pose.PoseLandmark.RIGHT_HIP: "RightUpperLeg",
    mp_pose.PoseLandmark.LEFT_KNEE: "LeftLowerLeg",
    mp_pose.PoseLandmark.RIGHT_KNEE: "RightLowerLeg",
    mp_pose.PoseLandmark.LEFT_ANKLE: "LeftFoot",
    mp_pose.PoseLandmark.RIGHT_ANKLE: "RightFoot",
}


# === Simple Smoothing ===
def smooth(prev, new, alpha=0.6):
    if prev is None:
        return new
    return prev * alpha + new * (1 - alpha)

# === MAIN LOOP ===
cap = cv2.VideoCapture(1)
prev_positions = {}
scale = 1.0  # Adjust to make avatar motion bigger or smaller

print("🟢 Sending OSC tracking data to VMC... (press ESC to exit)")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 0)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    if results.pose_landmarks:
        h, w, _ = frame.shape
        landmarks = results.pose_landmarks.landmark

        for idx, bone in landmark_to_bone.items():
            lm = landmarks[idx]
            x, y, z = lm.x, lm.y, lm.z

            # Optional: flip y-axis for consistency
            pos = np.array([(x - 0.5) * scale, -(y - 0.5) * scale, z * scale])
            prev_positions[bone] = smooth(prev_positions.get(bone), pos)
            # Smooth movement
            # === Add Chest bone (midpoint between shoulders) ===
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

            chest_x = (left_shoulder.x + right_shoulder.x) / 2
            chest_y = (left_shoulder.y + right_shoulder.y) / 2
            chest_z = (left_shoulder.z + right_shoulder.z) / 2

            chest_pos = np.array([(chest_x - 0.5) * scale, -(chest_y - 0.5) * scale, chest_z * scale])
            prev_positions["Chest"] = smooth(prev_positions.get("Chest"), chest_pos)
            client.send_message("/VMC/Ext/Bone/Pos", ["Chest", *prev_positions["Chest"], 0, 0, 0, 1])
            # === Add Hips bone (midpoint between hips) ===
            left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
            right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]

            hips_x = (left_hip.x + right_hip.x) / 2
            hips_y = (left_hip.y + right_hip.y) / 2
            hips_z = (left_hip.z + right_hip.z) / 2

            hips_pos = np.array([(hips_x - 0.5) * scale, -(hips_y - 0.5) * scale, hips_z * scale])
            prev_positions["Hips"] = smooth(prev_positions.get("Hips"), hips_pos)
            client.send_message("/VMC/Ext/Bone/Pos", ["Hips", *prev_positions["Hips"], 0, 0, 0, 1])

            # 💡 Draw the Hips point on screen
            hx, hy = int(hips_x * w), int(hips_y * h)
            cv2.circle(frame, (hx, hy), 6, (255, 255, 0), -1)
            cv2.putText(frame, "Hips", (hx + 10, hy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)

            # 💡 Draw the Chest point on screen
            cx, cy = int(chest_x * w), int(chest_y * h)
            cv2.circle(frame, (cx, cy), 6, (0, 255, 255), -1)
            cv2.putText(frame, "Chest", (cx + 10, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)


            # Send OSC message to VMC
            client.send_message("/VMC/Ext/Bone/Pos", [bone, *prev_positions[bone], 0, 0, 0, 1])

        # Draw skeleton
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    cv2.imshow("Full Body Tracking (to VMC)", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
