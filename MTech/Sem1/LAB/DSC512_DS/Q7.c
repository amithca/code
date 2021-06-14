/*
Read an array of ‘n’ integers from the user and do the following operations:

Delete an element from the array.
Sample Input/Output
Input:
    5
    17 42 16 18 39
    3
Output
  17 42 18 39   
*/
#include<stdio.h>
int main(){
    int n=0,v_pos,i=0,j=0;
    int a[1000],b[1000];
    scanf("%d",&n);
    for(int i=0;i<n;i++){
        scanf("%d",&a[i]);
    }
    scanf("%d",&v_pos);
    if (v_pos>n || v_pos<1){
        printf("Out of bound");
    }else{
    for(i=0;i<n;i++){
        if(i!=v_pos-1){
        b[j]=a[i];
        j++;
        }
    }
     for(i=0;i<j-1;i++){
        printf("%d ",b[i]);
    }
      printf("%d",b[i]);
    }
}