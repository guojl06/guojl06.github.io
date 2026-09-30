import random, sys
seed=int(sys.argv[1]); mode=sys.argv[2]
random.seed(seed)
V=10**5
if mode=='max':      n=m=2000; q=60
elif mode=='rowvec': n=2000; m=1; q=20
elif mode=='colvec': n=1; m=2000; q=20
elif mode=='tiny':   n=m=1; q=5
else:                n=random.randint(1,2000); m=random.randint(1,2000); q=random.randint(1,40)
out=[f"{n} {m}"]
for i in range(n):
    out.append(" ".join(str(random.randint(-V,V)) for _ in range(m)))
qs=[]
# 必含 4 个角 + 全矩阵
for (x,y,a,b) in [(1,1,n,m),(n,m,1,1),(1,m,n,1),(n,1,1,m),(1,1,1,1),(n,m,1,1)]:
    qs.append((x,y,a,b))
while len(qs)<q:
    x=random.randint(1,n); y=random.randint(1,m)
    # 边界偏置：一半查询贴右/下边界
    a=random.choice([1,n-x+1,random.randint(1,n-x+1)])
    b=random.choice([1,m-y+1,random.randint(1,m-y+1)])
    qs.append((x,y,a,b))
qs=qs[:q]
out.append(str(len(qs)))
for t in qs: out.append(" ".join(map(str,t)))
sys.stdout.write("\n".join(out)+"\n")
