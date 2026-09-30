#!/usr/bin/env python3
import subprocess, time, statistics, hashlib, os
CASES = [("A", "/tmp/A.in", "大面积询问"), ("B", "/tmp/B.in", "单点询问")]
PROGS = [("solution_1(scanf)", "/tmp/s1"), ("solution_2(scanf)", "/tmp/s2"),
         ("solution_3(scanf)", "/tmp/s3_scanf"), ("solution_3(fread,提交版)", "/tmp/s3_fread"),
         ("solution_3(cin,旧版)", "/tmp/s3")]
REPS = 5
for cname, path, desc in CASES:
    print(f"\n=== 数据类 {cname}: {desc} | {os.path.getsize(path)/1e6:.1f} MB ===", flush=True)
    digests = {}
    for pname, prog in PROGS:
        ts = []
        for r in range(REPS):
            with open(path, 'rb') as fi, open('/tmp/o.txt', 'wb') as fo:
                t0 = time.perf_counter(); subprocess.run([prog], stdin=fi, stdout=fo, check=True); t1 = time.perf_counter()
            ts.append(t1 - t0)
        digests[pname] = hashlib.md5(open('/tmp/o.txt','rb').read()).hexdigest()
        print(f"{pname:26s} 平均 {statistics.mean(ts):7.3f}s  最小 {min(ts):7.3f}  最大 {max(ts):7.3f}  极差 {max(ts)-min(ts):.3f}", flush=True)
    print("输出一致性: " + ("全部一致 OK" if len(set(digests.values()))==1 else "不一致! "+str(digests)), flush=True)
