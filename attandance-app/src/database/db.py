from src.database.config import supabase
import bcrypt 

def hash_pass(password):
    return bcrypt.hashpw(password.encode(),bcrypt.gensalt).decode()

def check_pass(psw,hashed):
    return bcrypt.checkpw(psw.encode(),hashed.encode())


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


def get_all_students():
    res=supabase.table("students").select("*").execute()
    return res.data
