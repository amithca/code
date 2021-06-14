#include<stdio.h>
#include<stdlib.h>
typedef struct llist{
    int data;
    struct llist *next;
    struct llist *prev;
}node;
node *head=NULL;
node *tail=NULL;
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
        ptr->next=NULL;
        ptr->prev=NULL;
        head=ptr;
        tail=ptr;
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
        v_out=traverse(1);
        return v_out;
    }
}
int traverse(int flg){
    int c=0;
    node *ptr;
    if(head==NULL){
        return -1;
    }else{
        ptr=head;
        while(ptr!=NULL){
            if(flg==0){
                if(ptr->next==NULL){
                    printf("%d\n",ptr->data);
                }else{
                    printf("%d ",ptr->data);
                }
            }
            if(ptr->data==42){
                c++;
            }
            ptr=ptr->next;
        }
    }
    return c;
}

int delete_before_pos(int pos){
    node *ptr,*del,*prv;
    int c=0;
    
    if(head==NULL){
        return -1;
    }else{
        ptr=head;
        while(ptr!=NULL){
            if(ptr->data==42){
                c++;
                if(c==pos){
                    if(ptr==head){
                        return -1;//Underflow
                    }else{
                   del=ptr->prev;
                   if(del==head){
                       head=ptr; 
                       ptr->prev=NULL;
                   }else{
                      prv=del->prev;
                   ptr->prev=prv;
                   prv->next=ptr;
                   }
                   //printf("prv=%d",prv->data);
                  // printf("del=%d",del->data);
                  // printf("ptr=%d",ptr->data);
                   free(del);
                   break;
                   return 0;
                }
            }
        }
        ptr=ptr->next;
    }
    return 0;
}
}
int main(){
    int cnt=0,pos=0,new_element=0,tmp=0;
    cnt=create_list();
    if(cnt>0){
            if(cnt>1){
        printf("%d occurrence of 42 found. Where should the deletion occur?\n",cnt);
        scanf("%d",&pos);
    }else{
        pos=1;
    }
    if(pos<1 || pos>cnt){
        printf("Out of bound");
    }else{
        tmp=delete_before_pos(pos);
    }
    if(tmp==-1){
        printf("No element before 42");
    }else{
    traverse(0);
    }
    }
    else{
         printf("At least one element must be 42.");
        }
    return 0;
}