from time import sleep
import streamlit as st
import pandas as pd
from crud import (
    create_user,
    read_users,
    update_user,
    delete_user,
    read_user_by_id,
    read_user_categories
)

def user_management():
    with st.sidebar:
        tab_user_management()



def tab_user_management():
    # Initialize session state variables if they don't exist
    if st.button('Clear_Cash'):
        st.cash_data.clear()
    if 'clear_tab_c' not in st.session_state:
        st.session_state['clear_tab_c'] = False
    
    tab_c, tab_r, tab_u, tab_d = st.tabs(['Create', 'Read', 'Update', 'Delete'])
    users = read_users('class')
    categories = read_user_categories('class')
    logged_user = st.session_state['logged_user']
    with tab_c:
        if st.session_state['clear_tab_c']:
            st.session_state['name_create'] = ''
            st.session_state['username_create'] = ''
            st.session_state['email_create'] = ''
            st.session_state['category_create'] = 'User'
            st.session_state['password_create'] = ''
            st.session_state['confirm_password_create'] = ''
            st.session_state['clear_tab_c'] = False
            st.rerun()
        name = st.text_input('Name', value='', key='name_create')
        username = st.text_input('Username', value='', key='username_create')
        email = st.text_input('Email', value='', key='email_create')
        category_dict = {category.category: category.id for category in categories}
        category_default_index = list(category_dict.keys()).index('User')
        category = st.selectbox('Category', category_dict.keys(), index=category_default_index, key='category_create')

        with st.container(border=True):
            password = st.text_input('Password', type='password', value='', key='password_create')
            confirm_password = st.text_input('Confirm Password', type='password', value='', key='confirm_password_create')

        cols = st.columns(2)
        with cols[0]:
            btn_clear = st.button('Clear', key='clear_create', use_container_width=True)
        with cols[1]:
            btn_create = st.button('Create', use_container_width=True)
        if btn_clear:
            st.session_state['clear_tab_c'] = True
            st.rerun()
        if btn_create:
            if name == '' or username == '' or email == '' or password == '' or confirm_password == '':
                st.error('All fields are required')
                # return
            elif username in [user.username for user in users]:
                st.error('Username already exists')
                # return
            elif password != confirm_password:
                st.error('Passwords do not match')
                # return
            else:
                create_user(
                    name=name,
                    username=username,
                    password=password,
                    email=email,
                    id_cat=category_dict[category]
                )
                st.session_state['clear_tab_c'] = True
                st.success('User created successfully!')
                sleep(1)
                st.rerun()
        
    with tab_r:
        data_users = [{
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'email': user.email,
            'category': user.category,
        } for user in users]
        st.dataframe(pd.DataFrame(data_users).set_index('id'), height=200)
    
    with tab_u:
        def clean_password():
            st.session_state.password_update = None
            st.session_state.confirm_password_update = None
        
        user_dict = {user.username: user.id for user in users}
        username = st.selectbox('Select user', user_dict.keys(), key='user_update', on_change=clean_password)
        user = read_user_by_id(user_dict[username])
        name = st.text_input('Name', user.name, key='name_update')
        email = st.text_input('Email', user.email, key='email_update')
        category_dict = {category.category: category.id for category in categories}
        category_default_index = list(category_dict.keys()).index(user.category)
        category = st.selectbox('Category', category_dict.keys(), index=category_default_index, key='category_update')
        with st.container(border=True):
            password = st.text_input('Password', type='password', value=None, key='password_update')
            confirm_password = st.text_input('Confirm Password', type='password', value=None, key='confirm_password_update')
            
        if st.button('Update'):
            if password is None or password == '':
                update_user(
                    id=user.id,
                    name=name,
                    email=email,
                    id_cat=category_dict[category]
                )
                st.success('User updated successfully!')
                sleep(1)
                st.rerun()
            else:
                if password == confirm_password:
                    update_user(
                        id=user.id,
                        name=name,
                        password=password,
                        email=email,
                        id_cat=category_dict[category]
                    )
                    st.success('User updated successfully!')
                    sleep(1)
                    st.rerun()
                else:
                    st.error('Passwords do not match')
                    # return

    with tab_d:
        user_dict = {user.username: user.id for user in users}
        username = st.selectbox('Select user', user_dict.keys(), key='user_delete')
        user = read_user_by_id(user_dict[username])
        if st.button('Delete'):
            st.session_state.confirm_delete = True
            st.session_state.user_to_delete = user_dict[username]
        
        if st.session_state.get('confirm_delete', False):
            st.warning(f'Are you sure you want to delete {user}?')
            cols = st.columns(2)
            with cols[0]:
                if st.button('Confirm Delete', use_container_width=True):
                    delete_user(st.session_state.user_to_delete)
                    st.session_state.confirm_delete = False
                    st.session_state.user_to_delete = None
                    st.rerun()
            with cols[1]:
                if st.button('Cancel', use_container_width=True):
                    st.session_state.confirm_delete = False
                    st.session_state.user_to_delete = None
                    st.rerun()

# if __name__ == '__main__':