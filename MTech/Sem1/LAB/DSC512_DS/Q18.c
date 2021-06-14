/*
Create a doubly linked circular list. Delete the last element in the doubly linked circular list.

Sample Input/Output
Input
    84 19 32 45 25 39 -999    
Output
    84 19 32 45 25

*/

#include<stdio.h>
#include<stdlib.h>
typedef struct llist{
    int data;
    struct llist *next;
    struct llist *prev;
}node;
node *head=NULL;
int traverse(int flg){
    int c=0;
    node *ptr;
    if(head==NULL){
        return -1;
    }else{
        ptr=head;
        while(ptr->next!=head){
            printf("%d ",ptr->data);
            ptr=ptr->next;
        }
        printf("%d\n",ptr->data);
          return 0;
    }
  
}
int del(){
    node *ptr,*prv;
    if(head!=NULL){
        
    if(head==head->next){
        ptr=head;
        free(ptr);
        head=NULL;
        return 1;
    }else{
    ptr=head->prev;
   head->prev=ptr->prev;
   prv=ptr->prev;
   prv->next=head;
   
   
   free(ptr);
    return 0;
    }
   
  
    
    }
    else{
        return -1;
    }
}
int create_list(){
    int v_inp;
    node *ptr,*new_node;
    scanf("%d",&v_inp);
    if(v_inp==-999){
        return -1;
    }else{
        ptr=(node*)malloc(sizeof(node));
        ptr->data=v_inp;
        ptr->next=ptr;
        ptr->prev=ptr;
        head=ptr;
        while(v_inp!=-999){
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
            new_node->next=head;
            new_node->prev=ptr;
            ptr->next=new_node;
            head->prev=new_node;
            new_node=new_node->next;
            ptr=ptr->next;
        }
        return 0;
    }
}
int main(){
    int tmp=0;
    create_list();
    tmp=del();
    if (head==NULL && tmp>=0){
         printf("Empty Linked list.");
    } else if(tmp>=0){
    traverse(0);
    } else{
        printf("Underflow !!! Empty Linked list.");
    }
}