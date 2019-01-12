import face_recognition
import cv2


#Load video stream
video_capture = cv2.VideoCapture(0)

#set up recognised people
josh_image = face_recognition.load_image_file("/home/josh/Downloads/josh-irish/front.jpg")
josh_face = face_recognition.face_encodings(josh_image)[0]
charlotte_image = face_recognition.load_image_file("/home/josh/Downloads/charlotte-bundy/front.jpg")
charlotte_face = face_recognition.face_encodings(charlotte_image)[0]
dan_image = face_recognition.load_image_file("/home/josh/Downloads/dan.jpg")
dan_face = face_recognition.face_encodings(dan_image)[0]
faces = [josh_face,charlotte_face,dan_face]
names = ["Josh","Charlotte","Dan"]

#save video
width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (width, height))
#out = cv2.VideoWriter('output.avi', -1, 20.0, (640,480))

#initialise
face_locations = []
face_encodings = []
face_names = []
frame_count = 0

while True:
    # get a frame
    ret, frame = video_capture.read()

   
    #optimise picture
    #small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    rgb_small_frame = frame[:, :, ::-1]#small_frame[:, :, ::-1]
    #rgb_small_frame = cv2.cvtColor(rgb_small_frame, cv2.COLOR_BGR2GRAY)

    #only bother check 1 frame every 10
    if frame_count == 0:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:
        
            #check known faces for a match
            matches = face_recognition.compare_faces(faces, face_encoding)
            #print(matches)
            name = ""#default blank if unknown

            
            if True in matches:
                first_match_index = matches.index(True)
                name = names[first_match_index]

            face_names.append(name)

    
    frame_count += 1
    #print(frame_count)
    if frame_count == 10: 
        frame_count = 0
 

    #dsiplay results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        #change position depending on scale
        #top *= 2
        #right *= 2
        #bottom *= 2
        #left *= 2


        #put name below face
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom + 45), font, 1.0, (0, 0, 255), 1)

    cv2.imshow('Video', frame)
    out.write(frame)

    #q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


video_capture.release()
out.release()
cv2.destroyAllWindows()