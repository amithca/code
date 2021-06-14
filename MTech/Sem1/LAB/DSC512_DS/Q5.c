/*
Read an array of ‘n’ integers from the user and do the following operations:

Insert an element at a specific position in the array.
Sample Input/Output
Input:
    5
    17 42 16 18 39
     2 98 
    Output         
     17 98 42 16 18 39
*/
#include<stdio.h>
int main(){
    int a[1000];
    int i=0,n=0;
    int v_pos=0;
    int b[1000];
    int v_inp_size=0;
    int v_element=0;
    scanf("%d",&v_inp_size);
    for(i=0;i<v_inp_size;i++){
        scanf("%d",&a[i]);
    }
    scanf("%d%d",&v_pos,&v_element);
    if(v_pos<=0 || v_pos>v_inp_size+1){
        printf("Out of Bound");
    }else{
    for(i=0;i<=v_inp_size;i++){
        if(i==v_pos-1){
        b[n]=v_element;
        n++;
        }
        b[n]=a[i];
        n++;
    }
    for(i=0;i<v_inp_size;i++){
        printf("%d ",b[i]);
    }
    printf("%d",b[i]);
    }
}