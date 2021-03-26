#!/bin/bash
import pandas as pd
import csv
import re
import os
import sys
import numpy as np
import argparse
import shutil

with open(sys.argv[1],"r") as fi:
    header = []
    for ln in fi:
        if ln.startswith("#"):
            ln = ln.strip()
            header.append(ln)
base=os.path.basename(sys.argv[1])
base=base.split(".final.vcf")
filename = base[0]

head =  '\n'.join([i for i in header[1:]])

df = pd.read_csv(sys.argv[1],delimiter='\t',comment="#")

if len(df.axes[0]) > 400:
    lines =len(df.axes[0])/25
    groups = df.groupby(np.arange(len(df.index))/lines)
    for (x, y) in groups:
        with open("%s%s%s%s.vcf" % (sys.argv[2],filename,str("_"),x),'w') as f:
            f.write(head)
            f.write("\n")
        y.to_csv("%s%s%s%s.vcf" % (sys.argv[2],filename,str("_"),x), sep="\t", mode='a', index=False)
else:
    shutil.copy(sys.argv[1],sys.argv[2])
    dest_loc = sys.argv[2] + filename + ".final.vcf"
    new_vcf_file = sys.argv[2]+ filename + "_0.vcf"
    os.rename(dest_loc, new_vcf_file)

    
