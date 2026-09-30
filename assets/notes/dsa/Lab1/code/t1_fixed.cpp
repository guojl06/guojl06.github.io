#include<cstdio>
using namespace std;

long long n,m;
long long ans[2001][2001]={0};

// fread 快读
namespace IO {
    char buf[1<<25], *p1;
    inline long long readInt(){
        long long x=0; char c=*p1++;
        while(c!='-' && (c<'0'||c>'9')) c=*p1++;
        long long sgn=1;
        if(c=='-'){ sgn=-1; c=*p1++; }
        while(c>='0'&&c<='9'){ x=x*10+c-'0'; c=*p1++; }
        return x*sgn;
    }
}

int main(){
    // 一次性读入整个 stdin
    size_t len=fread(IO::buf,1,sizeof(IO::buf)-4,stdin);
    IO::buf[len]='\0';
    IO::p1=IO::buf;

    n=IO::readInt(); m=IO::readInt();
    for(long long i=1;i<=n;i++){
        for(long long j=1;j<=m;j++){
            long long t=IO::readInt();
            ans[i][j]=t+ans[i-1][j]+ans[i][j-1]-ans[i-1][j-1];
        }
    }

    long long q=IO::readInt();
    for(long long i=1;i<=q;i++){
        long long x=IO::readInt(), y=IO::readInt(), a=IO::readInt(), b=IO::readInt();
        // (x,y) 是起点，(a,b) 是大小：行 x..x+a-1，列 y..y+b-1
        printf("%lld\n", ans[x+a-1][y+b-1]-ans[x-1][y+b-1]-ans[x+a-1][y-1]+ans[x-1][y-1]);
    }
    return 0;
}
