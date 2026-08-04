import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st
from src.database.db import get_all_students



@st.cache_resource  # coz these models are heavy so we gonna load only once and save in cache
def load_dlib_models():
    detector=dlib.get_frontal_face_detector()                #This tell how many faces and there location no inner detail of face

    sp=dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()       #basically dlib_shape_predictor mai hume model pass karna hota hai
    )                                                                  #sp is for shape predictor which gonna predict the landmarks of face like shape and features

    faceRec=dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()      #basically isme bhi hum model pass krte hai in face_recognition_model_v1 for better performance
    )

    return detector,sp,faceRec



def get_face_embeddings(image_np):        # basiclly this is to convert the face image in form of vector and num  
    detector,sp,faceRec=load_dlib_models()

    faces=detector(image_np,2)  #Here this 2 number means that 1 image ko kitni baar process krega like 2 means 2 baar from diff angls and pos

    encoding=[]

    for face in faces:
        shape=sp(image_np,face) # this means we are demanding give me all landmarks of this image aand in that image this particulr face like group photo me se is face ke embeddings
        face_desc=faceRec.compute_face_descriptor(image_np,shape,1) #To aab ye finally 128 Dimention ki embeddings bna dega finally from the image landmarks for that particular face
        encoding.append(np.array(face_desc))

    return encoding  # basically face ko ek number bna dia and append that in the encoding 



@st.cache_resource
def get_trained_model():  #so this is for DB se saare students nikalke unpe model ko train kr dega using SVC classifier
    X=[]  #x is for tracking the embedding of the student 
    Y=[]  #Y is for tracking the name or id of that student 
    #coz model x and y leta hai like student and its embeddings 

    students=get_all_students()
    if not students:
        return None
    for s in students:
        emb=s.get('face_embedding')
        if emb:
            X.append(np.array(emb))
            Y.append(s.get('student_id'))

    if len(X)==0: # agr kisi ki embeddings nahi mili to bhi return 0
        return 0

    #this is classifier we are using CSV as classifier
    clf=SVC(kernel='linear',probability=True,class_weight='balanced')
    try:
        clf.fit(X,Y)
    except ValueError:
        pass
    return {"clf":clf,"X":X,"Y":Y}




#basically this is for ki jb nya data aa gya to purene cached data ko clear krke get new udpated data and get it cached
def train_classifier():
    st.cache_resource.clear()
    model_data=get_trained_model()
    return bool(model_data)


#This gonna finally predict the attandace from the group photo
def predict_attandace(class_image_np):
    encodings=get_face_embeddings(class_image_np)# saare baccho from group photo ki phase embeddings bna dega
    detected_student={}
    model_data=get_trained_model()  #ye hum saare embeddings jo aabhi tk DB maai store hai vo leke aaye hai
    if not model_data:
        return detected_student,[],0  #so 1st one is students embeddings,2nd is list of them and there IDs and 3rd is no of students 

    clf=model_data['clf']     #bascically getting classifier val and X and Y from the model 
    X_train=model_data['X']
    Y_train=model_data['Y']

    all_students=sorted(list(set(Y_train))) #saare students getting them all 

    for encoding in encodings:                #basically yha hum aapne classifier se puch rhe hai ki ye banda grp photo mai hai kya hai to okey varna aage bhadenge 
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