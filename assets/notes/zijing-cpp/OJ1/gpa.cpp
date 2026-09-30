#include<iostream>

double get_grade(int score){
    if(score>=90) return 4;
    if(score>=85) return 3.6;
    if(score>=80) return 3.3;
    if(score>=77) return 3.0;
    if(score>=73) return 2.6;
    if(score>=70) return 2.3;
    if(score>=67) return 2.0;
    if(score>=63) return 1.6;
    if(score>=60) return 1.3;
    return 0;
}

int main(){

    int n,score,credit,credits=0;
    double total=0;
    scanf("%d",&n);
    for(int i=1;i<=n;i++){
        scanf("%d %d",&credit,&score);
        credits+=credit;
        total+=credit*get_grade(score);
        
    }
    printf("%.2lf",double(total)/credits);

    return 0;
}