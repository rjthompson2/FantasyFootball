import pandas as pd

df = pd.read_csv("sandbox/ppr_fantasy_leaders.csv")
rb_bench = 12*3
wr_bench = 12*4
te_bench = 12*2
qb_bench = 12*1

rb_df = df.loc[df["Pos"] == "RB"].head(rb_bench)
wr_df = df.loc[df["Pos"] == "WR"].head(wr_bench)
te_df = df.loc[df["Pos"] == "TE"].head(te_bench)
qb_df = df.loc[df["Pos"] == "QB"].head(qb_bench)
print(rb_df)
print(wr_df)
print(te_df)
print(qb_df)

print("AVG RB TTL:", sum(rb_df["TTL"])/len(rb_df))
print("AVG RB PPG:", sum(rb_df["AVG"])/len(rb_df))
print("WRST RB TTL:", rb_df.iloc[rb_bench-1]["TTL"])
print("WRST RB PPG:", rb_df.iloc[rb_bench-1]["AVG"])
print()

wr_total = sum(wr_df["TTL"])
print("AVG WR TTL:", sum(wr_df["TTL"])/len(wr_df))
print("AVG WR PPG:", sum(wr_df["AVG"])/len(wr_df))
print("WRST WR TTL:", wr_df.iloc[wr_bench-1]["TTL"])
print("WRST WR PPG:", wr_df.iloc[wr_bench-1]["AVG"])
print()

print("AVG TE TTL:", sum(te_df["TTL"])/len(te_df))
print("AVG TE PPG:", sum(te_df["AVG"])/len(te_df))
print("WRST TE TTL:", te_df.iloc[te_bench-1]["TTL"])
print("WRST TE PPG:", te_df.iloc[te_bench-1]["AVG"])
print()

print("AVG QB TTL:", sum(qb_df["TTL"])/len(qb_df))
print("AVG QB PPG:", sum(qb_df["AVG"])/len(qb_df))
print("WRST QB TTL:", qb_df.iloc[qb_bench-1]["TTL"])
print("WRST QB PPG:", qb_df.iloc[qb_bench-1]["AVG"])
print()