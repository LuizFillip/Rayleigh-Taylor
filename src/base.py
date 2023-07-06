import pandas as pd


def split_by_freq(
        df, 
        freq_per_split = "5D"
        ):
          
    groups = df.groupby(pd.Grouper(
        freq = freq_per_split)
        )
    split_dfs = []

    for group_key, group_df in groups:
        
        if len(group_df) != 0:
            split_dfs.append(group_df)
        
    return split_dfs


  