import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("data.txt", header=None, delimiter=r"\s+")
ndata = pd.DataFrame(columns="time acked".split())
ndata['time'] = data[0]
ndata["acked"] = data[4]
ndata = ndata.iloc[0:-1]

ndata["time"] = ndata["time"].astype(float)
ndata.loc[:,"time"] *= 1000
ndata["time"] = ndata["time"].astype(int)
ndata['acked'] = ndata.acked.apply(lambda x: int(x[2:-2], 16))

ndata = ndata.iloc[10:-3000]

# plt.plot(ndata["time"], ndata["acked"])
# plt.show()

cnt = 0
# nndata = pd.DataFrame(columns="time".split())


repeats = []
times = []
for idx, row in ndata.iterrows():
    cnt = cnt + 1
    # if cnt == 100:
    #     break
    if idx < len(ndata) -1:
        pkt_cnt = (ndata.iloc[idx+1]["acked"] - row["acked"]) / 1388
        # print(pkt_cnt)
        if pkt_cnt > 0:
            times.append(ndata.iloc[idx+1]["time"] - row["time"])
            repeats.append(pkt_cnt)
        # for i in range(int(pkt_cnt)):
        #     nndata.loc[len(nndata)] = [row["time"]]
        

what = []
ntimes = np.array(what)
itv = np.array(times)/np.array(repeats)
# print(itv)
for i in range(len(itv)):
    if ndata.iloc[i]["time"] == ndata.iloc[i+1]["time"]:
        ntimes = np.append(ntimes, np.arange(repeats[i]) * itv[i], axis=0)
    else:
        ntimes = np.append(ntimes, np.arange(repeats[i]) * 0.0, axis=0)

    
ndata = ndata[0:len(repeats)]
print(ndata.index.repeat(repeats))
ndata = ndata.loc[ndata.index.repeat(repeats)].reset_index(drop=True)


    
ndata.loc[:,"time"] += ntimes
ndata = ndata["time"]
ndata.to_csv("output.txt", header=None, index=False)

plt.plot(np.arange(len(ndata)), ndata)
plt.show()
