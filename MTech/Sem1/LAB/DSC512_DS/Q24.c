/*
Write a C program to implement Queue data structure using linked lists.

Do the following operations:

Insert few elements into the queue. (Minimum 4 elements)
Display the element at the front of the queue (Do not remove it from the Queue).
Remove and display three elements from the Queue.
Display the entire contents of the remaining Queue.
Sample Input/Output
Input

42 77 88 9 3 66 -999

Output

Element at the front of the queue: 42

Remove and display three elements: 42 77 88

Contents of the remaining queue: 9 3 66

*/

#include<stdio.h>
#include<ctype.h>
#include<stdlib.h>
typedef struct llist{
    int data;
    struct llist *next;
    struct llist *prev;
}node;
node *front,*back;
int add_element(int inp){
    node *new_node;
    new_node=(node*)malloc(sizeof(node));
    if(new_node==NULL){
        printf("Overflow");
        return -1;
    }
    
    new_node->data=inp;
    if(front==NULL){
        front=new_node;
        back=new_node;
    }else{
    new_node->prev=back;
    back->next=new_node;
    new_node->next=NULL;
    back=new_node;
    }
    return 0;
}

int delete_element(){
    int r;
    node *tmp;
    if(front==NULL){
        printf("Queue is empty");
        return -1;
    }else{
        r=front->data;
        tmp=front;
        front=front->next;
        free(tmp);
    }
    return r;
}
int peek(){
    return front->data;
}
void display(){
    node *tmp;
    tmp=front;
    if(tmp==NULL){
        printf("Queue is empty");
    }else{
        while(tmp!=NULL){
            printf(" %d",tmp->data);
            tmp=tmp->next;
        }
    }
}
int main(){
    int a=0,tmp=0,cnt=0,i=0;
    while(a!=-999 &&tmp==0){
        scanf("%d",&a);
        if(a==-999){
            break;
        }else{
            tmp=add_element(a);
            if(tmp==0)
            cnt++;
        }
    }
    if(cnt<4)
    printf("Minimum 4 elements must be entered.");
    else{
        tmp=0;
        printf("\nElement at the front of the queue:%d\n",peek());
          printf("\nRemove and display three elements:");
          while(i<3){
          tmp=delete_element();
          printf(" %d",tmp);
          i++;
          }
          printf("\n\nContents of the remaining queue:"); 
          display();
    }
}
