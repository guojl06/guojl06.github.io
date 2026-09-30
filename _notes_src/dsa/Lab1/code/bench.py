#!/usr/bin/env python3
import subprocess, time, statistics, hashlib, os
CASES = [("A", "/tmp/A.in", "瘦高型大面积询问 (a=n=2000, b<=20)"), ("B", "/tmp/B.in", "单点询问 (a=b=1)")]
PROGS = [("solution_1(scanf)", "/tmp/s1"), ("solution_2(scanf)", "/tmp/s2"),
         ("solution_3(cin)", "/tmp/s3"), ("solution_3(scanf)", "/tmp/s3_scanf")]
REPS = 3
rows = []
for cname, path, desc in CASES:
    print(f"\n=== 数据类 {cname}: {desc} | n=m=2000 q=100000 | 文件 {os.path.getsize(path)/1e6:.1f} MB ===", flush=True)
    digests = {}
    for pname, prog in PROGS:
        ts = []
        for r in range(REPS):
            out = f"/tmp/out_{cname}.txt"
            with open(path, 'rb') as fi, open(out, 'wb') as fo:
                t0 = time.perf_counter()
                subprocess.run([prog], stdin=fi, stdout=fo, check=True)
                t1 = time.perf_counter()
            ts.append(t1 - t0)
        digests[pname] = hashlib.md5(open(out, 'rb').read()).hexdigest()
        rows.append((cname, pname, statistics.mean(ts), min(ts), max(ts)))
        print(f"{pname:20s} 平均 {statistics.mean(ts):7.3f}s  最小 {min(ts):7.3f}  最大 {max(ts):7.3f}  极差 {max(ts)-min(ts):.3f}", flush=True)
    ok = len(set(digests.values())) == 1
    print("输出一致性: " + ("四个程序输出完全一致 OK" if ok else "不一致! " + str(digests)), flush=True)
print("\n=== 汇总 (类 程序 平均 最小 最大) ===")
for r in rows:
    print(f"{r[0]}\t{r[1]}\t{r[2]:.3f}\t{r[3]:.3f}\t{r[4]:.3f}")
