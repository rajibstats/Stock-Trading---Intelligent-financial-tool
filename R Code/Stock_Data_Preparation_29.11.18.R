##memory clear
rm(list = ls())

#Set working directory To Project Directory 
#setwd("D:\\Stock_Prediction")

#Step-1
#loadning data
library(data.table)
stock_data <- fread("D:\\Stock_Prediction\\data\\Non_Owner\\fund641_nonOwner.csv")
#View(stock_data)
#stock_data = data

#Remove columns (unnecessary)
#library(dplyr)
#RemoveToCols = c("StockWeightage","SectorWeightage","id","Fund_id","Stock_Id","QDate","status","ClassDate")
#stock_data1 = stock_data[,!(names(stock_data) %in% RemoveToCols)]
stock_data1 = subset(stock_data, select = -c(StockWeightage,SectorWeightage,id,Fund_id,Stock_Id,QDate,status,ClassDate) )
stock_data2 = stock_data1[,-1]
target_data = stock_data1[,1]
#Convert to Numeric
stock_data2[] <- lapply(stock_data2, function(x) as.numeric(as.character(x)))


#Numeric_data4 <- as.data.frame(apply(Numeric_data1, 2, function(x) (x - min(x))/(max(x)-min(x))))
normalize_data <- scale(stock_data2)
#Normalize values in the matrix using the function
#Numeric_data5 <- t(apply(Numeric_data1, 1, nor.min.max))
#Numeric_data3 = normalize(Numeric_data1, method = "standardize", range = c(0, 1), margin = 2L, on.constant = "quiet")
#Final dataFrame
final_data = cbind(target_data, normalize_data)


