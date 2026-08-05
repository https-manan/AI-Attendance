import streamlit as st
import numpy as np
import io 
import librosa
from resemblyzer import VoiceEncoder,preprocess_wav


@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()  # basically voice encoders ko cache krne ke lie



def get_voice_embedding(audio_bytes):  #audio_bytes means audio ka binary
    try:
        encoder=load_voice_encoder()
        audio,sr=librosa.load(io.BytesIO(audio_bytes),sr=16000) #librosa return 2 things audio and sample rate
        wav=preprocess_wav(audio)      #preprocess_wev is to cleaning the audio  
        embedding=encoder.ember_utterance(wav)  #cleaned audio(wav) file daalte haai to ye embeeddings de deta hai
        return embedding.tolist()#image vale mai 128D tha idhr 256D mai embedd hua hai
    
    except Exception as e:
        st.error('Voice rec error')
        return None



#This is to match the audio to yha audio lenge and uske embedding nikalenge and match with all preloaded embedding in DB
def identify_speaker(new_embedding, candidates_dict, threshold=0.65): #yhaa pr this threshold is for ki dot product se nikalte hai matching and agar iss se km aayi(lines ka distance) to we return not matched and all 
    if new_embedding is None or not candidates_dict:
        return None, 0.0
 
    best_sid = None  #best student id jisse sabse zada match kr rha hai
    best_score = -1.0  #best score for tracking aabhi tk kiske sabse best close aaya hai 

    for sid, stored_embedding in candidates_dict.items():
        if stored_embedding:
            similarity = np.dot(new_embedding, stored_embedding)
            if similarity > best_score:
                best_score = similarity
                best_sid = sid

    if best_score >= threshold:
        return best_sid, best_score

    return None, best_score

def process_bulk_audio():
    pass