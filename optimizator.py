import pandas as pd
import pulp as pu
import numpy as np

def lp_model_solver(instance_conf:pd.DataFrame, work_demand:pd.DataFrame)->pd.DataFrame:

    # sets:

    periods = list(work_demand.index)

    instances = list(instance_conf['Instance Type'])

    # parameters:
    D = {i:work_demand.loc[i]['required capacity']  for i in periods}
    W = {instance_conf.loc[i]['Instance Type']:instance_conf.loc[i]['Instance Capacity']  for i in instance_conf.index}
    C = {instance_conf.loc[i]['Instance Type']:instance_conf.loc[i]['Instance Cost']  for i in instance_conf.index}
    S = {instance_conf.loc[i]['Instance Type']:instance_conf.loc[i]['Initial active quantity']  for i in instance_conf.index}

    # Variables:
    X = dict()
    I = dict()
    for instance in instances:
        X[instance] =  dict()
        I[instance] =  dict()
        for period in periods:
            x_var_name = f'X_{instance}_{period}'
            X[instance][period] = pu.LpVariable(name=x_var_name, lowBound=0, cat=pu.LpInteger)

            i_var_name = f'I_{instance}_{period}'
            I[instance][period] = pu.LpVariable(name=i_var_name, cat=pu.LpInteger)

    # problem solver
    model = pu.LpProblem(name='Capacity server optimization', sense=pu.const.LpMinimize)

    # Target function

    fobj = [C[instance]*X[instance][period] for instance in instances for period in periods]
    model += pu.lpSum(fobj)
    # Constraints

    # Active instances inventory balance
    for instance in instances:
        for period in periods:
            # if inicial period then use S (initial amount)
            if period == 0:
                model += (X[instance][period]==S[instance] + I[instance][period], f'inventory balance {instance} in {period}')
            else:
                model += (X[instance][period]==X[instance][period-1] + I[instance][period],f'inventory balance {instance} in {period}')

    # Demand
    for period in periods:
        left_expresion = list()
        for instance in instances:
            left_expresion.append(W[instance]*X[instance][period])

        const = (pu.lpSum(left_expresion)>=D[period], f'Demand match with {instance} at period {period}' )        

        model += const


    # solve model
    model.solve()

    # model.writeLP(filename='model.lp')

    # Build report
    df_dict = dict()

    df_dict['Period'] = list()
    df_dict['Instance Type'] = list()
    df_dict['Instances'] = list()

    for period in periods:
        for instance in instances:
            df_dict['Period'].append(period)
            df_dict['Instance Type'].append(instance)
            df_dict['Instances'].append(X[instance][period].varValue)

    df = pd.DataFrame(df_dict)    
    

    df = df.pivot_table(values='Instances',
                        index=['Instance Type'],
                        columns='Period',
                        aggfunc=np.sum)
    
    df['Total Instance Type'] = df.apply(np.sum,axis=1)

    df.reset_index(inplace=True)

    df['Instance Capacity'] = df['Instance Type'].map(W)

    df['Total Required Capacity'] = df['Total Instance Type']*df['Instance Capacity']

    df['Instance Cost'] = df['Instance Type'].map(C).astype(float)

    df['Total Cost'] = df['Total Instance Type']*df['Instance Cost']
   
    df.set_index('Instance Type', inplace=True, drop=True)
    return df


