/*
Write a C program for parenthesis checking using linked list implementation of stack.

Sample Input/Output I
Input
    [56 + 29 {a – b (m + n) * u} + 89]    
Output
    Parenthesis Matched.

Sample Input/Output II
Input
    [ p + q {m + 8 ] * c { -4 / b ) }    
Output
    Parenthesis Mismatched.
*/

#include<stdio.h>
#include<stdlib.h>
#include<string.h>
typedef struct llist{
    char data;
    struct llist *next;
}node;
node *top=NULL;
int push(char inp){
    node *new_node;
    new_node=(node*)malloc(sizeof(node));
    new_node->data=inp;
    if(top==NULL){
        new_node->next=NULL;
    }else{
    new_node->next=top;
    }
    top=new_node;
    return 0;
}
int pop(){
    node *ptr;
    int a=-1;
    ptr=top;
    if(ptr==NULL){
       a=-1;
    }else{
    top=top->next;
    a=ptr->data;
    free(ptr);
   a=0;
    }
     return a;
}
char peek(){
    char tmp='\0';
    if(top!=NULL){
    tmp= top->data;
    }
    return tmp;
}
void main(){
    char v_inp[100], tmp;
    int flg=0,tmp_pop=0;
    fgets(v_inp,100,stdin);
   
   // printf("%s,%d",v_inp,l);
    for(int i=0;i<=strlen(v_inp);i++){
    
        if(v_inp[i]=='{'||v_inp[i]=='('||v_inp[i]=='['){
            flg=1;
            push(v_inp[i]);
          
        }
        else if((v_inp[i]=='}')||(v_inp[i]==')')||(v_inp[i]==']')){
             if(peek()=='\0'){
                 tmp_pop=-1;
                 break;
             }
            if((v_inp[i]=='}'&&'{'==peek())||(v_inp[i]==')'&&'('==peek())||(v_inp[i]==']'&&'['==peek())){
          tmp_pop= pop();
          if(tmp_pop==-1){
              break;
          }
            }else{
                 tmp_pop=-1;
                 break;
            }
        }
      
    }
    if(flg==0){
        printf("No Parenthesis found.");
    }else if(top==NULL && tmp_pop!=-1){
        printf("Parenthesis Matched.");
    }else{
        printf("Parenthesis Mismatched.");
    }
    
}