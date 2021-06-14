/*
Write a C program to read an integer from the user and check whether it is a palindrome or not. The program should output the number and say whether it is a palindrome or not.
After printing it, can you reverse the order of digits in the number the user has just entered. E.g. 1234 should become 4321. Display the result on the screen in an easily understandable format.
Sample Input/Output
    Input:
    121
    Output
    Palindrome
    121

    Input
    1143
    Output
    Not Palindrome
    3411
*/

#include<stdio.h>
int main(){
    int v_inp;
    int temp1=0;
    int v_out=0;
    int temp=0;
    scanf("%d",&v_inp);
    temp1=v_inp;
    while(temp1!=0){
        
        temp=temp1%10;
        v_out=v_out*10+temp;
        temp1=temp1/10;
        
    }
    if(v_inp==v_out){
    printf("Palindrome\n");
    printf("%d",v_out);
    }
    else {
        printf("Not Palindrome\n");
    printf("%d",v_out);
    }
    return 0;
}