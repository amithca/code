/*
Write a C program to generate prime numbers which has two equidistant prime numbers from it within a given range.

For example, 5 is one such number because we have two prime numbers 3 and 7 both of which are equidistant from 5. The distance in this case would be 2.

Can you generate all such numbers within a given range along with their corresponding two prime numbers and distance?

Sample Input/Output
    Input:
    2 10
    Output
    3 5 7 2

    Input
    10 30
    Output
    11 17 23 6                                                                                                                                                     
    17 23 29 6
*/
#include<stdio.h>
int fun_chk(int a[],int m,int x,int b){
    int i=0;
    for(i=x;i<m;i++){
        if(a[i]==b){
            return 1;
        }
    }
    return 0;
}
int main()
{
    int arr_prime[1000];
    int tmp1=0,tmp2=0,temp=0;
    int v_flg=0;
    int i=0,n=0,j=0;
    int v_inp_min=0;
    int v_inp_max=0;
    scanf("%d %d",&v_inp_min,&v_inp_max);
    if (v_inp_max<v_inp_min){
        temp=v_inp_min;
        v_inp_min=v_inp_max;
        v_inp_max=temp;
    }
    if (v_inp_min<=0){v_inp_min=0;}
    for(i=v_inp_min;i<=v_inp_max;i++){
        v_flg=0;
        for(j=2;j<=i/2;j++){
            if (i%j==0){
                v_flg=1;
            }
            
        }
        if (v_flg!=1){
            if(i!=1){
            arr_prime[n]=i;
            n++;
            }
        }
    }
    for(j=2;j<arr_prime[n-1]-arr_prime[0];j++){
        for(i=0;i<n;i++){
          tmp1=fun_chk(arr_prime,n,i,arr_prime[i]+j);
          if(tmp1==1){
            tmp2=fun_chk(arr_prime,n,i,arr_prime[i]+j+j);
            if(tmp2==1){
                  printf("%d %d %d %d\n",arr_prime[i],arr_prime[i]+j,arr_prime[i]+j+j,j);
                
            }
              
          }
            
        }
        
    }
    return 0;
}