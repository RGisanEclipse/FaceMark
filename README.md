# FaceMark

FaceMark is a camera-based attendance system leveraging facial recognition technology to automate and enhance the accuracy of attendance tracking in educational institutions, workplaces, and event organizations. The system utilizes a K-Nearest Neighbors (KNN) model for face detection and recognition, ensuring efficient and fraud-resistant attendance management.

## Features
- **Automated Attendance Tracking:** Uses high-resolution cameras and facial recognition to automate the attendance process.
- **Enhanced Accuracy and Fraud Prevention:** Reduces human error and prevents proxy attendance through precise identification.
- **Real-Time Processing:** Captures and processes images in real-time, providing immediate attendance updates.
- **Detailed Reporting:** Generates comprehensive attendance reports for better monitoring and compliance.
- **Scalability:** Designed to scale for large institutions and organizations with multiple entry points.

## Project Structure
The project is divided into three main stages:
1. **Script Development:** Core functionality for capturing images and performing facial recognition using Python, OpenCV, and Joblib.
2. **Backend Server Creation and Script Optimization:** Setting up a server to handle client requests and optimize the facial recognition script.
3. **Frontend Server Development:** Developing a user-friendly web interface for administrators and end-users to interact with the system.

## Technologies Used
- **Python:** Core programming language for developing the backend and facial recognition algorithms.
- **Flask:** Micro web framework used for creating the backend server.
- **OpenCV:** Library used for real-time computer vision tasks.
- **Joblib:** Used for serializing Python objects, particularly for saving and loading models.
- **React.js:** JavaScript library for building the user interface.

## Installation
To set up FaceMark on your local machine, follow these steps:

 1. **Clone the repository:**
    
	 ```bash
    git clone https://github.com/RGisanEclipse/FaceMark.git
    cd FaceMark
    ```
 2. **Set up the Back End Server:**
    
	 - Ensure you have Flask and other dependencies installed.
	 - Run the Back End Server Script:

	 ```bash
    python App.py
    ```
 3. **Set up the Front End Server:**
    
	 - Ensure you have Node.js installed.
	 - Navigate to the client directory and install dependencies:

	 ```bash
    cd client
    npm install
    ```
  
    - Start the server:
      
     ```bash
    npm run dev
    ```
 ## Usage
1. **Starting the System:**
   - Ensure both backend and frontend servers are running.
   - Access the web interface through your browser.

2. **Admin Interface:**
   - Use the admin panel to manage user profiles, view attendance records, and perform administrative tasks.

3. **Capturing Attendance:**
   - Cameras capture images of individuals as they pass by.
   - The system processes the images in real-time and marks attendance based on facial recognition.

## Future Scope
- **Improved Accuracy:** Enhance facial recognition algorithms to improve accuracy in various conditions.
- **Mobile Integration:** Develop mobile applications for on-the-go attendance tracking.
- **Advanced Analytics:** Integrate analytics to provide insights on attendance patterns and trends.

