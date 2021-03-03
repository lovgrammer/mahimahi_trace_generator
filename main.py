import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

data = pd.read_csv("20180618/tcpprobe4.log", header=None, delimiter=r"\s+")
ndata = pd.DataFrame(columns="time acked".split())
ndata['time'] = data[0]
ndata['port'] = data[2]
ndata["acked"] = data[4]
ndata = ndata.iloc[0:-1]

#ndata["acked"] = ndata["acked"].astype(str).str[2:-2]
ndata["port"] = ndata["port"].astype(str).str[-5:]
#print(ndata["port"])

ndata["time"] = ndata["time"].astype(float)
ndata["time"] = ndata["time"] - ndata.iloc[0]["time"]

#ndata['acked'] = ndata.acked.apply(lambda x: int(x[2:-2], 16))
ndata['acked'] = ndata.acked.apply(lambda x: int(x[2:], 16))

ndata = ndata[ndata['port'].astype(str) == "39935"]
#print(ndata["acked"])


# plt.plot(ndata["time"], ndata["acked"])
# plt.show()

cnt = 0
# nndata = pd.DataFrame(columns="time".split())


repeats = []
times = []
itv = []
for idx, row in ndata.iterrows():
    cnt = cnt + 1
    # if cnt == 100:
    #     break
    if idx < len(ndata) -1:
        pkt_cnt = (ndata.iloc[idx+1]["acked"] - row["acked"]) / 1350.0
        tv = ndata.iloc[idx+1]["time"] - row["time"]
        times.append(tv)
        if pkt_cnt <= 0:
              repeats.append(0)
              itv.append(0)
        else:
              repeats.append(pkt_cnt)
              itv.append(tv/pkt_cnt)
        # for i in range(int(pkt_cnt)):
        #     nndata.loc[len(nndata)] = [row["time"]]
        



what = []
ntimes = np.array(what)

for i in range(len(itv)):
        ntimes = np.append(ntimes, np.arange(repeats[i]) * itv[i], axis=0)

    
ndata = ndata[0:len(repeats)]
ndata = ndata.loc[ndata.index.repeat(repeats)].reset_index(drop=True)

print(len(ndata))
print(len(ntimes))
    
ndata.loc[:,"time"] += ntimes
ndata.loc[:,"time"] *= 1000
ndata["time"] = ndata["time"].astype(int)
ndata = ndata["time"]
ndata.to_csv("output.txt", header=None, index=False)

plt.plot(np.arange(len(ndata)), ndata)
plt.show()
