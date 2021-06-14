/*
Create a doubly linked list. 

Delete 3 elements from the end of the linked list. Display the elements of the resulting doubly linked list in reverse order.

Sample Input/Output
Input
    84 19 32 45 25 39 -999    
Output
    32 19 84

*/
#include<stdio.h>
#include<stdlib.h>
typedef struct llist{
    int data;
    struct llist *next;
    struct llist *prev;
}node;
node *head=NULL;
node *tail=NULL;
int create_llist(){
    int v_inp;
    node *ptr,*new_node;
    scanf("%d",&v_inp);
    if(v_inp==-999){
        //printf("Error!! Underflow, Minimum 3 elements are required.");
        return 1;
    }else{
        ptr=(node*)malloc(sizeof(node));
        ptr->data=v_inp;
        ptr->next=NULL;
        ptr->prev=NULL;
        head=ptr;
        tail=ptr;
    }while(v_inp!=-999){
        scanf("%d",&v_inp);
        if(v_inp==-999){
            break;
        }
        new_node=(node*)malloc(sizeof(node));
        if(new_node==NULL){
            printf("Overflow");
            return 0;
        }
        new_node->data=v_inp;
        new_node->next=NULL;
        new_node->prev=ptr;
        ptr->next=new_node;
        tail=new_node;
        new_node=new_node->next;
        ptr=ptr->next;
    }
    return 0;
}
int del(){
    node *ptr;
    if(tail==NULL){
         //printf("Error!! Underflow, Minimum 3 elements are required.");
         return  1;
    }else if(tail==head){
        free(tail);
        tail=NULL;
        head=NULL;
        
    }else{
    ptr=tail;
    tail=tail->prev;
    tail->next=NULL;
    free(ptr);
    }
    return 0;
}
void traverse_frm_tail(){
    node *ptr;
    if(tail==NULL){
        return;
    }else{
        ptr=tail;
        while(ptr->prev!=NULL){
            printf("%d ",ptr->data);
            ptr=ptr->prev;
        }
        printf("%d\n",ptr->data);
        }
    }
int main(){
    int i=0,a=0;
    a=create_llist();
   while(i<3){
        if(a==0){
        a=del();
        }else{ break;}
        i++;
    }
    if(a==1){
         printf("Error!! Underflow, Minimum 3 elements are required.");
    }else{
        if(head==tail){
            printf("NULL");
        }else{
    traverse_frm_tail();
        }
    }
}