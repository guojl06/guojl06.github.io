#include<cstdio>
using namespace std;

long long n,m;
long long ans[2001][2001]={0};

char buf[1<<26],*p=buf;

long long readint(){
    long long x=0;int f=1;
    while(*p<'0'||*p>'9'){if(*p=='-')f=-1;p++;}
    while(*p>='0'&&*p<='9'){x=x*10+*p-'0';p++;}
    return x*f;
}

int main(){
    int len=fread(buf,1,sizeof(buf)-1,stdin);
    buf[len]=0;
    n=readint();m=readint();
    for(long long i=1;i<=n;i++){
        for(long long j=1;j<=m;j++){
            ans[i][j]=readint()+ans[i-1][j]+ans[i][j-1]-ans[i-1][j-1];
        }
    }
    long long q=readint();
    for(long long i=1;i<=q;i++){
        long long x=readint(),y=readint(),a=readint(),b=readint();
        printf("%lld\n",ans[x+a-1][y+b-1]-ans[x-1][y+b-1]-ans[x+a-1][y-1]+ans[x-1][y-1]);
    }
    return 0;
}
