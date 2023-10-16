import streamlit as st
import pandas as pd

@st.cache_data
def get_data_frame(instance_amount:int)->pd.DataFrame:
        
    data_dict = dict()
    data_dict['Instance Type'] = list()
    data_dict['Instance Capacity'] = list()
    data_dict['Instrance Cost'] = list()

    for i in range(instance_amount):
        data_dict['Instance Type'].append(f'Instance Type {i}')
        data_dict['Instance Capacity'].append(i*0.23)
        data_dict['Instrance Cost'].append(i*1.12)

    df = pd.DataFrame(data_dict)

    st.session_state['instance_df'] = df


st.header('Server Capacity Optimization')
st.subheader('A simple linear programing model to solve a problem capacity')

if not 'instance_df' in st.session_state:

    with st.form('Instance Parameters'):
        period_of_time = st.selectbox('period of time',
                                    options=['minutes', 'hours', 'days'])
        instance_amount = st.slider(
            'Total amount of intances', min_value=1, max_value=5)

        submitted = st.form_submit_button('Create a data frame')

        if submitted:

            data_dict = dict()
            data_dict['Instance Type'] = list()
            data_dict['Instance Capacity'] = list()
            data_dict['Instrance Cost'] = list()
            data_dict['Inicial active quantity'] = list()

            for i in range(instance_amount):
                data_dict['Instance Type'].append(f'Instance Type {i}')
                data_dict['Instance Capacity'].append(i*0.23)
                data_dict['Instrance Cost'].append(i*1.12)
                data_dict['Inicial active quantity'].append(0)

            df = pd.DataFrame(data_dict)

            st.session_state['instance_df'] = df

else:
    df = st.session_state['instance_df']    
    with st.form('Configure the instance type:'):
        
        st.data_editor(df)

        submitted = st.form_submit_button('Continue')
        
        if submitted:
            st.write('continuar')
