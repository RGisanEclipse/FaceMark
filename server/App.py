import cv2
import os
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from datetime import date
from datetime import datetime
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import joblib
import time

app = Flask(__name__)
CORS(app)
nimgs = 100


datetoday = date.today().strftime("%m_%d_%y")
datetoday2 = date.today().strftime("%d-%B-%Y")


face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


if not os.path.isdir('Attendance'):
    os.makedirs('Attendance')
if not os.path.isdir('static'):
    os.makedirs('static')
if not os.path.isdir('static/faces'):
    os.makedirs('static/faces')
if f'Attendance-{datetoday}.csv' not in os.listdir('Attendance'):
    with open(f'Attendance/Attendance-{datetoday}.csv', 'w') as f:
        f.write('Name,Roll,Time')



def totalreg():
    return len(os.listdir('static/faces'))



def extract_faces(img):
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_points = face_detector.detectMultiScale(gray, 1.2, 5, minSize=(20, 20))
        return face_points
    except:
        return []



def identify_face(facearray):
    model = joblib.load('static/face_recognition_model.pkl')
    return model.predict(facearray)



def train_model():
    faces = []
    labels = []
    userlist = os.listdir('static/faces')
    for user in userlist:
        for imgname in os.listdir(f'static/faces/{user}'):
            img = cv2.imread(f'static/faces/{user}/{imgname}')
            resized_face = cv2.resize(img, (50, 50))
            faces.append(resized_face.ravel())
            labels.append(user)
    faces = np.array(faces)
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(faces, labels)
    joblib.dump(knn, 'static/face_recognition_model.pkl')



def extract_attendance():
    df = pd.read_csv(f'Attendance/Attendance-{datetoday}.csv')
    names = df['Name']
    rolls = df['Roll']
    times = df['Time']
    l = len(df)
    return names, rolls, times, l

def extract_attendance_custom(current_date):
    df = pd.read_csv(f'Attendance/Attendance-{current_date}.csv')
    names = df['Name']
    rolls = df['Roll']
    times = df['Time']
    l = len(df)
    return names, rolls, times, l

# Add Attendance of a specific user
def add_attendance(name):
    username = name.split('_')[0]
    userid = name.split('_')[1]
    current_time = datetime.now().strftime("%H:%M:%S")

    df = pd.read_csv(f'Attendance/Attendance-{datetoday}.csv')
    if int(userid) not in list(df['Roll']):
        with open(f'Attendance/Attendance-{datetoday}.csv', 'a') as f:
            f.write(f'\n{username},{userid},{current_time}')

def get_all_attendance():
    attendanceList = os.listdir('Attendance')

    return attendanceList



def getallusers():
    userlist = os.listdir('static/faces')
    names = []
    rolls = []
    l = len(userlist)

    for i in userlist:
        name, roll = i.split('_')
        names.append(name)
        rolls.append(roll)

    return userlist, names, rolls, l



def deletefolder(duser):
    pics = os.listdir(duser)
    for i in pics:
        os.remove(duser + '/' + i)
    os.rmdir(duser)





@app.route('/')
def home():
    return jsonify({"message": "working"})

## get custom attendance
@app.route('/custom_attendance',methods = ['POST'])
def custom_attendance():
    data = request.json
    current_date = data.get('custom_date')
    names, rolls, times, l = extract_attendance_custom(current_date)
    names = names.tolist()
    rolls = rolls.tolist()
    times = times.tolist()

    return jsonify({'success': True, 'names': names, 'rolls': rolls, 'times': times, 'l': l})

## get attendance
@app.route('/attendance')
def attendance():
    names, rolls, times, l = extract_attendance()
    names = names.tolist()
    rolls = rolls.tolist()
    times = times.tolist()

    return jsonify({'success': True, 'names': names, 'rolls': rolls, 'times': times, 'l': l})

@app.route('/getAllAttendance')
def getAllAttendance():
    attendance_list = get_all_attendance()

    return jsonify({'success': True, 'Attendance':attendance_list});


## List users page
@app.route('/listusers')
def listusers():
    userlist, names, rolls, l = getallusers()

    data = {
        "userlist": userlist,
        "names": names,
        "rolls": rolls,
        "l": l,
        "totalreg": totalreg(),
        "datetoday2": datetoday2
    }

    return jsonify(data)


## Delete functionality
@app.route('/deleteuser', methods=['POST'])
def deleteuser():
    data = request.json
    duser = data.get('user')
    deletefolder('static/faces/' + duser)

    ##deleting trained file
    if os.listdir('static/faces/') == []:
        os.remove('static/face_recognition_model.pkl')

    try:
        train_model()
    except:
        pass

    userlist, names, rolls, l = getallusers()

    data = {
        "userlist": userlist,
        "names": names,
        "rolls": rolls,
        "l": l,
        "totalreg": totalreg(),
        "datetoday2": datetoday2
    }

    return jsonify(data)


# Our main Face Recognition functionality.
# This function will run when we click on Take Attendance Button.
@app.route('/start', methods=['GET'])
def start():
    # Extract attendance details
    names, rolls, times, l = extract_attendance()

    # Check if the face recognition model is trained
    if 'face_recognition_model.pkl' not in os.listdir('static'):
        return jsonify({"success": False, "message": "There is no trained model"})

    # Load the face recognition model
    model = joblib.load('static/face_recognition_model.pkl')

    # Start capturing video
    cap = cv2.VideoCapture(0)

    # Initialize a list to store the present users
    present_users = []

    # Start time
    start_time = time.time()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break

        # Detect faces in the frame
        faces = extract_faces(frame)

        # Process each detected face
        for (x, y, w, h) in faces:
            # Extract the face region
            face_region = frame[y:y+h, x:x+w]

            # Resize the face region to match the model input size
            resized_face = cv2.resize(face_region, (50, 50))

            # Flatten the face array
            face_array = resized_face.ravel().reshape(1, -1)

            # Predict the identity of the face using the model
            prediction = model.predict(face_array)[0]  # Extract the first element of the prediction array

            # Convert the prediction to a string
            prediction_str = str(prediction)

            # Get the name and roll number of the predicted user
            name, roll = prediction_str.split('_')

            # Get the current time
            current_time = datetime.now().strftime("%H:%M:%S")

            # Check if the user is already present
            if int(roll) not in rolls:
                # Add the user to the present users list
                present_users.append({"name": name, "roll": int(roll), "time": current_time})

                # Update the attendance record
                add_attendance(prediction)

                # Update the attendance details
                names, rolls, times, l = extract_attendance()

        # Check if 5 seconds have passed
        if time.time() - start_time >= 5:
            break

    # Release the video capture device and close the window
    cap.release()
    cv2.destroyAllWindows()

    # Return the list of present users
    return jsonify({"success": True, "present_users": present_users})



# A function to add a new user.
# This function will run when we add a new user.
@app.route('/add', methods=['POST'])
def add():
    data = request.json
    newusername = data.get('newusername')
    newuserid = data.get('newuserid')

    if not newusername or not newuserid:
        return jsonify({'error': 'New username or user ID missing'}), 400

    userimagefolder = 'static/faces/' + newusername + '_' + str(newuserid)
    if not os.path.isdir(userimagefolder):
        os.makedirs(userimagefolder)
    i, j = 0, 0
    image_paths = []
    cap = cv2.VideoCapture(0)
    while 1:
        _, frame = cap.read()
        faces = extract_faces(frame)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 20), 2)
            cv2.putText(frame, f'Images Captured: {i}/{nimgs}', (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 20), 2, cv2.LINE_AA)
            if j % 5 == 0:
                name = newusername + '_' + str(i) + '.jpg'
                image_path = userimagefolder + '/' + name
                cv2.imwrite(image_path, frame[y:y + h, x:x + w])
                image_paths.append(image_path)
                i += 1
            j += 1
        if j == nimgs * 5:
            break
        if cv2.waitKey(1) == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    print('Training Model')
    train_model()
    names, rolls, times, l = extract_attendance()

    names = names.tolist()
    rolls = rolls.tolist()
    times = times.tolist()

    return jsonify({'success': True, 'names': names, 'rolls': rolls, 'times': times, 'l': l, 'image_paths': image_paths})



# Our main function which runs the Flask App
if __name__ == '__main__':
    app.run(debug=True)
