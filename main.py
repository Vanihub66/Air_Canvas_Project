import cv2
import mediapipe as mp
import numpy as np
import math
import time


# =========================================================
# FROSTWRITE - ICE BLUE AIR CANVAS
# =========================================================

WIDTH = 1280
HEIGHT = 720

BRUSH_SIZE = 7
ERASER_SIZE = 50

COLORS = {
    "ICE BLUE": (255, 180, 70),
    "PURPLE": (180, 70, 255),
    "PINK": (255, 80, 180),
    "GREEN": (80, 220, 100)
}

current_color = "ICE BLUE"
BRUSH_COLOR = COLORS[current_color]

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils


# =========================================================
# CAMERA
# =========================================================

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)


# =========================================================
# CANVAS
# =========================================================

canvas = np.zeros(
    (HEIGHT, WIDTH, 3),
    dtype=np.uint8
)

previous_point = None


# =========================================================
# DISTANCE
# =========================================================

def distance(p1, p2):

    return math.sqrt(
        (p1[0] - p2[0]) ** 2 +
        (p1[1] - p2[1]) ** 2
    )


# =========================================================
# FINGER DETECTION
# =========================================================

def fingers_status(hand):

    lm = hand.landmark

    index_up = lm[8].y < lm[6].y
    middle_up = lm[12].y < lm[10].y
    ring_up = lm[16].y < lm[14].y
    pinky_up = lm[20].y < lm[18].y

    return (
        index_up,
        middle_up,
        ring_up,
        pinky_up
    )


# =========================================================
# ICE BLUE EFFECT
# =========================================================

def draw_ice_energy(frame, p1, p2):

    x1, y1 = p1
    x2, y2 = p2

    dx = x2 - x1
    dy = y2 - y1

    length = math.sqrt(dx * dx + dy * dy)

    if length == 0:
        return frame

    nx = -dy / length
    ny = dx / length

    t = time.time()

    pulse = 0.5 + 0.5 * math.sin(t * 6)

    # =====================================================
    # BIG BLUE GLOW
    # =====================================================

    glow = np.zeros_like(frame)

    points = []

    for i in range(101):

        progress = i / 100

        x = x1 + dx * progress
        y = y1 + dy * progress

        wave = math.sin(
            progress * 18 +
            t * 8
        )

        wave *= 12 + 10 * pulse

        x += nx * wave
        y += ny * wave

        points.append((int(x), int(y)))

    points = np.array(points, dtype=np.int32)

    # Huge glow
    cv2.polylines(
        glow,
        [points],
        False,
        (255, 120, 20),
        55,
        cv2.LINE_AA
    )

    # Medium glow
    cv2.polylines(
        glow,
        [points],
        False,
        (255, 200, 60),
        30,
        cv2.LINE_AA
    )

    frame = cv2.addWeighted(
        frame,
        1.0,
        glow,
        0.45,
        0
    )

    # =====================================================
    # ICE ENERGY STRANDS
    # =====================================================

    for strand in range(9):

        strand_points = []

        for i in range(101):

            progress = i / 100

            x = x1 + dx * progress
            y = y1 + dy * progress

            wave = math.sin(
                progress * 25 +
                t * 10 +
                strand
            )

            wave *= 5 + 8 * pulse

            spread = (strand - 4) * 4

            x += nx * (wave + spread)
            y += ny * (wave + spread)

            strand_points.append(
                (int(x), int(y))
            )

        strand_points = np.array(
            strand_points,
            dtype=np.int32
        )

        # Outer blue
        cv2.polylines(
            frame,
            [strand_points],
            False,
            (255, 100, 0),
            14,
            cv2.LINE_AA
        )

        # Ice blue
        cv2.polylines(
            frame,
            [strand_points],
            False,
            (255, 220, 100),
            6,
            cv2.LINE_AA
        )

        # White core
        cv2.polylines(
            frame,
            [strand_points],
            False,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

    # =====================================================
    # ICE PARTICLES
    # =====================================================

    for i in range(80):

        progress = (
            i / 80 +
            t * 0.12
        ) % 1

        x = x1 + dx * progress
        y = y1 + dy * progress

        wave = math.sin(
            t * 5 + i
        ) * 25

        x += nx * wave
        y += ny * wave

        radius = 1 + (i % 4)

        cv2.circle(
            frame,
            (int(x), int(y)),
            radius,
            (220, 250, 255),
            -1,
            cv2.LINE_AA
        )

    # =====================================================
    # SPARKLES
    # =====================================================

    for i in range(25):

        progress = (
            i * 0.041 +
            t * 0.08
        ) % 1

        x = int(x1 + dx * progress)
        y = int(y1 + dy * progress)

        size = int(
            4 +
            5 * math.sin(t * 7 + i)
        )

        size = max(size, 2)

        cv2.line(
            frame,
            (x - size, y),
            (x + size, y),
            (230, 250, 255),
            2,
            cv2.LINE_AA
        )

        cv2.line(
            frame,
            (x, y - size),
            (x, y + size),
            (230, 250, 255),
            2,
            cv2.LINE_AA
        )

    # =====================================================
    # ICE CRYSTALS ON HANDS
    # =====================================================

    for px, py in [p1, p2]:

        crystal_size = int(
            25 + 12 * pulse
        )

        for angle in range(0, 360, 60):

            rad = math.radians(angle)

            ex = int(
                px +
                math.cos(rad) *
                crystal_size
            )

            ey = int(
                py +
                math.sin(rad) *
                crystal_size
            )

            cv2.line(
                frame,
                (px, py),
                (ex, ey),
                (180, 240, 255),
                3,
                cv2.LINE_AA
            )

        # Bright center
        cv2.circle(
            frame,
            (px, py),
            int(12 + 5 * pulse),
            (240, 255, 255),
            -1,
            cv2.LINE_AA
        )

        # Outer ring
        cv2.circle(
            frame,
            (px, py),
            int(28 + 10 * pulse),
            (160, 230, 255),
            3,
            cv2.LINE_AA
        )

    return frame


# =========================================================
# MEDIAPIPE
# =========================================================

with mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
) as hands:

    while True:

        success, frame = cap.read()

        if not success:
            print("Camera nahi mil raha!")
            break

        # Mirror
        frame = cv2.flip(frame, 1)

        frame = cv2.resize(
            frame,
            (WIDTH, HEIGHT)
        )

        # =================================================
        # HAND PROCESSING
        # =================================================

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = hands.process(rgb)

        mode = "IDLE"

        hand_centers = []

        # =================================================
        # HAND DETECTED
        # =================================================

        if results.multi_hand_landmarks:

            for hand in results.multi_hand_landmarks:

                mp_draw.draw_landmarks(
                    frame,
                    hand,
                    mp_hands.HAND_CONNECTIONS
                )

                palm = hand.landmark[9]

                px = int(
                    palm.x * WIDTH
                )

                py = int(
                    palm.y * HEIGHT
                )

                hand_centers.append(
                    (px, py)
                )

            # =================================================
            # TWO HAND ICE MODE
            # =================================================

            ice_active = False

            if len(hand_centers) >= 2:

                hand1 = hand_centers[0]
                hand2 = hand_centers[1]

                hand_distance = distance(
                    hand1,
                    hand2
                )

                cv2.putText(
                    frame,
                    f"Distance: {int(hand_distance)}",
                    (900, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (220, 250, 255),
                    2
                )

                # IMPORTANT:
                # 91, 200, 400 etc = ICE
                # 690+ = no ICE

                if hand_distance < 700:

                    ice_active = True

                    mode = "ICE LINK"

                    frame = draw_ice_energy(
                        frame,
                        hand1,
                        hand2
                    )

            # =================================================
            # NORMAL DRAW / ERASE
            # =================================================

            if not ice_active:

                hand = results.multi_hand_landmarks[0]

                (
                    index_up,
                    middle_up,
                    ring_up,
                    pinky_up
                ) = fingers_status(hand)

                index_tip = hand.landmark[8]

                x = int(
                    index_tip.x * WIDTH
                )

                y = int(
                    index_tip.y * HEIGHT
                )

                # =================================================
                # DRAW
                # =================================================

                if (
                    index_up
                    and not middle_up
                    and not ring_up
                    and not pinky_up
                ):

                    mode = "DRAW"

                    cv2.circle(
                        frame,
                        (x, y),
                        12,
                        (180, 235, 255),
                        -1
                    )

                    cv2.circle(
                        frame,
                        (x, y),
                        6,
                        (255, 255, 255),
                        -1
                    )

                    if previous_point is not None:

                        cv2.line(
                            canvas,
                            previous_point,
                            (x, y),
                            BRUSH_COLOR,
                            BRUSH_SIZE,
                            cv2.LINE_AA
                        )

                    previous_point = (x, y)

                # =================================================
                # ERASE
                # =================================================

                elif (
                    index_up
                    and middle_up
                    and ring_up
                    and pinky_up
                ):

                    mode = "ERASE"

                    previous_point = None

                    cv2.circle(
                        frame,
                        (x, y),
                        ERASER_SIZE,
                        (220, 250, 255),
                        2
                    )

                    mask = np.zeros(
                        canvas.shape[:2],
                        dtype=np.uint8
                    )

                    cv2.circle(
                        mask,
                        (x, y),
                        ERASER_SIZE,
                        255,
                        -1
                    )

                    canvas[mask == 255] = 0

                else:

                    mode = "IDLE"
                    previous_point = None

        else:

            previous_point = None

        # =================================================
        # ADD CANVAS
        # =================================================

        frame = cv2.add(
            frame,
            canvas
        )

        # =================================================
        # HEADER
        # =================================================

        cv2.rectangle(
            frame,
            (20, 20),
            (450, 105),
            (12, 18, 28),
            -1
        )

        cv2.rectangle(
            frame,
            (20, 20),
            (450, 105),
            (140, 225, 255),
            2
        )

        cv2.putText(
            frame,
            "FROSTWRITE",
            (40, 55),
            cv2.FONT_HERSHEY_DUPLEX,
            0.9,
            (235, 250, 255),
            2
        )

        cv2.putText(
            frame,
            "MODE: " + mode,
            (40, 88),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (180, 230, 255),
            2
        )

        # =================================================
        # ICE ACTIVE
        # =================================================

        if mode == "ICE LINK":

            cv2.putText(
                frame,
                "ICE ENERGY ACTIVE",
                (850, 55),
                cv2.FONT_HERSHEY_DUPLEX,
                0.7,
                (220, 250, 255),
                2
            )
        # =========================================================
        # COLOR PANEL
        # =========================================================

        cv2.rectangle(
            frame,
            (850, 570),
            (1250, 660),
            (12, 18, 28),
            -1
        )

        cv2.rectangle(
            frame,
            (850, 570),
            (1250, 660),
            (140, 225, 255),
            2
        )

        cv2.putText(
            frame,
            "BRUSH COLOR",
            (875, 600),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (235, 250, 255),
            2
        )

        cv2.putText(
            frame,
            current_color,
            (875, 635),
            cv2.FONT_HERSHEY_DUPLEX,
            0.65,
            BRUSH_COLOR,
            2
        )

        cv2.putText(
            frame,
            "1 BLUE   2 PURPLE   3 PINK   4 GREEN",
            (850, 690),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.42,
            (255, 255, 255),
            1
        )
        # =================================================
        # CONTROLS
        # =================================================

        cv2.putText(
            frame,
            "INDEX = DRAW",
            (30, 680),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1
        )

        cv2.putText(
            frame,
            "PALM = ERASE",
            (230, 680),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1
        )

        cv2.putText(
            frame,
            "C = CLEAR",
            (430, 680),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1
        )

        cv2.putText(
            frame,
            "Q = QUIT",
            (600, 680),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1
        )

        # =================================================
        # SHOW
        # =================================================

        cv2.imshow(
            "FrostWrite - Magical Ice Canvas",
            frame
        )

        key = cv2.waitKey(1) & 0xFF
        if key == ord("1"):
            current_color = "ICE BLUE"
            BRUSH_COLOR = COLORS[current_color]

        elif key == ord("2"):
            current_color = "PURPLE"
            BRUSH_COLOR = COLORS[current_color]

        elif key == ord("3"):
            current_color = "PINK"
            BRUSH_COLOR = COLORS[current_color]

        elif key == ord("4"):
            current_color = "GREEN"
            BRUSH_COLOR = COLORS[current_color]

        if key == ord("q"):
            break

        if key == ord("c"):

            canvas = np.zeros(
                (HEIGHT, WIDTH, 3),
                dtype=np.uint8
            )


# =========================================================
# CLOSE
# =========================================================

cap.release()
cv2.destroyAllWindows()