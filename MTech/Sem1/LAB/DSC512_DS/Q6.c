/*
Read an array of ‘n’ integers from the user and do the following operations:

Search for a specific element in the array.
Sample Input/Output
Input:
    5
    17 42 16 18 39
    18
Output
    Element Found  at position 4   
*/
#include<stdio.h>
#include<stdbool.h>
int main(){
    int n=0,i=0,j=0,v_element=0;
    bool flg;
    int a[1000],b[1000];
    scanf("%d",&n);
    for(i=0;i<n;i++){
        scanf("%d",&a[i]);
    }
    scanf("%d",&v_element);
    for(i=0;i<n;i++){
        if(a[i]==v_element){
            b[j]=i+1;
            j++;
            flg=true;
        }
    }
    if (flg==true){
        if(j>1){
             printf("Element Found at positions ");
        }else{
             printf("Element Found at position ");
        }
       
        for(i=0;i<j-1;i++){
         printf("%d,",b[i]);
        }
     printf("%d",b[i]);
    }else{
        printf("Element Not Found");
    }
}