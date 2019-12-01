##memory clear
rm(list = ls())

#Set working directory To Project Directory 
setwd("D:\\Stock_Prediction")

#Step-1
#loadning data
library(readxl)
stock_data <- read_excel("D:/Stock_Prediction/owner_2018Q2.xlsx")
#View(stock_data)
#stock_data = data

#Remove columns (unnecessary)
library(dplyr)
RemoveToCols = c("ActionTaken","Cap_Size","IsOwner","Fund Name","Stock Name","industry","Sector" )
stock_data1 = stock_data[,!(names(stock_data) %in% RemoveToCols)]


#making classind as a last column
stock_data2 = stock_data1 %>% select(fund_id:sharevalue,stock_price:tot_debt,starts_with('ClassInd'))

#Putting sharevalue and stockprice in front of asset_turn
stock_data3 = stock_data2[,c(1:4, 7:18, 5:6, 19:98)]


#Aging Manipulation 
stock_data3$Aging = stock_data3$Aging/365

stock_data3$Aging[stock_data3$Aging <5] <- 1
stock_data3$Aging[stock_data3$Aging >5] <- 2

#Creating Age_Range instead of Aging
colnames(stock_data3)[colnames(stock_data3) == 'Aging'] <- 'Age_Range'


##CAtegorical Data
categorical_data = stock_data3[,1:16]

#Numetic Data
Numeric_data = stock_data3[,17:97]

#Target Data
Target_data = stock_data3[,98]

#Convert to Numeric
Numeric_data1 = as.data.frame((sapply(Numeric_data, as.numeric)))

# Scale all numeric columns in a data frame.

#performScaling <- TRUE  # Turn it on/off for experimentation.

#if (performScaling) {
  
  # Loop over each column.
  #for (colName in names(Numeric_data1)) {
    
    # Check if the column contains numeric data.
    #if(class(Numeric_data1[,colName]) == 'integer' | class(Numeric_data1[,colName]) == 'numeric') {
      
      # Scale this column (scale() function applies z-scaling).
      #Numeric_data1[,colName] <- scale(Numeric_data1[,colName])
#    }
#  }
#}
#Numeric_data4 <- as.data.frame(apply(Numeric_data1, 2, function(x) (x - min(x))/(max(x)-min(x))))
Numeric_data2 <- scale(Numeric_data1)
#Normalize values in the matrix using the function
#Numeric_data5 <- t(apply(Numeric_data1, 1, nor.min.max))
#Numeric_data3 = normalize(Numeric_data1, method = "standardize", range = c(0, 1), margin = 2L, on.constant = "quiet")
#Final dataFrame
final_data = cbind(categorical_data, Numeric_data2, Target_data)


