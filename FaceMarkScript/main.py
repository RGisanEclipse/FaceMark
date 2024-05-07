import cv2
import os
import numpy as np
import sqlite3
import datetime

conn = sqlite3.connect('attendance.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS attendance
             (id INTEGER PRIMARY KEY, name TEXT, status TEXT, time TEXT)''')
conn.commit()


def insert_attendance_record(name, status):
    now = datetime.datetime.now()
    time_str = now.strftime("%Y-%m-%d %H:%M:%S")

    c.execute("INSERT INTO attendance (name, status, time) VALUES (?, ?, ?)", (name, status, time_str))
    conn.commit()


def display_attendance_records():
    c.execute("SELECT * FROM attendance")
    records = c.fetchall()

    print("\nAttendance Records:")
    print("ID\tName\tStatus\tTime")
    print("-" * 30)

    for record in records:
        print(f"{record[0]}\t{record[1]}\t{record[2]}\t{record[3]}")


def capture_and_save_image(folder, name):
    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Error: Unable to capture video.")
            break

        cv2.imshow('Capture Image', frame)

        if cv2.waitKey(1) & 0xFF == ord('c'):
            if not os.path.exists(folder):
                os.makedirs(folder)

            img_path = os.path.join(folder, f'{name}.jpg')
            cv2.imwrite(img_path, frame)
            print(f"Image captured and saved as: {img_path}")
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


def load_images_from_folder(folder):
    images = []
    names = []
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        img = cv2.imread(img_path)
        if img is not None:
            images.append(img)
            names.append(os.path.splitext(filename)[0])
    return names, images


def mark_attendance(known_names, known_images):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    cam = cv2.VideoCapture(0)

    marked_persons = set()

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Error: Unable to capture video.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            for name, known_img in zip(known_names, known_images):
                resized_known_img = cv2.resize(known_img, (w, h))

                gray_known_img = cv2.cvtColor(resized_known_img, cv2.COLOR_BGR2GRAY)
                gray_detected_img = gray[y:y + h, x:x + w]

                diff = cv2.absdiff(gray_known_img, gray_detected_img)

                mse = np.mean(diff)

                if mse < 100:
                    if name not in marked_persons:
                        print(f"Attendance marked for: {name}")

                        cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                        insert_attendance_record(name, "Present")

                        marked_persons.add(name)

        cv2.imshow('Mark Attendance', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


def main():
    while True:
        print("\nOptions:")
        print("1. Capture and Save Image")
        print("2. Mark Attendance")
        print("3. View Attendance Records")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == '1':
            name = input("Enter the name of the person: ")
            capture_and_save_image('known_faces', name)
        elif choice == '2':
            known_names, known_images = load_images_from_folder('known_faces')
            mark_attendance(known_names, known_images)
            print("Attendance marked.")
        elif choice == '3':
            display_attendance_records()
        elif choice == '4':
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()
