#!/home/mgreco/miniconda3/envs/speedtest/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl

raw = pd.read_csv("~/github/mmngreco/speedtest/test.log")
raw.index = pd.to_datetime(raw.Timestamp)
raw.index = raw.index.map(lambda x: x.tz_convert("Europe/Madrid"))

raw.loc[:, "Download"] = raw.Download.div(1e6)
raw.loc[:, "Upload"] = raw.Upload.div(1e6)

resampled = raw.resample("1H")
ping = resampled.Ping.mean()
down = resampled.Download.mean()
up = resampled.Upload.mean()

data = pd.concat([down, up, ping], axis=1)
cols = ["Download", "Upload", "Ping"]


raw.loc[:, "Hour"] = raw.index.hour
long_data = raw.loc[:, cols+["Hour"]].melt("Hour")
long_data.head()
sns.catplot(data=long_data, x="Hour", y="value", col="variable", kind="point", sharey=False, estimator=np.mean)
g = sns.relplot(x="Hour", y="value", col="variable", kind="line", data=long_data, marker="o",
        facet_kws={"sharey": False})
plt.savefig("/home/mgreco/github/mmngreco/speedtest/test.png")

by_hour_mean = raw.groupby(lambda x: x.hour)[cols].mean()
by_hour_min = raw.groupby(lambda x: x.hour)[cols].min()
by_hour_max = raw.groupby(lambda x: x.hour)[cols].max()
by_hour_std = raw.groupby(lambda x: x.hour)[cols].std()


span = 80
print("="*span)
print("RAW")
print("-"*span)
print(raw[cols].tail())
print("="*span)
print("RESAMPLED")
print("-"*span)
print(data.tail())
print("="*span)
print("STATS")
print("-"*span)
print(raw.describe())
print("="*span)


# axs = data.plot(subplots=True, figsize=(15,10), marker="o", sharex=True, sharey=False)
# _ = plt.suptitle("SPEED TEST : MASMOVIL (21378)", y=0.97, fontfamily="sans-serif")
# # _ = plt.ylabel("Mbps")
# _ = plt.xlabel("Timestamp")

# freq = 2
# xticks = data.index.map(lambda x: x.toordinal())
# xticks_lab = data.index.strftime("%T %H")
# axs[-1].xaxis.set_major_locator(mpl.ticker.NullLocator())
# axs[-1].xaxis.set_major_locator(mpl.ticker.NullLocator())
# plt.xticks(xticks[::freq], xticks_lab[::freq], rotation=90)
# plt.tight_layout(rect=[0.0, 0.05, 1, 0.95])
# plt.savefig("/home/mgreco/github/mmngreco/speedtest/test.png")
