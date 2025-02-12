import os
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime
from pathlib import Path
import pandas as pd

from werkzeug.security import generate_password_hash, check_password_hash

MYPATH = Path(__file__).parent
# Load environment variables from .env
load_dotenv()
URL = os.getenv("URL")
KEY = os.getenv("KEY")
supabase: Client = create_client(URL, KEY)

# ==================== TABLE SITUATION ====================
class Situation:
    __tablename__ = 'situation'
    def __init__(
        self,
        id: int = None,
        situation: str = None
    ):
        self.id = id
        self.situation = situation

def create_situation(situation):
    response = (
        supabase.table('situation')
        .insert([{'situation': situation}])
        .execute()
    )
    return response.count

def read_situations(return_type = 'df'):
    response = (
        supabase.table('situation')
        .select()
        .execute()
    )
    
    if return_type == 'list':
        return response.data
    elif return_type == 'df':
        df = pd.DataFrame(response.data)
        return df.set_index('id')
    elif return_type == 'class':
        df = pd.DataFrame(response.data)
        situations = [Situation(**row) for index, row in df.iterrows()]
        return situations
    else:
        return print('Invalid return_type')

def get_situation(id_sit):
    response = (
        supabase.table('situation')
        .select()
        .eq('id', id_sit)
        .execute()
    )
    return response.data[0]['situation']


# ==================== TABLE USER_CATEGORY ====================
class UserCategory():
    __tablename__ = 'user_category'
    def __init__(
        self,
        id: int = None,
        category: str = None,
        id_sit: int = None,
        created_at: datetime = None,
    ):
        self.id = id
        self.category = category
        self.id_sit = id_sit
        self.created_at = created_at
        self.situation = get_situation(id_sit)

def create_user_category(category):
    response = (
        supabase.table('user_category')
        .insert([{'category': category, 'id_sit': 1}])
        .execute()
    )
    return response.count
    
@st.cache_data
def read_user_categories(return_type = 'df'):
    response = (
        supabase.table('user_category')
        .select()
        .eq('id_sit', 1)
        .execute()
    )
    
    if return_type == 'list':
        return response.data
    elif return_type == 'df':
        df = pd.DataFrame(response.data)
        return df.set_index('id')
    elif return_type == 'class':
        df = pd.DataFrame(response.data)
        user_categories = [UserCategory(**row) for index, row in df.iterrows()]
        return user_categories
    else:
        return print('Invalid return_type')

def update_user_category(
    id,
    **kwargs
):
    response = (
        supabase.table('user_category')
        .update(kwargs)
        .eq('id', id)
        .execute()
    )
    return response.count

def get_category(id_cat):
    response = (
        supabase.table('user_category')
        .select()
        .eq('id', id_cat)
        .execute()
    )
    return response.data[0]['category']


# ==================== TABLE USERS ====================
class Users():
    __tablename__ = 'users'
    def __init__(
        self,
        id: int = None,
        username: str = None,
        name: str = None,
        password: str = None,
        email: str = None,
        id_cat: int = None,
        id_sit: int = None,
        created_at: datetime = None
    ):
        self.id = id
        self.username = username
        self.name = name
        self.password = password
        self.email = email
        self.id_cat = id_cat
        self.category = get_category(id_cat)
        self.id_sit = id_sit
        self.situation = get_situation(id_sit)
        self.created_at = created_at
    
    def __repr__(self):
        return f"Username: {self.username}, Name: {self.name}"
    
    def define_password(self, password):
        self.password = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password, password)

def create_user(
        username,
        password,
        **kwargs
):
    response = (
        supabase.table('users')
        .insert([{**{'username': username, 'password': generate_password_hash(password), 'id_sit': 1}, **kwargs}])
        .execute()
    )
    return response.count

@st.cache_data
def read_users(return_type = 'df'):
    response = (
        supabase.table('users')
        .select()
        .eq('id_sit', 1)
        .execute()
    )
    
    if return_type == 'list':
        return response.data
    elif return_type == 'df':
        df = pd.DataFrame(response.data)
        return df.set_index('id')
    elif return_type == 'class':
        df = pd.DataFrame(response.data)
        users = [Users(**row) for index, row in df.iterrows()]
        return users
    else:
        return print('Invalid return_type')

def read_user_by_id(id):
    response = (
        supabase.table('users')
        .select()
        .eq('id', id)
        .execute()
    )
    return Users(**response.data[0])

def update_user(
        id,
        **kwargs
):
    response = (
        supabase.table('users')
        .update(kwargs)
        .eq('id', id)
        .execute()
    )
    return response.count

def delete_user(id):
    response = (
        supabase.table('users')
        .update({'id_sit': 3})
        .eq('id', id)
        .execute()
    )
    return response.count
