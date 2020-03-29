#!/home/mgreco/miniconda3/envs/dev/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

raw = pd.read_csv("~/speedtest/test.log")
raw.index = pd.to_datetime(raw.Timestamp)

raw.loc[:, "Download"] = raw.Download.div(1e6)
raw.loc[:, "Upload"] = raw.Upload.div(1e6)

resampled = raw.resample("1H")
ping = resampled.Ping.mean()
down = resampled.Download.mean()
up = resampled.Upload.mean()

data = pd.concat([down, up, ping], axis=1)
cols = ["Download", "Upload", "Ping"]
print("="*40)
print("RAW")
print("="*40)
print(raw[cols].tail())
print("="*40)
print("RESAMPLED")
print("="*40)
print(data.tail())

axs = data.plot(subplots=True, figsize=(20,10), marker="o", sharex=True, sharey=False)
_ = plt.suptitle("Speed Test : MasMovil")
_ = plt.ylabel("Mbps")
_ = plt.xlabel("Timestamp")
freq = 2
xticks = data.index.astype(int) / 60 / 60 / 1e9
xticks_lab = data.index.strftime("%T %d-%m")
axs[-1].xaxis.set_major_locator(mpl.ticker.NullLocator())
axs[-1].xaxis.set_minor_locator(mpl.ticker.NullLocator())
plt.xticks(xticks[::freq], xticks_lab[::freq])
plt.tight_layout()
plt.savefig("/home/mgreco/speedtest/test.png")
