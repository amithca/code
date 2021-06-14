/*
Create a doubly linked list. 

Add 3 elements from the beginning of the linked list. Display the elements of the resulting doubly linked list in reverse order.

Sample Input/Output
Input
    84 19 32 45 25 39 -999
    -5 -12 -68
Output
    39 25 45 32 19 84 -5 -12 -68
*/
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
typedef struct llist{
    int data;
    struct llist *next;
    struct llist *prev;
}node;
node *head=NULL,*tail=NULL;
int create(){
    int v_inp;
    node *ptr,*new_node;
    scanf("%d",&v_inp);
    if(v_inp==-999){
        //printf("Underflow")
        return 0;
    }else{
        ptr=(node*)malloc(sizeof(node));
        if(ptr==NULL){
            printf("Overflow");
        }
        ptr->data=v_inp;
        ptr->next=NULL;
        ptr->prev=NULL;
        head=ptr;
        tail=ptr;
        while(v_inp!=-999){
            scanf("%d",&v_inp);
            if(v_inp==-999){
                break;
            }else{
            new_node=(node*)malloc(sizeof(node));
            new_node->data=v_inp;
            new_node->next=NULL;
            new_node->prev=ptr;
            ptr->next=new_node;
            ptr=ptr->next;
            tail=new_node;
            new_node=new_node->next;
            }
        }
    }
    return 0;
}
void traverse(){
    node *ptr;
    ptr=tail;
    if(tail==NULL){
        printf("Underflow");
        return;
    }else{
    while(ptr!=NULL){
        printf("%d ",ptr->data);
        ptr=ptr->prev;
    }
}
}
int insert(int v_inp){
    node *ptr;
 if(v_inp==-999){
     return 0;
 }else{
        ptr=(node*)malloc(sizeof(node));
        if(ptr==NULL){
            printf("Overflow");
        }
        ptr->data=v_inp;
        ptr->prev=NULL;
        if(head!=NULL){
          ptr->next=head;
        head->prev=ptr;
        head=ptr;
        }else{
        ptr->next=NULL;
        head=ptr;
        tail=ptr;
        } 
        }
    return 0;
}
int read_elements(){
    int k=0,a=-1;
    int  n=-1;
    char *p;
    int c[1000];
    char b[1000];
     fgets(b,1000,stdin);
    
   p=strtok(b," ");
   while(p!=NULL){
     sscanf(p,"%d",&n);
       c[k++]=n;
      p=strtok(NULL," ");
      
   }
   if(k<3){
   printf("Error!! Three elements must be inserted.");
   return 1;
   }else{
   for(int j=0;j<k;j++){
       insert(c[j]);
   }
   }
   return 0;
}
int main(){
    int k=0,a=-1;
    int c[10];
    char b[10];
    a=create();
   getchar();
   if(a==0){
a=read_elements();
}
if(a==0){
   traverse();
   }
   return 0;
}