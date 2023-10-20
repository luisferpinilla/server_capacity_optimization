import streamlit as st
import pandas as pd
import numpy as np
from optimizator import lp_model_solver

st.header('Server Capacity Optimization')
st.subheader('A simple linear programming model to solve a problem capacity')

if not 'instance_df' in st.session_state:

    with st.form('Instance Parameters'):
        period_of_time = st.slider('period of time', min_value=5, max_value=10, value=10)
        instance_amount = st.slider(
            'Total amount of intances', min_value=1, max_value=5, value=5)

        submitted = st.form_submit_button('Create a data frame')

        if submitted:

            data_dict = dict()
            data_dict['Instance Type'] = list()
            data_dict['Instance Capacity'] = list()
            data_dict['Instance Cost'] = list()
            data_dict['Initial active quantity'] = list()

            for i in range(instance_amount):
                data_dict['Instance Type'].append(f'InstanceType{i}')
                data_dict['Instance Capacity'].append(i*1.23+0.4)
                data_dict['Instance Cost'].append(i*0.8+0.3)
                data_dict['Initial active quantity'].append(0)

            df = pd.DataFrame(data_dict)

            st.session_state['instance_df'] = df

            data2_dict = dict()
            data2_dict['period'] = list()   
            data2_dict['required capacity'] = list()

            for t in range(period_of_time):
                data2_dict['period'].append(t)
                data2_dict['required capacity'].append(np.random.randint(low=1,high=5))

            period_of_time_df = pd.DataFrame(data2_dict)

            period_of_time_df.set_index('period', drop=True, inplace=True)

            st.session_state['demand'] = period_of_time_df

else:

    instance_type_df = st.session_state['instance_df']
    demand_df = st.session_state['demand']

    with st.form('Configure the instance type:'):

        st.markdown('## Parameter configuration')
        st.markdown('1- Complete the instance configuration')

        edited_instance_type_df = st.data_editor(instance_type_df)

        st.markdown('2- Complete the demand information')
        edited_demand_df = st.data_editor(demand_df, column_config={
            'period':st.column_config.NumberColumn(label='period', help='Period', disabled=False)
        })

        st.markdown('3- Press Solve button to find the optimal capacity Schedule')
        submitted = st.form_submit_button('Solve')

        if submitted:

            st.markdown('See the model bellow:')

            result_df = lp_model_solver(instance_conf=edited_instance_type_df, work_demand=edited_demand_df)

            st.markdown('# Results:')
            st.markdown('This is the suggested scheduled capacity:')

            st.write(result_df)  

            st.write(f"The planned total cost is = {round(result_df['Total Cost'].sum(),ndigits=3)}") 