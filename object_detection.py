import cv2
import numpy as np


net = cv2.dnn.readNet("yolov4.cfg", "yolov4.weights")


classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]


conf_threshold = 0.5
nms_threshold = 0.4


def detect_objects(frame):
    
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)

  
    net.setInput(blob)

    
    outs = net.forward(net.getUnconnectedOutLayersNames())

   
    class_ids = []
    confidences = []
    boxes = []

  
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            
            if confidence > conf_threshold and classes[class_id] == "person":
                # Scale the bounding box coordinates
                center_x = int(detection[0] * frame.shape[1])
                center_y = int(detection[1] * frame.shape[0])
                width = int(detection[2] * frame.shape[1])
                height = int(detection[3] * frame.shape[0])

               
                x = int(center_x - width / 2)
                y = int(center_y - height / 2)

                
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, width, height])

    
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    
    people_count = len(indices)

    
    if len(indices) > 0:
        for i in indices.flatten():
            x, y, w, h = boxes[i]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Person", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return frame, people_count
