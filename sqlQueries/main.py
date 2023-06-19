import streamlit as st
import pandas as pd
import sqlite3
conn = sqlite3.connect('data/data.sqlite')

c = conn.cursor()

def sql_queries(raw_code):
    c.execute(raw_code)
    names = list(map(lambda x: x[0], c.description))
    # to get data
    data = c.fetchall()

    return data,names

st.title('SQLite3 DML Compiler')
col1,col2 = st.columns(2)

with col1:
    with st.form(key='query_form'):
        raw_code = st.text_area('Write Your Query')
        submit = st.form_submit_button('Execute')
    sql_query = """SELECT name FROM sqlite_master  
          WHERE type='table';"""
    c.execute(sql_query)
    data = c.fetchall()
    result_df = pd.DataFrame(data)

    with st.expander('Database'):
        st.dataframe(result_df)
    for i in data:
        query = f'pragma table_info({i[0]});'
        d = c.execute(query)
        names = list(map(lambda x: x[0], c.description))
        result_df = pd.DataFrame(d,columns = names)
        with st.expander(f"Table '{i[0]}' Description"):
            st.dataframe(result_df)

with col2:
    if submit:
        st.info('Query Submitted')
        st.code(raw_code)

        # to get result
        try:
            query_result,name = sql_queries(raw_code)
            with st.expander('Results'):
                st.write(query_result)
            with st.expander('Table'):
                result_df = pd.DataFrame(query_result,columns = name)
                st.dataframe(result_df)

        except:
            st.write('There is error in sqlite syntax')



