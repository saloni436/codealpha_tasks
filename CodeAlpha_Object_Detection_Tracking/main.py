
import argparse
import cv2
import torch
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Object Detection and Tracking"
    )
    parser.add_argument("--source", default="0",
                        help="Webcam index or video file path")
    parser.add_argument("--model", default="yolov8n.pt",
                        help="YOLO model filename")
    parser.add_argument("--conf", type=float, default=0.4,
                        help="Detection confidence threshold")
    parser.add_argument("--width", type=int, default=640,
                        help="Frame width; use 0 to disable resizing")
    return parser.parse_args()


def main():
    args = parse_arguments()

    if not 0 <= args.conf <= 1:
        raise ValueError("--conf must be between 0 and 1")
    if args.width < 0:
        raise ValueError("--width cannot be negative")

    device = 0 if torch.cuda.is_available() else "cpu"
    print(f"Using {'GPU' if device == 0 else 'CPU'}")

    print("Loading YOLO model...")
    model = YOLO(args.model)
    tracker = DeepSort(max_age=30)

    source = int(args.source) if args.source.isdigit() else args.source
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print(f"Error: Could not open video source: {args.source}")
        return

    print("Video started. Press 'q' to quit.")

    try:
        while True:
            success, frame = cap.read()
            if not success:
                print("Video ended or frame could not be read.")
                break

            if args.width and frame.shape[1] > args.width:
                height = int(args.width * frame.shape[0] / frame.shape[1])
                frame = cv2.resize(frame, (args.width, height))

            results = model.predict(
                frame, conf=args.conf, device=device, verbose=False
            )

            detections = []
            for box in results[0].boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().tolist()
                confidence = float(box.conf[0].cpu())
                class_id = int(box.cls[0].cpu())
                class_name = model.names[class_id]

                detections.append((
                    [x1, y1, x2 - x1, y2 - y1],
                    confidence,
                    class_name
                ))

            tracks = tracker.update_tracks(detections, frame=frame)

            for track in tracks:
                if not track.is_confirmed() or track.time_since_update > 0:
                    continue

                left, top, right, bottom = map(int, track.to_ltrb())
                left = max(0, left)
                top = max(0, top)
                right = min(frame.shape[1] - 1, right)
                bottom = min(frame.shape[0] - 1, bottom)

                if right <= left or bottom <= top:
                    continue

                class_name = track.get_det_class() or "object"
                confidence = track.get_det_conf()
                confidence_text = (
                    f"{float(confidence):.2f}"
                    if confidence is not None else "N/A"
                )
                label = (
                    f"ID {track.track_id} | {class_name} | "
                    f"Conf: {confidence_text}"
                )

                color = (60, 220, 90)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(
                    frame, label, (left, max(22, top - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2
                )

            cv2.imshow("Object Detection and Tracking", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Video resources released.")


if __name__ == "__main__":
    main()
