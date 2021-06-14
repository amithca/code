/*
Write a C program to read name and total marks of students in a batch.

The program must sort student names in alphabetical order. The program must also sort student list based on descending order of marks. 

You must use multi-linked lists with various links following ascending ordered marks and alphabetically ordered records.

If two students have same marks display them alphabetically. If two students have the same name display the details of the student with highest marks first.

Note: Marks cannot be negative. The name of a student only consists of capital and small English alphabets.

Sample Input/Output
Input
    James
    56
    Paul
    39
    Augustine
    12
    William
    85
    Kishan
    35
    Rithi Sing
    85
    Kishan
    55
    -999    
Output
    Descending order of Marks: Rithi Sing 85, William 85, James 56, Kishan 55, Paul 39, Kishan 35, Augustine 12,
    Alphabetical Order: Augustine 12, James 56, Kishan 55, Kishan 35, Paul 39, Rithi Sing 85, William 85,

*/

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
        if(isalpha(a[i])<=0 && a[i]!=' ')
            flg=-1;
    }
    return flg;
}
int is_valid_mark(char *a){
    int len=0;
    int flg=0;
    len=strlen(a);
    for(int i=0;i<len;i++){
        if(!isdigit(a[i])>0){
            if(i==0 && a[i]=='-'){
                continue;
            }else{
            flg=-1;
            break;
            }
        }
    }
    return flg;
}
int create_llist(){
    char v_inp_nam[100],tmp_inp_mark[100];
    int v_inp_mark;
    int c=0,len=0;
    node *ptr,*new_node,*markptr,*nameptr, *tmpPrevMark;
    fgets(v_inp_nam,100,stdin);
    len=strlen(v_inp_nam);
    if(len>0&&v_inp_nam[len-1]=='\n'){
        v_inp_nam[--len]='\0';
    }
    if(strcmp(v_inp_nam,"-999")==0){
        return -4;
    }else{
         if(is_valid_name(v_inp_nam)==-1 ){
            return -1;
        }
    }
    scanf("%s",tmp_inp_mark);
    getchar();
     if(is_valid_mark(tmp_inp_mark)==-1 ){
        return -2;
    }else{
        v_inp_mark=atoi(tmp_inp_mark);
     }
    if (v_inp_mark<0){
        return -3;
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
        c++;
    }
    while(strcmp(v_inp_nam,"-999")!=0){
        fgets(v_inp_nam,100,stdin);
        len=strlen(v_inp_nam);
        if(len>0&&v_inp_nam[len-1]=='\n'){
             v_inp_nam[--len]='\0';
        }
        if(strcmp(v_inp_nam,"-999")==0 ){
            break;
        }
         if(is_valid_name(v_inp_nam)==-1 ){
            return -1;
        }
        scanf("%s",tmp_inp_mark);
        getchar();
         if(is_valid_mark(tmp_inp_mark)==-1 ){
            return -2;
        }else{
            v_inp_mark=atoi(tmp_inp_mark);
        }
         c++;
        if(v_inp_mark<0){
               return -3;
        }
        new_node=(node*)malloc(sizeof(node));
        if(new_node==NULL){
            printf("Overflow");
            return 0;
        }
        strcpy(new_node->nam,v_inp_nam);
        new_node->mark=v_inp_mark;
        new_node->next=NULL;
        new_node->marks_next=NULL;
        new_node->lex_next=NULL;
        ptr->next=new_node;
        ptr->marks_next=new_node;
        ptr->lex_next=new_node;
        new_node=new_node->next;
        ptr=ptr->next;
    }
    
    return c;
}
void split_list(node *hd,node **front,node **back,int flg){
    node *tmp_last,*tmp_mid;
    if(flg==0){
        //Mark
    tmp_mid=hd;
    tmp_last=hd->marks_next;
    while(tmp_last!=NULL){
        tmp_last=tmp_last->marks_next;
        if(tmp_last!=NULL){
            tmp_mid=tmp_mid->marks_next;
            tmp_last=tmp_last->marks_next;
        }
    }
    *front=hd;
    *back=tmp_mid->marks_next;
    tmp_mid->marks_next=NULL;
    }else{
        //Name
          tmp_mid=hd;
    tmp_last=hd->lex_next;
    while(tmp_last!=NULL){
        tmp_last=tmp_last->lex_next;
        if(tmp_last!=NULL){
            tmp_mid=tmp_mid->lex_next;
            tmp_last=tmp_last->lex_next;
        }
    }
    *front=hd;
    *back=tmp_mid->lex_next;
    tmp_mid->lex_next=NULL;
    }
}
node* SortedMerge(node *a,node *b,int flg){
    node* result=NULL;
    if(a==NULL)
    return b;
    else if(b==NULL)
    return a;
    if(flg==0){
        //Marks
        if(a->mark>b->mark){
            result=a;
            result->marks_next=SortedMerge(a->marks_next,b,flg);
        }else if(a->mark==b->mark){
            if(strcmp(a->nam,b->nam)<=0){
            result=a;
            result->marks_next=SortedMerge(a->marks_next,b,flg);
            }else{
                 result=b;
            result->marks_next=SortedMerge(a,b->marks_next,flg);
            }
        }
        else {
            result=b;
            result->marks_next=SortedMerge(a,b->marks_next,flg);
        }
   
    }else{
        //Name
        if(strcmp(a->nam,b->nam)<0){
            result=a;
            result->lex_next=SortedMerge(a->lex_next,b,flg);
        }else  if(strcmp(a->nam,b->nam)==0){
            if(a->mark>=b->mark){
            result=a;
            result->lex_next=SortedMerge(a->lex_next,b,flg);
            }else{
                result=b;
                result->lex_next=SortedMerge(a,b->lex_next,flg);
            }
        }else {
            result=b;
            result->lex_next=SortedMerge(a,b->lex_next,flg);
        }
    }
    return result;
}
void MergeSort(node** headRef,int flg){
    node* tmp_head=*headRef;
    node* a;
    node* b;
    if(flg==0){
    if((tmp_head==NULL)||(tmp_head->marks_next==NULL)){
        return;
    }
    split_list(tmp_head,&a,&b,flg);
    MergeSort(&a,flg);
    MergeSort(&b,flg);
    *headRef=SortedMerge(a,b,flg);
    }else{
         if((tmp_head==NULL)||(tmp_head->lex_next==NULL)){
        return;
    }
    split_list(tmp_head,&a,&b,flg);
    MergeSort(&a,flg);
    MergeSort(&b,flg);
    *headRef=SortedMerge(a,b,flg);
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
         printf("%s %d,\n",ptr->nam,ptr->mark);
    }
}
void traverseByName(){
    node *ptr;
    if(headByName==NULL){
        return ;
    }else{
        ptr=headByName;
        while(ptr->lex_next!=NULL){
            printf("%s %d,",ptr->nam,ptr->mark);
            ptr=ptr->lex_next;
        }
         printf("%s %d,\n",ptr->nam,ptr->mark);
    }
}
int main(){
    int a;
    a=create_llist();
    if( a==-1){
        printf("Input Error!!! Name of a student should only have alphabets.");
    }else if (a==-2){
        printf("Input Error!!! Marks Missing");
    }else if(a==-3){
        printf("Marks cannot be negative");
    }else if (a==-4){
        printf("You must enter atleast one student.");
    }else if (a>0){
        MergeSort(&headByMarks,0);//Set the marks_next pointer in proper order
        MergeSort(&headByName,1);//Set the lex_next pointer in proper order
        printf("Descending order of Marks: ");
        traverseByMark();
        printf("Alphabetical order: ");
        traverseByName();
    }
}
