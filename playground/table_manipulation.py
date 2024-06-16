import pandas as pd
import numpy as np

def lensol(df):
    cols = [col for col in df.columns if "_sol" in col and "diverses" not in col]
    # print(cols[0])
    # print(df[cols[0]].iloc[13])
    # print(len(df[cols[0]][0]))
    def f(el):
        if "[" in el:
            print(el)
            return el.count("(") -1
        return el
    
    for col in cols:
        df[col] = df[col].apply(f)
    return df

# df = pd.read_csv("diverses_solutions_solvers_chars_components_small.csv")
# dg = lensol(df)
# dg.to_csv("proba.csv",index=False)

def UB(df):
    df = df.drop("remove_edges_FAS_greedy_sol",axis=1)
    df = df.drop("remove_edges_FAS_greedy_time",axis=1)
    # df = df.drop("italjani_sol",axis=1)
    # df = df.drop("italjani_time",axis=1)
    print(df.columns)
    cols = [col for col in df.columns if "_sol" in col]
    df["UB"] = df[cols].min(axis=1)
    return df

# df = pd.read_csv("proba.csv")
# dg = UB(df)
# print(dg["UB"])
# dg.to_csv("UB_proba.csv", index=False)

# def LB_UB(df):
#     df["gap"] = df["UB"] - df["LB"]
#     df["rel_gap"] = 2 * (df["UB"] - df["LB"]) / (df["UB"] + df["LB"])
#     return df






    
# df = pd.read_csv("UB_proba.csv")
# dg = LB_UB(df)
# print(dg["gap"])
# dg.to_csv("gap_proba.csv",index = False)



def remove_1node_rows(df):
    dg = df[df.n > 1]
    return dg

df = pd.read_csv("solutions2_solvers_chars_components_small.csv")
dg = remove_1node_rows(df)
dg.to_csv("nonodes_solutions2_solvers_chars_components_small.csv", index=False)


# import pandas as pd

def add_interquartile_range(df):
    # Find all columns ending in '_p25' and '_p75'
    p25_columns = [col for col in df.columns if col.endswith('_p25')]
    p75_columns = [col for col in df.columns if col.endswith('_p75')]
    
    for p25_col in p25_columns:
        # Find the corresponding p75 column
        base_name = p25_col[:-4]  # Remove '_p25' to get the base name
        p75_col = base_name + '_p75'
        
        if p75_col in p75_columns:
            # Calculate the IQR
            iqr_col = base_name + '_iqr'
            df[iqr_col] = df[p75_col] - df[p25_col]
    
    return df


# df = pd.read_csv("nonodes_sols_4_3_2_1_components.csv")
# dg = add_interquartile_range(df)
# dg.to_csv("iqr_nonodes_sols_4_3_2_1_components.csv", index=False)


def add_best_solver_and_UB_columns(df):
    # Find all columns ending in '_sol' and '_time'
    sol_columns = [col for col in df.columns if col.endswith('_sol')]
    time_columns = [col for col in df.columns if col.endswith('_time')]
    
    best_solvers = []
    UB_values = []

    for idx, row in df.iterrows():
        # Get the values of _sol and _time columns for the current row
        sol_values = row[sol_columns]
        time_values = row[time_columns]
        
        # Find the minimum _sol value
        min_sol = sol_values.min()
        
        # Find the solvers with the minimum _sol value
        min_sol_solvers = sol_values[sol_values == min_sol].index
        
        if len(min_sol_solvers) > 1:
            # If there's a tie, compare the corresponding _time values
            # min_time_solver = min_sol_solvers[time_values[min_sol_solvers].idxmin()]
            # print(min_sol_solvers)
            # print(time_values)
            idxx = time_values[list(map(lambda x : x[:-4] + "_time", min_sol_solvers))].idxmin()
            idxx = 0
            min_time_solver = min_sol_solvers[idxx]
        else:
            # If there's no tie, select the solver with the minimum _sol value
            min_time_solver = min_sol_solvers[0]
        
        best_solvers.append(min_time_solver[:-4])
        UB_values.append(min_sol)
    
    # Create the new columns in the DataFrame
    df['best_solver'] = best_solvers
    df['UB'] = UB_values




def add_gap_columns(df):
    # Check if 'UB' column exists
    if 'UB' not in df.columns:
        raise ValueError("The DataFrame must contain a 'UB' column.")
    
    # Find all columns ending in '_sol'
    sol_columns = [col for col in df.columns if col.endswith('_sol')]
    
    for sol_col in sol_columns:
        # Calculate the gap
        gap_col = sol_col.replace('_sol', '_gap')
        df[gap_col] = df[sol_col] / df['UB']
    
    return df

# db_name = "diversesfill_diversesfill_smartAEainf_diverses_nonodes_sols_4_3_2_1_components.csv"
# df = pd.read_csv(db_name)
# dg = add_best_solver_and_UB_columns(df)
# dg = add_gap_columns(df)
# dg.to_csv("gap_UB_" + db_name, index=False)




def add_interquartile_range(df):
    # Find all columns ending in '_p25' and '_p75'
    p25_columns = [col for col in df.columns if col.endswith('_p25')]
    p75_columns = [col for col in df.columns if col.endswith('_p75')]
    
    for p25_col in p25_columns:
        # Find the corresponding p75 column
        base_name = p25_col[:-4]  # Remove '_p25' to get the base name
        p75_col = base_name + '_p75'
        
        if p75_col in p75_columns:
            # Calculate the IQR
            iqr_col = base_name + '_iqr'
            df[iqr_col] = df[p75_col] - df[p25_col]
    
    return df

# db_name = "gap_UB_diversesfill_diversesfill_smartAEainf_diverses_nonodes_sols_4_3_2_1_components.csv"
# df = pd.read_csv(db_name)
# dg = add_interquartile_range(df)
# dg.to_csv("iqr_" + db_name, index=False)


# db_name = "iqr_gap_UB_diversesfill_diversesfill_smartAEainf_diverses_nonodes_sols_4_3_2_1_components.csv"
# df = pd.read_csv(db_name)
# df["treewidth"] = np.min([df.treewidth_min_fill_in.values, df.treewidth_min_degree.values],axis = 0)
# print(df["treewidth"])
# df.to_csv("tw_" + db_name, index=False)


db_name = "tw_iqr_gap_UB_diversesfill_diversesfill_smartAEainf_diverses_nonodes_sols_4_3_2_1_components.csv"
df = pd.read_csv(db_name)

df = df[(df["n"] <= 5000)& (df["m"] <= 10000)]

df.to_csv("nothuge_" + db_name, index=False)
