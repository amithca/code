/*
Create a doubly linked list. Make sure one of the entered elements is 24.

Insert a new element after the existing linked list element 24. If there are more than one occurrence of 24, give user the choice where the new element must be inserted.

Sample Input/Output
Input
    24 19 32 45 24 39 -999
     -56
Output
    2 occurrence of 24 found. Where should the insertion occur?
Input
    1
Output
    24 -56 19 32 45 24 39
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
        }new_node->data=v_inp;
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
                }
                else{
            printf("%d ",ptr->data);
            
            }}
            if(ptr->data==24){
                c++;
            }
            ptr=ptr->next;
        }
       // if(flg==0){
        //printf("%d\n",ptr->data);
        //}
    }
    return c;
}
int insert_at_pos(int inp,int pos){
    node *ptr,*new_node,*nxt;
    int c=0;
    if(head==NULL){
        return -1;
    }
    else{
        ptr=head;
        while(ptr!=NULL){
            if(ptr->data==24){
                c++;
                if(c==pos){
                    
                     new_node=(node*)malloc(sizeof(node));
        new_node->data=inp;
        new_node->prev=ptr;
        if(ptr==tail){
            tail=new_node;
            new_node->next=NULL;
        }else{
        new_node->next=ptr->next;
        nxt=ptr->next;
        
        nxt->prev=new_node;
        }
        ptr->next=new_node;
                }
            }
          
            ptr=ptr->next;
        }
    }
    return 0;
    
}
int main(){
    int cnt=0,pos=0,new_element=0,tmp=0;
    cnt=create_list();
   if(cnt>0){
if ( scanf("%d",&new_element)){
        if(cnt>1){
        printf("%d occurrence of 24 found. Where should the insertion occur?",cnt);
        scanf("%d",&pos);
}
else{pos=cnt;}
        if(pos<1){
            printf("Out of bound");
        }else{
        insert_at_pos(new_element,pos);
        }
    
    }else{        printf("At least one element must be 24.");
    }
    traverse(0);
}  else{        printf("At least one element must be 24.");
    }

return 0;
}