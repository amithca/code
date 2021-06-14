#include<stdio.h>
#include<stdlib.h>
#include<ctype.h>
typedef struct llist{
    int data;
    struct  llist *next;
}node;
node *start=NULL;
int main(){
    node *new_node,*ptr;
    int v_inp_after=0,v_inp_element=0;
    int flg=0;
    int v_inp=0;
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
        node *tmp_node;
        tmp_node=(node*)malloc(sizeof(node));
        if(tmp_node==NULL){
            printf("Overflow");
            return 0;
        }
        ptr=start;
        while(ptr->next!=NULL){
            ptr=ptr->next;
        }
        tmp_node->data=v_inp;
        tmp_node->next=NULL;
        ptr->next=tmp_node;
    }
    scanf("%d%d",&v_inp_after,&v_inp_element);
    if(start==NULL ){
        printf("Underflow");
        return 0;
    }else if(v_inp_after==-999){
         printf("Not Found");
         return 0;
    }else if (v_inp_element==-999){
        return 0;
    }
    else{
        ptr=start;
        while(ptr->next!=NULL){
            if(ptr->data==v_inp_after){
                node *tmp_node;
                tmp_node=(node*)malloc(sizeof(node));
                 if(tmp_node==NULL){
            printf("Overflow");
            return 0;
        }
                tmp_node->data=v_inp_element;
                tmp_node->next=ptr->next;
                ptr->next=tmp_node;
                flg=1;
                break;
                
            }
            ptr=ptr->next;
        }
         if(ptr->data==v_inp_after && flg==0){
                node *tmp_node;
                tmp_node=(node*)malloc(sizeof(node));
                 if(tmp_node==NULL){
            printf("Overflow");
            return 0;
        }
                tmp_node->data=v_inp_element;
                tmp_node->next=ptr->next;
                ptr->next=tmp_node;
                flg=1;
                
            }
    }
    if(start!=NULL){
        if(flg==0){
            printf("Not Found");
        }
        else{
   ptr=start;
   while(ptr->next!=NULL){
       printf("%d ",ptr->data);
       ptr=ptr->next;
   }
    printf("%d",ptr->data);
    }
    }
    return 0;
    
}
