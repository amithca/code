# Write a R program to extract 3rd and 5th rows with 1st and 3rd columns from a given data frame.[You may create your own data frame] 
# 
# Ans:

a<-c(1,2,3,4,5)
df<-data.frame(a)
names(df)<-"ID"
df$ITEM<-c("Book","Pen","Pencil","Stapler","Eraser")
df$PRICE<-c(250.5,5,3.5,25.0,5)
df$AVAILABILITY<-factor(c("A","NA","A","NA","NA"))
print("DATAFRAME:")
print(df)
print("-----------------------------------------")
print("EXTRACT:")
print(df[c(3,5),c("ID","PRICE")])