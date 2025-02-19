from time import sleep
from datetime import datetime
import streamlit as st
import pandas as pd
from crud import (
    create_expense,
    read_expenses,
    update_expense,
    delete_expense,
    read_expense_by_id
)

def expense_control():
    logged_user = st.session_state['logged_user']
    with st.sidebar:
        tab_expense_control()
    df_expenses = read_expenses('df')
    st.write(df_expenses)
    
    


def tab_expense_control():
    # Initialize session state variables if they don't exist
    if 'clear_tab_e' not in st.session_state:
        st.session_state['clear_tab_e'] = False
    
    tab_c, tab_r, tab_u, tab_d = st.tabs(['Create', 'Read', 'Update', 'Delete'])
    logged_user = st.session_state['logged_user']
    with tab_c:
        if st.session_state['clear_tab_e']:
            st.session_state['clear_tab_e'] = False
            st.rerun()
        st.write('Create Expense')
        st.session_state['clear_tab_e'] = True
    with tab_r:
        st.write('Read Expense')
    with tab_u:
        st.write('Update Expense')
    with tab_d:
        st.write('Delete Expense')