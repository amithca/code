/*
Write a C program to build a Binary Search Tree using the following elements: 45, 39, 56, 12, 34, 78, 32, 10, 89, 54, 67, 81

Do In-order Traversal on the constructed Binary Search Tree.

Sample Input/Output
Input

45, 39, 56, 12, 34, 78, 32, 10, 89, 54, 67, 81, -999
Output 

In-order Traversal of the Binary Search Tree Constructed: 10, 12, 32, 34, 39, 45, 54, 56, 67, 78, 81, 89
*/

#include<stdio.h>
#include<stdlib.h>
struct node{
    int key;
    struct node *left,*right;
};
struct node *r=NULL;
struct node *newNode(int item){
    struct node *temp=(struct node *)malloc(sizeof(struct node));
    temp->key=item;
    temp->left=temp->right=NULL;
    return temp;

}
void inorder(struct node *root){
    if(root!=NULL){
        inorder(root->left);
        printf("%d, ",root->key);
        inorder(root->right);
    }
}
struct node *insert(struct node *node,int key){
    if(node==NULL)
        return newNode(key);
    if(key<node->key)
        node->left=insert(node->left,key);
    else
        node->right=insert(node->right,key);
    return node;
}

struct node *minValueNode(struct node *node){
    struct node *current=node;
    while(current&&current->left!=NULL)
        current=current->left;
    return current;
}
int read_input(){
     
     int v_inp;
     scanf("%d,",&v_inp);
     if(v_inp==-999){
         return -1;
     }else{
          r=insert(r,v_inp);
         while(v_inp!=-999){
             scanf("%d,",&v_inp);
             if(v_inp==-999){
                 break;
             }
             r=insert(r,v_inp);
         }
     }
   return 0;
}
int main(){
    read_input();
    printf("In-order Traversal of the Binary Search Tree Constructed: ");
    inorder(r);
}