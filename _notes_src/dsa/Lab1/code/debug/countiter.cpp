#include <cstdio>
int main(){int n,m,q;scanf("%d%d",&n,&m);
 for(int i=0;i<n*m;++i){int v;scanf("%d",&v);}
 scanf("%d",&q); long long it=0;
 for(int i=0;i<q;++i){int x,y,a,b;scanf("%d %d %d %d",&x,&y,&a,&b); it+=(long long)a*b;}
 printf("q=%d 内层迭代总数=%lld\n",q,it); return 0;}
