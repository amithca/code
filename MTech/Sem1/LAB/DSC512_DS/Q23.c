/*
Write a C program to convert Infix expression to Prefix expression using linked list implementation of stacks.

Sample Input/Output I
Input
    A – (B / C + (D % E * F) / G) * H   
Output
    * A – + / B C / % D * E F G H

Sample Input/Output II
Input
    ( A + B * ( C - D ) ) / E   
Output
    / + A * B - C D E

*/

#include<stdio.h>
#include<ctype.h>
#include<stdlib.h>
#include<string.h>
typedef struct llist{
    char data;
    struct llist *next;
    
}node;
node *top;
char *strrev(char *str){
    char *p1,*p2;
    if(!str ||!*str)
        return str;
    for(p1=str,p2=str+strlen(str)-1;p2>p1;++p1,--p2){
        *p1 ^=*p2;
        *p2 ^=*p1;
        *p1 ^=*p2;
    }
    return str;
}
int push(char inp){
    node *new_node;
    new_node=(node*)malloc(sizeof(node));
    if(new_node==NULL){
        printf("Overflow");
        return -1;
    }
    new_node->data=inp;
    new_node->next=top;
    top=new_node;
    return 0;
}
char pop(){
    char r;
    node *tmp;
    if(top==NULL){
        printf("Stack is Empty");
        return '\0';
    }else{
        r=top->data;
        tmp=top;
        top=top->next;
        free(tmp);
    }
    return r;
}
int is_operator(char inp){
    if(inp=='^'||inp=='*'||inp=='/'||inp=='+'||inp=='-'||inp=='%')
    return 1;
    else
    return 0;
}
int get_precedence(char inp){
    if(inp=='^')
    return 3;
    else if(inp=='*'||inp=='/'||inp=='%')
    return 2;
    else if (inp=='+' ||inp=='-')
    return 1;
    else
    return 0;
}
int to_postfix(char* inp,char* result){
    int j=0,i=0,flg=0;
    char tmp2;
    char tmp=')';
    strrev(inp);
    inp=strcat(inp,"(");
    while(tmp!='\0'){
        if(tmp==')'){
            push(tmp);
        }
        else if (isspace(tmp)!=0){
                tmp=inp[i++];
                continue;
        }else if(isalnum(tmp)){
            result[j++]=tmp;
           
           flg=1;
        }
        else if(is_operator(tmp)==1){
            tmp2=pop();
            while(is_operator(tmp2)==1&&get_precedence(tmp2)>get_precedence(tmp)){
                result[j++]=tmp2;
                //result[j++]=' ';
                tmp2=pop();
            }
            push(tmp2);
            push(tmp);
        }
        else if(tmp=='('){
            tmp2=pop();
            while(tmp2!=')'){
                result[j++]=tmp2;
               // result[j++]=' ';
                tmp2=pop();
            }
        }
        else{
            tmp=inp[i++];
            continue;
        }
        tmp=inp[i++];
    }
    result[j++]='\0';
     strrev(result);
    return flg;
    }
int main(){
    char v_inp[100];
    char v_out[100];
    int len,flg=0,cnt=0,i=0,k;
    fgets(v_inp,100,stdin);
    len=strlen(v_inp);
    if(v_inp[len-1]=='\n'&&len==1){
        fgets(v_inp,100,stdin);
    }
    len=strlen(v_inp);
    if(len>0&&v_inp[len-1]=='\n')
        v_inp[--len]='\0';
        else if(len==0)
        printf("No input detected");
        for(k=0;v_inp[k]!='\0';k++){
            cnt++;
        }
        flg=to_postfix(v_inp,v_out);
        if(flg==1){
            i=0;
            while(v_out[i]!='\0')
                printf("%c ",v_out[i++]);
        }
        else if(cnt==0&&flg==0)
        printf("No input detected");
        else
        printf("Invalid input");
}   
    
    
    

