#include <cstdio>
static long long P[2001][2001];
int main(){int n,m,q;if(scanf("%d%d",&n,&m)!=2)return 1;
 for(int i=1;i<=n;++i)for(int j=1;j<=m;++j){int v;scanf("%d",&v);P[i][j]=P[i-1][j]+P[i][j-1]-P[i-1][j-1]+v;}
 scanf("%d",&q);
 for(int i=0;i<q;++i){int x,y,a,b;scanf("%d %d %d %d",&x,&y,&a,&b);
  long long s=P[x+a-1][y+b-1]-P[x-1][y+b-1]-P[x+a-1][y-1]+P[x-1][y-1];
  printf("%lld\n",s);} return 0;}
