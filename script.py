import cv2
import sys
from random import randint 

# Video que será monitorado
cap = cv2.VideoCapture('source/carros.mp4')

# Pega primeiro frame do video, para definir objetos que serão monitorados
ok, frame = cap.read()
if not ok:
    print('Não foi possivel ler o arquivo')
    sys.exit(1)

bboxes = [] # Objetos de interesse no  video
colors = [] 

while True:
    bbox = cv2.selectROI('Tracker', frame)
    bboxes.append(bbox)
    colors.append((randint(0,255),randint(0,255),randint(0,255)))
    print('Pressione Q para sair ou qualquer tecla para selecionar o próximo objeto')
    k = cv2.waitKey(0) & 0XFF
    if (k == 113):
        break

# print('bboxes > ', bboxes)

multiTracker = cv2.legacy.MultiTracker_create()
# Para cada objeto de interesse criar um tracker que
# será responsável em monitorar o objeto o qual ele é responsável
for bbox in bboxes:
  multiTracker.add(cv2.legacy.TrackerCSRT_create(), frame, bbox)


# Roda o vídeo e monitora os objetos nele
while cap.isOpened():
    ok, frame = cap.read()   
    if not ok:
        break
    
    ok, boxes = multiTracker.update(frame)

    for i, newBox in enumerate(boxes):
        (x,y,w,h) = [int(v) for v in newBox]
        cv2.rectangle(frame, (x,y), (x+w, y+h), colors[i], 2, 1)
    
    cv2.imshow('MultiTracker', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break