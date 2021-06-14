#include<stdio.h>
#include<stdlib.h>
#include<ctype.h>
#include<string.h>
typedef struct llist{
    char nam[100];
    int mark;
    struct llist *next;
    struct llist *prev;
    struct llist *lex_next;
    struct llist *marks_next;
}node;
node *head=NULL;
node *tail=NULL;
node *headByName=NULL;
node *headByMarks=NULL;
int is_valid_name(char *a){
    int len=0;
    int flg=0;
    len=strlen(a);
    for(int i=0;i<len;i++){
        if(isalpha(a[i])<=0){
            flg=-1;
            break;
        }
       // printf("%c",a[i]);
    }
    return flg;
}
int create_llist(){
    char v_inp_nam[100];
    int v_inp_mark;
    int c=0;
    node *ptr,*new_node,*markptr,*nameptr, *tmpPrevMark;
    scanf("%s",v_inp_nam);
     
    if(strcmp(v_inp_nam,"-999")==0){
        printf("Underflow");
        return 0;
    }
    scanf("%d",&v_inp_mark);
    if (v_inp_mark<0){
         printf("Marks cannot be negative");
        return 0;
    }
    else{
        ptr=(node*)malloc(sizeof(node));
        strcpy(ptr->nam,v_inp_nam);
        ptr->mark=v_inp_mark;
        ptr->next=NULL;
        ptr->prev=NULL;
        ptr->marks_next=NULL;
        ptr->lex_next=NULL;
        head=ptr;
        tail=ptr;
        headByName=ptr;
        headByMarks=ptr;
    }
    //printf("check=%d",!strcmp(v_inp_nam,"-999"));
    while(strcmp(v_inp_nam,"-999")!=0){
        scanf("%s",v_inp_nam);
        
        if(strcmp(v_inp_nam,"-999")==0 ){
            break;
        }
         if(is_valid_name(v_inp_nam)==-1 ){
            return -1;
            break;
        }
        scanf("%d",&v_inp_mark);
         c++;
         
        if(v_inp_mark<0){
            break;
            
        }
        new_node=(node*)malloc(sizeof(node));
        if(new_node==NULL){
            printf("Overflow");
            return 0;
        }
        markptr=headByMarks;
        
    tmpPrevMark=headByMarks;
    nameptr=headByName;
      /*  while((strcmp(toupper((char)nameptr->nam),toupper(v_inp_mark))<0)&&nameptr->lex_next!=NULL){
            nameptr=nameptr->lex_next;
        }*/
        strcpy(new_node->nam,v_inp_nam);
        new_node->mark=v_inp_mark;
        new_node->next=NULL;
        new_node->prev=ptr;
        //new_node->lex_next=nameptr->lex_next;
        while(markptr->mark>=v_inp_mark &&markptr!=NULL){
            tmpPrevMark=markptr;
            markptr=markptr->marks_next;
        
        }
        new_node->marks_next=markptr;
        tmpPrevMark->marks_next=new_node;
        
        ptr->next=new_node;
       //nameptr->lex_next=new_node;
        markptr->marks_next=new_node;
        tail=new_node;
        new_node=new_node->next;
        ptr=ptr->next;
       
    }
    
    return c;
}
void sort(){
    node *ptr1, *ptr2,*tmp;
    ptr1=head;
    while(ptr1->next!=NULL){
        ptr2=ptr1;
        prv=ptr2;
        while(ptr2->next!=NULL){
            if(ptr2->data<ptr2->next>data){
                tmp=ptr;
                prv->next=ptr->next;
                tmp->next=ptr->next->next;
                ptr=ptr->next;
                ptr->next=tmp;
            }
            prv=ptr;
            ptr=ptr->next;
            
        }
    }
}

void traverse(){
    node *ptr;
    if(head==NULL){
        return ;
    }else{
        ptr=head;
        while(ptr->next!=NULL){
            printf("%s %d,",ptr->nam,ptr->mark);
            ptr=ptr->next;
        }
         printf("%s %d\n",ptr->nam,ptr->mark);
    }
}
void traverseByMark(){
    node *ptr;
    if(headByMarks==NULL){
        return ;
    }else{
        ptr=headByMarks;
        while(ptr->marks_next!=NULL){
            printf("%s %d,",ptr->nam,ptr->mark);
            ptr=ptr->marks_next;
        }
         printf("%s %d\n",ptr->nam,ptr->mark);
    }
}
int main(){
    int a;
    a=create_llist();
    if( a==-1){
    printf("Name must contain only alphabets.");
    }else{
    traverse();
     printf("Descending order of Marks: ");
  //  traverseByMark();
    }
}
