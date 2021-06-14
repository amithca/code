/*
Write C program to find the Huffman encoding for a given String.

Sample Input/Output
Input

sseasoseoeaieiestseossieiaeiuiaieeiaeueaiuiasaeieauasisess

Output [Note: Huffman Code must be displayed in alphabetical order to match with the test cases]
a = 111

e = 10

i = 00

o = 11001

s = 01

t = 11000

u = 1101



*/


#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<ctype.h>
#define MAX_TREE_HT 100
typedef struct tmp{
    char arr;
    char cnt[20];
}node;
node out[26];
int x=0;
struct MinHeapNode{
    char data;
    unsigned  freq;
    struct MinHeapNode *left,*right;
};
struct MinHeap{
    unsigned size;
    unsigned capacity;
    struct MinHeapNode** array;
};
struct MinHeapNode* newNode(char data,unsigned freq){
    struct MinHeapNode* temp=(struct MinHeapNode*)malloc(sizeof(struct MinHeapNode));
    temp->left=temp->right=NULL;
    temp->data=data;
    temp->freq=freq;
    return temp;
}
struct MinHeap* createMinHeap(unsigned capacity){
    struct MinHeap* minHeap=(struct MinHeap*)malloc(sizeof(struct MinHeap));
    minHeap->size=0;
    minHeap->capacity=capacity;
    minHeap->array=(struct MinHeapNode**)malloc(minHeap->capacity * sizeof(struct MinHeapNode*));
    return minHeap;
}
void swapMinHeapNode(struct MinHeapNode** a, struct MinHeapNode** b){
    struct MinHeapNode* t = *a;
    *a=*b;
    *b=t;
}
void minHeapify(struct MinHeap* minHeap, int idx){
    int smallest=idx;
    int left = 2*idx +1;
    int right=2*idx+2;
    if(left<minHeap->size && minHeap->array[left]->freq<minHeap->array[smallest]->freq)
        smallest=left;
    if(right<minHeap->size&&minHeap->array[right]->freq<minHeap->array[smallest]->freq)
        smallest=right;
    if(smallest!=idx){
        swapMinHeapNode(&minHeap->array[smallest],&minHeap->array[idx]);
        minHeapify(minHeap,smallest);
    }
}
int isSizeOne(struct MinHeap* minHeap){
    return (minHeap->size ==1);
}
struct MinHeapNode* extractMin(struct MinHeap* minHeap){
    struct MinHeapNode* temp=minHeap->array[0];
    minHeap->array[0]=minHeap->array[minHeap->size-1];
    --minHeap->size;
    minHeapify(minHeap,0);
    return temp;
}
void insertMinHeap(struct MinHeap* minHeap, struct MinHeapNode* minHeapNode){
    ++minHeap->size;
    int i =minHeap->size-1;
    while(i&&minHeapNode->freq<minHeap->array[(i-1)/2]->freq){
        minHeap->array[i]=minHeap->array[(i-1)/2];
        i=(i-1)/2;
    }
    minHeap->array[i]=minHeapNode;
}

void buildMinHeap(struct MinHeap* minHeap){
    int n=minHeap->size-1;
    int i;
    for(i=(n-1)/2;i>=0;--i)
        minHeapify(minHeap,i);
}
void printArr(int arr[],int n){
    int i;
    int y=0;
    for(i=0;i<n;++i){
        //printf("%d",arr[i]);
       y+=sprintf(&out[x].cnt[y],"%d",arr[i]);
        
    }
    x++;
    //printf("\n");
}
int isLeaf(struct MinHeapNode* root){
    return !(root->left)&&!(root->right);
}
struct MinHeap* createAndBuildMinHeap(char data[], int freq[], int size){
    struct MinHeap* minHeap=createMinHeap(size);
    for(int i=0;i<size;++i)
        minHeap->array[i]=newNode(data[i],freq[i]);
        minHeap->size=size;
        buildMinHeap(minHeap);
        return minHeap;
        
}
struct MinHeapNode* buildHuffmanTree(char data[],int freq[],int size){
    struct MinHeapNode *left,*right,*top;
    struct MinHeap* minHeap=createAndBuildMinHeap(data,freq,size);
    while(!isSizeOne(minHeap)){
        left=extractMin(minHeap);
        right=extractMin(minHeap);
        top=newNode('$',left->freq+right->freq);
        top->left=left;
        top->right=right;
        insertMinHeap(minHeap,top);
        
    }
    return extractMin(minHeap);
}
void  printCodes(struct MinHeapNode* root,int arr[],int top){
    if(root->left){
        arr[top]=0;
        printCodes(root->left,arr,top+1);
        
    }
    if(root->right){
        arr[top]=1;
        printCodes(root->right,arr,top+1);
    }
    if(isLeaf(root)){
        //printf("\n%c = ",root->data);
        out[x].arr=root->data;
        printArr(arr,top);
    }
}
void HuffmanCodes(char data[],int freq[],int size){
    struct MinHeapNode* root=buildHuffmanTree(data,freq,size);
    int arr[MAX_TREE_HT],top=0;
    printCodes(root,arr,top);
}

int main(){
    
    char arr[26],inp[100],c,tmp_arr,tmp_freq[20];
    int freq[26],counts[26]={0};
    int len,n=0,flg=0,i=0,j=0;
    fgets(inp,100,stdin);
    len=strlen(inp);
    if(inp[len-1]=='\n'&&len==1){
        fgets(inp,100,stdin);
    }
    len=strlen(inp);
    i=0;
  for(i=0;i<len;i++){
      char c=inp[i];
      if(!isalpha(c)) continue;
      counts[(int)(tolower(c)-'a')]++;
  }
  for(i=0;i<26;i++){
      if(counts[i]!=0){
          arr[n]=i+'a';
          freq[n]=counts[i];
          n++;
      }
    
  }

/*for(i=0;i<n;i++){
    printf("arr=%c,freq=%d\n",arr[i],freq[i]);
}*/
    //int size=n/sizeof(arr[0]);
 int size=n;
    HuffmanCodes(arr,freq,size);
    
    for(i=0;i<x-1;i++){
    for(j=0;j<x-i-1;j++){
        if(out[j].arr>out[j+1].arr){
            tmp_arr=out[j].arr;
            strcpy(tmp_freq,out[j].cnt);
            out[j]=out[j+1];
            //out[j]=freq[j+1];
            out[j+1].arr=tmp_arr;
            strcpy(out[j+1].cnt,tmp_freq);
        }
    }
}
   // printf("OUT:\n");
    for(i=0;i<x;i++){
        printf("%c = %s\n",out[i].arr,out[i].cnt);
    }
    return 0;
}