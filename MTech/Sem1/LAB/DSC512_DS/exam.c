#include<stdio.h>
#include<string.h>
void main(){
    char inp[20];
    int i=0,j=0;
    scanf("%s",&inp);
    for(i=0;i<strlen(inp);i++){
        for(j=strlen(inp)/2;j<=i;j++){
            printf("%c ",inp[j]);
        }
    }
}