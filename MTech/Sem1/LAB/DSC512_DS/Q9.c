#include<stdio.h>
#include<stdlib.h>
typedef struct llist{
    int data;
    struct llist *next;
}node;
node *start=NULL;
int main(){
     node *new_node;
     node *ptr;
     int v_inp=0,i=0;
     
    scanf("%d",&v_inp);
    if(v_inp!=-999){
       
        new_node=(node*)malloc(sizeof(node));
        new_node->data=v_inp;
        new_node->next=NULL;
        start=new_node;
    }
   while(v_inp!=-999){
       
           v_inp=0;
            scanf("%d",&v_inp);
            if(v_inp==-999)
               break;
            ptr=start;
            while(ptr->next!=NULL){
                ptr=ptr->next;
            }
            node *tmp_node;
            tmp_node=(node*)malloc(sizeof( node));
            if(tmp_node==NULL){
                printf("Overflow");
                break;
            }
            tmp_node->data=v_inp;
            tmp_node->next=NULL;
            ptr->next=tmp_node;
   }
      
      if(start==NULL){
          printf("Underflow");
      }else{
          ptr=start;
           while(ptr->next!=NULL){
               printf("%d ",ptr->data);
                ptr=ptr->next;
            }
             printf("%d",ptr->data);
          
      } 
       
    }