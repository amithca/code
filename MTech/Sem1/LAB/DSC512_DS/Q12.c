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
         printf("Underflow");
        return 0;
    }else{
        ptr=(node*)malloc(sizeof(node));
        ptr->data=v_inp;
        ptr->next=NULL;
        ptr->prev=NULL;
        head=ptr;
        tail=ptr;
    }
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
        new_node->next=NULL;
        new_node->prev=ptr;
        ptr->next=new_node;
        tail=new_node;
        new_node=new_node->next;
        ptr=ptr->next;
        
    }
    return 0;
}
void traverse_frm_head(){
    node *ptr;
   
    if(head==NULL){
        return;
    }else{
     ptr=head;
    while(ptr->next!=NULL){
        printf("%d ",ptr->data);
        ptr=ptr->next;
    }
    printf("%d\n",ptr->data);
    }
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
  create_llist();
 traverse_frm_head();
 traverse_frm_tail();
}