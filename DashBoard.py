import os
from time import sleep
import streamlit as st
from crud import read_users
from user_management import user_management
from dotenv import load_dotenv

# load_dotenv()
# ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
# ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')


def login():
    users = read_users('class')
    users = {user.username: user for user in users}
    with st.container(border=True):
        st.markdown('Welcome to Marconi Assis Pedrosa WebApp')
        with st.form(key='login_form'):
            username = st.text_input('Enter your username')
            password = st.text_input('Enter your password', type='password')
            if st.form_submit_button('Login'):
                user = users[username]
                if user.verify_password(password):
                    st.success('Login successful')
                    st.session_state['logged'] = True
                    st.session_state['logged_user'] = user
                    sleep(1)
                    st.rerun()
                else:
                    st.error('Incorrect password')

def main_page():
    st.title('Welcome to Expense Control App')

    logged_user = st.session_state['logged_user']
    if logged_user.category == 'Admin':
        cols = st.columns(2)
        with cols[0]:
            if st.button(
                'User Management',
                use_container_width=True):
                st.session_state['page_user_management'] = True
                st.rerun()
        with cols[1]:
            if st.button(
                'Expenses',
                use_container_width=True
                ):
                st.session_state['page_user_management'] = False
                st.rerun()
        
    if st.session_state['page_user_management']:
        user_management()
    # else:
    #     expense_control()

def main():
    if not 'logged' in st.session_state:
        st.session_state['logged'] = False
    if not 'page_user_management' in st.session_state:
        st.session_state['page_user_management'] = False

    if not st.session_state['logged']:
        login()
    else:
        main_page()


if __name__ == '__main__':
    main()