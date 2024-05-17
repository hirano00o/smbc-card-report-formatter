import sys
import pandas as pd
import unicodedata
import os
import re


def _translate(df):
    df["content"] = unicodedata.normalize("NFKC", str(df["content"]))
    if type(df["note"]) != float:
        df["content"] += " (" + unicodedata.normalize("NFKC", str(df["note"])) + ")"
    df["content"] = re.sub(" +", " ", df["content"])

    return df


df = pd.read_csv(sys.argv[1], encoding="cp932", header=0, skipfooter=1, names=["date", "content", "amount", "kubun1", "kubun2", "pay", "note"], index_col=0, engine="python")
df = df.apply(_translate, axis=1)
df.drop(["amount","kubun1", "kubun2", "note"], axis=1, inplace=True)
df = df.filter(regex="(19|20)([0-9]{2}/(?!((0[2469]|11)/31)|02/(29|30))((0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01]))|([02468][048]|[13579][26])/02/29)", axis=0)
print(df)
name = os.path.basename(sys.argv[1])
df.to_csv("mitsui_" + name, header=False, index=True)
