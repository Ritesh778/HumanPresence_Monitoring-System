import psycopg2
import numpy as np
import io
import cv2
from datetime import datetime

def connect_to_db():
    connection = psycopg2.connect(
        host="localhost",
        database="Object data",
        user="postgres",
        password="0507"
    )
    cursor = connection.cursor()
    return connection, cursor

def initialize_table():
    connection, cursor = connect_to_db()
    cursor.execute("CREATE TABLE IF NOT EXISTS rtsp_data (id SERIAL PRIMARY KEY, capture_time TIMESTAMP, image BYTEA, count INTEGER)")
    connection.commit()
    cursor.close()
    connection.close()

def insert_image(capture_time, image, count):
    connection, cursor = connect_to_db()
    _, image_data = cv2.imencode('.jpg', image)
    image_bytes = np.array(image_data).tobytes()

    cursor.execute("INSERT INTO rtsp_data (count, capture_time, image) VALUES (%s, %s, %s)", (count, capture_time, psycopg2.Binary(image_bytes)))
    connection.commit()
    cursor.close()
    connection.close()

