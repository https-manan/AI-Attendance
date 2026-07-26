import dlib
import hyperframe
import numpy as np
import face_recognition_models
from sklearn.svm import SVC, SVM
import streamlit as st 
from src.database.db import get_all_students


@st.cache_resource
def load_dlib_models():
    detector=dlib.get_frontal_face_detector()                         #This tell how many faces and there location no inner detail of face
    sp=dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()       #basically dlib_shape_predictor mai hume model pass karna hota hai
    )                                                                  #sp is for shape predictor which gonna predict the landmarks of face like shape and features
    faceRec=dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()      #basically isme bhi hum model pass krte hai in face_recognition_model_v1 for better performance
    )

    return detector,sp,faceRec



def get_face_embeddings(image_np):          # basiclly this is to convert the face image in form of vector and num  
    detector,sp,faceRec=load_dlib_models()
    faces=detector(image_np,2)  #Here this 2 number means that 1 image ko kitni baar process krega like 2 means 2 baar may be from diff angls and pos
    encoding=[]
    for face in faces:
        shape=sp(image_np,face) # this means we are demanding give me all landmarks of this image aand in that image this particulr face like group photo me se is face ke embeddings
        face_desc=faceRec.compute_face_descriptor(image_np,shape,1) #To aab ye finally 128 Dimention ki embeddings bna dega finally from the image landmarks for that particular face
        encoding.append(np.array(face_desc))
    return encoding  # basically face ko ek number bna dia and append that in the encoding 



@st.cache_resource
def get_trained_model():  #so this is for DB se saare students nikalke unpe train kr dega 
    X=[]  #x is for tracking the embedding of the student 
    Y=[]  #Y is for tracking the name or id of that student 
    student_db=get_all_students()
    if not student_db:
        return None 
    for student in student_db:
        embedding=student.get('face_embedding')
        if embedding:
            X.append(np.array())
            Y.append(student.get('student_id'))
    if len(X)==0:
        return 0
    clf=SVC(kernel='linear',probability=True,class_weight='balanced')#this is classifier we are using CSV as classifier
    try:
        clf.fit(X,Y)
    except ValueError:
        pass
    return {"clf":clf,"X":X,"Y":Y}

def train_classifier():
    st.cache_resource.clear()
    model_data=get_trained_model()
    return bool(model_data)

def predict_attandace(class_image_np):
    encodings=get_face_embeddings(class_image_np)
    detected_student={}
    model_data=get_trained_model()
    if not model_data:
        return detected_student,[],len(encodings)
    clf=model_data['clf']
    X_train=model_data['X']
    Y_train=model_data['Y']

    all_students=sorted(list(set(Y_train)))

    for encoding in encodings:
        if len(all_students) >= 2:
            predicted_id = int(clf.predict([encoding])[0])
        else:
            predicted_id = int(all_students[0])
        student_embedding = X_train[Y_train.index(predicted_id)]
        best_match_score = np.linalg.norm(student_embedding - encoding)
        resemblance_threshold = 0.6
        if best_match_score <= resemblance_threshold:
            detected_student[predicted_id] = True
    return detected_student, all_students, len(encoding)