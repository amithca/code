/*
Read an array of ‘n’ integers from the user and do the following operations:

Sort the array in ascending order.
Sort the array in descending order.
Sample Input/Output
    Input:
    5
    17 42 16 18 39
    Output
    16 17 18 39 98
    98 39 18 17 16
*/
#include<stdio.h>
int main(){
    int n=0,i=0,j=0,temp=0;
    int a[1000];
    scanf("%d",&n);
    for(i=0;i<n;i++){
        scanf("%d",&a[i]);
    }
     for(i=0;i<n;i++){
         for(j=0;j<n-1;j++){
        if(a[j+1]<a[j]){
            temp=a[j+1];
            a[j+1]=a[j];
            a[j]=temp;
        }
         }
    }
    for(i=0;i<n-1;i++){
        printf("%d ",a[i]);
    }
    printf("%d\n",a[i]);
     for(i=0;i<n;i++){
         for(j=0;j<n-1;j++){
        if(a[j+1]>a[j]){
            temp=a[j+1];
            a[j+1]=a[j];
            a[j]=temp;
        }
         }
    }
    for(i=0;i<n-1;i++){
        printf("%d ",a[i]);
    }
    printf("%d\n",a[i]);
}