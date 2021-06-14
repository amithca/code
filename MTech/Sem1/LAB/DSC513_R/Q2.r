# Write a R program to test whether a given vector contains a specified element.
# 1) 42      2) 9
# You may use the input to vector as -> 10, 20, 30, 25, 9, 26
# Hint: Use is.element() function 
# 
# Ans:
  
x<-c(10,20,30,25,9,26)
cat("x=[",x,"]\n")
print("--------------------------")
print("case 1, Test for 42")
print(is.element(42,x))
print("case 2, test for 9")
print(is.element(9,x))