import pandas as pd

# csv_files = [
#     "season_data_1.csv",
#     "season_data_2.csv",
#     "season_data_3.csv",
#     "season_data_4_1.csv",
#     "season_data_5.csv",
#     "season_data_6.csv",
#     "season_data_10_12500.csv",
#     "season_data_15_16.csv",
#     "season_data_16_17.csv",
#     "season_data_17_18.csv",
#     "season_data_18_19.csv",
#     "season_data_19_20.csv",
#     "season_data_12500_15.csv",
# ]

csv_files = ["mv_1.csv", "mv_2.csv", "mv_3.csv", "mv_4.csv"]


df_concat = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)

df_concat.to_csv("mv_data_all.csv", index=False)
