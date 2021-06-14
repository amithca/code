#include<stdio.h>
#include<stdlib.h>
typedef struct llist{
    int data;
    struct llist *next;
}node;
node *start=NULL;
int main(){
    node *new_node,*ptr,*prv,*del;
    int v_inp=0,v_inp_del_before=0;
    int flg=0;
    scanf("%d",&v_inp);
    if(v_inp!=-999){
        new_node=(node*)malloc(sizeof(node));
        if(new_node==NULL){
            printf("Overflow");
            return 0;
        }
        new_node->data=v_inp;
        new_node->next=NULL;
        start=new_node;
    }
    ptr=start;
    while(v_inp!=-999){
        scanf("%d",&v_inp);
        if(v_inp==-999){
            break;
        }
        node *tmp_node;
        tmp_node=(node*)malloc(sizeof(node));
        if(tmp_node==NULL){
            printf("Overflow");
        }
        tmp_node->data=v_inp;
        tmp_node->next=NULL;
        ptr->next=tmp_node;
        ptr=ptr->next;
    }
    scanf("%d",&v_inp_del_before);
    if(v_inp_del_before==-999){
        printf("Not Found");
    }
    ptr=start;
    prv=ptr;
    if(start==NULL){
        printf("Underflow");
        return 0;
    }else if (ptr->next==NULL){
        printf("Underflow");
        return 0;
    }
    while(prv->next!=NULL){
        if(ptr->data==v_inp_del_before && ptr!=start){
          del=prv; //Identify the last element to be deleted
          flg++;
        }
        prv=ptr;
        ptr=ptr->next;
    }
    if (start->data==v_inp_del_before&& flg==0){
        printf("Out of bound");
         return 0;
    }
    if(flg==0){
        printf("Not Found");
         return 0;
    }
        
    else{
    ptr=start;
    prv=ptr;
    while(ptr->next!=NULL){
        if(ptr==del ){
            prv->next=ptr->next;
            free(ptr);
        }else{
       printf("%d ",ptr->data);
        }
        ptr=ptr->next;
    }
    }
    printf("%d",ptr->data);
}#include<stdio.h>
#include<stdlib.h>
typedef struct llist{
    int data;
    struct llist *next;
}node;
node *start=NULL;
int main(){
    node *new_node,*ptr,*prv,*del;
    int v_inp=0,v_inp_del_before=0;
    int flg=0;
    scanf("%d",&v_inp);
    if(v_inp!=-999){
        new_node=(node*)malloc(sizeof(node));
        if(new_node==NULL){
            printf("Overflow");
            return 0;
        }
        new_node->data=v_inp;
        new_node->next=NULL;
        start=new_node;
    }
    ptr=start;
    while(v_inp!=-999){
        scanf("%d",&v_inp);
        if(v_inp==-999){
            break;
        }
        node *tmp_node;
        tmp_node=(node*)malloc(sizeof(node));
        if(tmp_node==NULL){
            printf("Overflow");
        }
        tmp_node->data=v_inp;
        tmp_node->next=NULL;
        ptr->next=tmp_node;
        ptr=ptr->next;
    }
    scanf("%d",&v_inp_del_before);
    if(v_inp_del_before==-999){
        printf("Not Found");
    }
    ptr=start;
    prv=ptr;
    if(start==NULL){
        printf("Underflow");
        return 0;
    }else if (ptr->next==NULL){
        printf("Underflow");
        return 0;
    }
    while(prv->next!=NULL){
        if(ptr->data==v_inp_del_before && ptr!=start){
          del=prv; //Identify the last element to be deleted
          flg++;
        }
        prv=ptr;
        ptr=ptr->next;
    }
    if (start->data==v_inp_del_before&& flg==0){
        printf("Out of bound");
         return 0;
    }
    if(flg==0){
        printf("Not Found");
         return 0;
    }
        
    else{
    ptr=start;
    prv=ptr;
    while(ptr->next!=NULL){
        if(ptr==del ){
            prv->next=ptr->next;
            free(ptr);
        }else{
       printf("%d ",ptr->data);
        }
        ptr=ptr->next;
    }
    }
    printf("%d",ptr->data);
}