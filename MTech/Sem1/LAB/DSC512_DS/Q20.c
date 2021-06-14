/*
Write a C program to implement stack data structure using linked lists.

Do the following operations:

PUSH a few elements into the stack. (Minimum 4 elements)
Do a PEEK operation.
Do three consecutive POP operations and display the elements.
Display the entire contents of the remaining Stack.


*/
#include<stdio.h>
#include<stdlib.h>
typedef struct llist{
    int data;
    
    struct llist *next;
}node;
node *top=NULL;
void push(int inp){
   node *new_node,*ptr;
   new_node=(node*)malloc(sizeof(node));
   new_node->data=inp;
   if(top==NULL){
       new_node->next=NULL;
    }else{
        new_node->next=top;
    }
    top=new_node;
}
int pop(){
    node *ptr;
    ptr=top;
    if(ptr==NULL){
        printf("Stack is empty");
        return -1;
    }else{
    top=top->next;
    printf("%d ",ptr->data);
    free(ptr);
    return 0;
    }
}
int display(){
    node *ptr;
    ptr=top;
    if (ptr==NULL){
        return -1;
    }else{
    while(ptr->next!=NULL){
        printf("%d ",ptr->data);
        ptr=ptr->next;
    }
     printf("%d\n",ptr->data);
     return 0;
    }
}
int peek(){
    if(top==NULL){
        return -1;
    }
    else{
    printf("%d ",top->data);
    return 0;
    }
}
void main(){
    int element_count=0,v_inp=0;
    while(v_inp!=-999){
    scanf("%d",&v_inp);
    if(v_inp==-999){
        break;
    }else{
   push(v_inp);
    element_count++;
    }
    }
    if(element_count==-1){
        printf("Stack is empty");
    }else if (element_count<4){
         printf("Minimum 4 elements must be entered.");
        
    }else{
    
    printf("\nPeek: ");
    peek();
    printf("\nPOP operations: ");
   pop();
    pop();
   pop();
    printf("\nContents of the remaining Stack: ");
    display();
    }
}