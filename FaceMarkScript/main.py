import cv2
import os
import numpy as np
import sqlite3
import datetime

# Connect to SQLite database
conn = sqlite3.connect('attendance.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS attendance
             (id INTEGER PRIMARY KEY, name TEXT, status TEXT, time TEXT)''')
conn.commit()


# Function to insert attendance record into the database
def insert_attendance_record(name, status):
    # Get current date and time
    now = datetime.datetime.now()
    time_str = now.strftime("%Y-%m-%d %H:%M:%S")

    # Insert record into the database
    c.execute("INSERT INTO attendance (name, status, time) VALUES (?, ?, ?)", (name, status, time_str))
    conn.commit()


# Function to display attendance records from the database
def display_attendance_records():
    # Retrieve all records from the database
    c.execute("SELECT * FROM attendance")
    records = c.fetchall()

    # Print header
    print("\nAttendance Records:")
    print("ID\tName\tStatus\tTime")
    print("-" * 30)

    # Print each record
    for record in records:
        print(f"{record[0]}\t{record[1]}\t{record[2]}\t{record[3]}")


# Function to capture and save an image
def capture_and_save_image(folder, name):
    # Start video capture
    cam = cv2.VideoCapture(0)

    while True:
        # Read frame from camera
        ret, frame = cam.read()
        if not ret:
            print("Error: Unable to capture video.")
            break

        # Display the frame
        cv2.imshow('Capture Image', frame)

        # Press 'c' to capture image
        if cv2.waitKey(1) & 0xFF == ord('c'):
            # Create folder if it doesn't exist
            if not os.path.exists(folder):
                os.makedirs(folder)

            # Save the captured image
            img_path = os.path.join(folder, f'{name}.jpg')
            cv2.imwrite(img_path, frame)
            print(f"Image captured and saved as: {img_path}")
            break

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all windows
    cam.release()
    cv2.destroyAllWindows()


# Function to load images from a folder
def load_images_from_folder(folder):
    images = []
    names = []
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        img = cv2.imread(img_path)
        if img is not None:
            images.append(img)
            names.append(os.path.splitext(filename)[0])  # Extract name from filename
    return names, images


# Function for marking attendance using facial recognition
def mark_attendance(known_names, known_images):
    # Load the cascade classifier file for face detection
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Start video capture
    cam = cv2.VideoCapture(0)

    # Set to keep track of already marked persons
    marked_persons = set()

    while True:
        # Read frame from camera
        ret, frame = cam.read()
        if not ret:
            print("Error: Unable to capture video.")
            break

        # Convert frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            # Draw rectangle around the detected face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Perform facial recognition
            for name, known_img in zip(known_names, known_images):
                # Resize the known image to match the size of the detected face
                resized_known_img = cv2.resize(known_img, (w, h))

                # Convert images to grayscale for comparison
                gray_known_img = cv2.cvtColor(resized_known_img, cv2.COLOR_BGR2GRAY)
                gray_detected_img = gray[y:y + h, x:x + w]

                # Calculate absolute difference between images
                diff = cv2.absdiff(gray_known_img, gray_detected_img)

                # Calculate mean squared error
                mse = np.mean(diff)

                # If mean squared error is below threshold, recognize the face
                if mse < 100:
                    # Check if the person is already marked
                    if name not in marked_persons:
                        print(f"Attendance marked for: {name}")

                        # Display name above the rectangle
                        cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                        # Insert attendance record into the database
                        insert_attendance_record(name, "Present")

                        # Add the person to the marked set
                        marked_persons.add(name)

        # Display the frame with detected faces
        cv2.imshow('Mark Attendance', frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all windows
    cam.release()
    cv2.destroyAllWindows()


# Main function
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
