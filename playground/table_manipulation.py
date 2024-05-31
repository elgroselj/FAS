import pandas as pd

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

def LB_UB(df):
    df["gap"] = df["UB"] - df["LB"]
    df["rel_gap"] = 2 * (df["UB"] - df["LB"]) / (df["UB"] + df["LB"])
    return df
    
df = pd.read_csv("UB_proba.csv")
dg = LB_UB(df)
print(dg["gap"])
dg.to_csv("gap_proba.csv",index = False)





