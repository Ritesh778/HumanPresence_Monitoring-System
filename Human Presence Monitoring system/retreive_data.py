import psycopg2
from openpyxl import Workbook
from openpyxl.drawing.image import Image
import io

connection = psycopg2.connect(
    host="localhost",
    database="Object data",
    user="postgres",
    password="0507"
)

cursor = connection.cursor()

cursor.execute("SELECT id, capture_time, image FROM rtsp_data, count")
records = cursor.fetchall()

workbook = Workbook()
sheet = workbook.active

sheet.column_dimensions['A'].width = 10
sheet.column_dimensions['B'].width = 20
sheet.column_dimensions['C'].width = 100
sheet.column_dimensions['D'].width = 10

sheet['A1'] = "ID"
sheet['B1'] = "Capture Time"
sheet['C1'] = "Image"
sheet['D1'] = "Count"

for index, record in enumerate(records, start=2):
    record_id = record[0]
    capture_time = record[1]
    image_bytes = record[2]
    count= record[3]

    image_data = io.BytesIO(image_bytes)

    img = Image(image_data)

    img.width = 90
    img.height = 120

    sheet.row_dimensions[index].height = 150
    sheet.add_image(img, f'C{index}')

    sheet[f'A{index}'] = record_id
    sheet[f'B{index}'] = capture_time
    sheet[f'D{index}'] = count

workbook.save("rtsp_data_with_images.xlsx")

cursor.close()
connection.close()





