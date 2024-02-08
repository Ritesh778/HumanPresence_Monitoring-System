import cv2
import streamlit as st
from datetime import datetime
import time
from object_detection import detect_objects
from database import initialize_table, insert_image
import psycopg2

def initialize_app():
    st.title("Real-Time Object Detection with RTSP Camera")
    st.sidebar.title("Database Configuration")


    db_host = st.sidebar.text_input("Host", "localhost")
    db_name = st.sidebar.text_input("Database Name", "Object data")
    db_user = st.sidebar.text_input("Username", "postgres")
    db_password = st.sidebar.text_input("Password", "0507", type="password")

    try:
        connection = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password
        )
        connection.close()
        st.sidebar.success("Database connection successful!")
    except psycopg2.OperationalError as e:
        st.sidebar.error("Database connection failed.")

    
    initialize_table()

    
    cap = cv2.VideoCapture('url', cv2.CAP_FFMPEG)
     
    if not cap.isOpened():
        st.error("Error: RTSP Camera not found or cannot be accessed.")
        return

    #
    prev_time = datetime.now()

    
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        
        curr_time = datetime.now()
        time_diff = curr_time - prev_time

        
        if time_diff.total_seconds() >= 30:
            prev_time = curr_time

            
            processed_frame, people_count = detect_objects(frame)

            
            st.image(processed_frame, channels="BGR", caption="Processed Frame", use_column_width=True)

            
            insert_image(curr_time, processed_frame, people_count)

            
            st.subheader("People Count")
            st.write("Capture Time:", curr_time)
            st.write("Total Count:", people_count)

        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    
    cap.release()
    cv2.destroyAllWindows()
   



if __name__ == "__main__":
    initialize_app()
