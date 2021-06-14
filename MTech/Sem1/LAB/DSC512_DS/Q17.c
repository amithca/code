/*
Create a doubly linked circular list. 

Delete the 3rd element in the doubly linked circular list. Display the elements of the resulting linked list in reverse order.

Sample Input/Output
Input
    84 19 32 45 25 39 -999    
Output
    39 25 45 19 84


*/

#include<stdio.h>
#include<stdlib.h>
typedef struct llist{
    int data;
    struct llist *next;
    struct llist *prev;
}node;
node *head=NULL;
//node *tail=NULL;
int traverse(int flg);

int create_list(){
    int v_inp,v_out=0;
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
   // tail=ptr;
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
    //v_out=traverse(0);
    return 0;
}}
int traverse(int flg){
    int c=0;
    node *ptr;
    if(head==NULL){
        return -1;
    }else{
        ptr=head->prev;
        while(ptr!=head){
            
                    printf("%d ",ptr->data);
                     ptr=ptr->prev;
                }
                  printf("%d\n",ptr->data);
            }
           
           

    return 0;
}
int del(){
     int c=1;
    node *ptr,*prv;
    if(head==NULL){
        return -1;
    }else{
        ptr=head->next;
        prv=ptr;
        while(ptr!=head){
            c++;
            if(c==3){
                  
                     prv->next=ptr->next;
                     (ptr->next)->prev=prv;
                     free(ptr);
                }
                  
                   prv=ptr;
                   ptr=ptr->next;
            }
           
    }

    return c;
}
int main(){
    int tmp=0;
   create_list();
   tmp=del();
   if(tmp>=3){
   traverse(0);
   } else{
       printf("Underflow !!! Minimum 3 elements must be entered.");
   }
    return 0;
    
}