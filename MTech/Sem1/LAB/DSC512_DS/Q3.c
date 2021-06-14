/*
Write a C program to read a string from the user and check whether the string is a pangram or not.

A pangram is a sentence containing every letter in the English alphabet. If the sentence is not a pangram print the alphabets that are missing that will make the sentence a pangram.

For example, the sentence, “The quick brown fox jumps over the lazy dog” is a pangram as it contains all the characters from ‘a’ to ‘z’. The sentence “The quick brown fox jumps over the dog” is not a pangram because the characters ‘a’, ‘l’, ‘z’ and ‘y’ are missing.

Sample Input/Output
    Input:
    The five boxing wizards jump quickly
    Output
    Pangram
    Input:
    bcdefghijklmnopqrstuvwxz.
    Output
    Not Pangram
    a y
*/
#include <stdio.h>
#include <ctype.h>
#include <string.h>
int main(){
    
    char v_inp[1000];
    int i=0;
    int j=0;
    int x=0;
    int vp=0;
    char v_temp[27]="abcdefghijklmnopqrstuvwxyz";
    char tmp=' ';
    char emptystr='\0';
    char v_out[1000]="";
   
    int n=0;
   
   
    fgets(v_inp,1000,stdin);
    
    for(x=0;x<strlen(v_inp);x++){
       v_inp[x]=tolower(v_inp[x]);
    }
   
    
    
    for( i=0;i<strlen(v_temp);i++){
       tmp=emptystr;
        tmp=v_temp[i];
       
         
         vp=0;
         for(j=0;j<strlen(v_inp);j++){
             if((v_inp[j]==tmp)&&(v_inp[j]!=' ')){
                 vp=1;
                
             }
         }
         if(vp==0){
             v_out[n]=tmp;
             n++;
         }
    }
     
    if(strlen(v_out)==0){
        printf("Pangram");
        
    } else{
        printf("Not Pangram\n");
    
    
    for(i=0;i<strlen(v_out)-1;i++){
        printf("%c ",v_out[i]);
    }
     printf("%c",v_out[i]);
    }
    return 0;
}