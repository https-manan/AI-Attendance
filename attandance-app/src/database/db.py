from src.database.config import supabase
import bcrypt 

#All teacher tings 
#---------------------
def hash_pass(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_pass(psw, hashed):
    return bcrypt.checkpw(psw.encode(), hashed.encode())


def check_teacher_exists(username):
    res=supabase.table("teachers").select("username").eq("username",username).execute()
    return len(res.data)>0

def create_teacher(username,password,name):
    data={"username":username,"password":hash_pass(password),"name":name}
    res=supabase.table("teachers").insert(data).execute()
    return res.data


def teacher_login(username,password):
    res=supabase.table("teachers").select("*").eq("username",username).execute()
    if res.data:
        teacher=res.data[0]
        if check_pass(password,teacher['password']):
            return teacher
        return None




#All students tings 
#---------------------

def get_all_students():
    res=supabase.table("students").select("*").execute()
    return res.data

def create_subject(subject_code,name,section,teacher_id):
    data={'subject_code':subject_code,"name":name,"section":section,'teacher_id':teacher_id}
    res=supabase.table('subject').insert(data).execute()
    return res.data

def get_teacher_subjects(teacher_id):
    res=supabase.table('subject').select('*,subject_student(count),attandance_logs(timestam)').eq("teacher_id",teacher_id).execute()
    subject=res.data

    for sub in subject():
        sub['total_students']=sub.get("subject_student",[{}])[0].get('count',0)if sub.get('subject_student')else 0      #this [{}] is fall back ki agar nahi mila so we return empty 
        attandance=sub.get('attandance_logs',[])
        unique_session=len(set(log['timestams'] for log in attandances))
        sub['total_classes']=unique_session
        sub.pop('subject_student',None)
        sub.pop('attandance_logs',None)
        
    return subjects

def enroll_student_to_subject(student_id, subject_id):
    data = {'student_id': student_id, "subject_id": subject_id}
    response= supabase.table('subject_students').insert(data).execute()
    return response.data


def unenroll_student_to_subject(student_id, subject_id):
    response= supabase.table('subject_students').delete().eq('student_id', student_id).eq('subject_id', subject_id).execute()
    return response.data


def get_student_subject(student_id):
    response = supabase.table('subject_students').select('*, subjects(*)').eq('student_id', student_id).execute()
    return response.data


def get_student_attendance(student_id):
    response = supabase.table('attendance_logs').select('*, subjects(*)').eq('student_id', student_id).execute()
    return response.data

