import streamlit as st
import pandas as pd

st.header('Server Capacity Optimization')
st.subheader('A simple linear programing model to solve a problem capacity')

if not 'instance_df' in st.session_state:

    with st.form('Instance Parameters'):
        period_of_time = st.slider('period of time', min_value=5, max_value=10)
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

            data2_dict = dict()
            data2_dict['period'] = list()   
            data2_dict['required capacity'] = list()

            for t in range(period_of_time):
                data2_dict['period'].append(t)
                data2_dict['required capacity'].append(5)

            period_of_time_df = pd.DataFrame(data2_dict)

            period_of_time_df.set_index('period', drop=True, inplace=True)

            st.session_state['demand'] = period_of_time_df


else:

    instance_type_df = st.session_state['instance_df']
    demand_df = st.session_state['demand']

    with st.form('Configure the instance type:'):

        st.markdown('## Parameter configuration')
        st.markdown('Complete the instance configuration and the demand information')

        edited_instance_type_df = st.data_editor(instance_type_df)
        edited_demand_df = st.data_editor(demand_df, column_config={
            'period':st.column_config.NumberColumn(label='Period', help='Period', disabled=False)
        })

        submitted = st.form_submit_button('Solve')

        if submitted:

            st.write('solving')