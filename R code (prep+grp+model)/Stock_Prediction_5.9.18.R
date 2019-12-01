##memory clear
rm(list = ls())

#Set working directory To Project Directory 
setwd("D:\\Stock_Prediction")

#Step-1
#loadning data
library(readxl)
stock_data <- read_excel("D:/Stock_Prediction/owner_2018Q2.xlsx")
View(stock_data)

#Removing few unnecessary columns
#remove zero variance variables
stock_data1 = subset(stock_data, select = -c(IsOwner,ActivePassive, InvestorStyle, AUM, Turnover))
#Manually remove few variables
stock_data2 = subset(stock_data1, select = -c(fund_id,stock_id, QDate))

#Investordata
Investor_data = stock_data2[,1:16]


#making stock price numeric
#Investor_data1 <- as.data.frame(sapply(Investor_data$stock_price, as.numeric)) #<- sapply is here
#colnames(Investor_data1) = "stock_price"

#Fund data
fund_data = stock_data2[,17:97]

#Convert to numeric
fund_data1 <- as.data.frame(sapply(fund_data, as.numeric)) #<- sapply is here

#Step-2
## Remove columns with 100% NA
library(dplyr)
not_all_na <- function(x) any(!is.null(x))
fund_data2 = fund_data1 %>% select_if(not_all_na)

#Final_data
final_data = cbind(Investor_data,fund_data2)



#Step-3
#Necessary data to apply model (High Fund Value)
sec1_data = subset(final_data, Sector_ID==1)
sec2_data = subset(final_data, Sector_ID==2)
sec3_data = subset(final_data, Sector_ID==3)
sec4_data = subset(final_data, Sector_ID==4)
sec5_data = subset(final_data, Sector_ID==5)
sec6_data = subset(final_data, Sector_ID==6)
sec7_data = subset(final_data, Sector_ID==7)
sec8_data = subset(final_data, Sector_ID==8)
sec9_data = subset(final_data, Sector_ID==9)
sec10_data = subset(final_data, Sector_ID==10)
sec11_data = subset(final_data, Sector_ID==11)


#Step-4
#Remove columns depending 70% missing (NULL)
## Remove columns with more than 60% NA
sec1_data_clean = sec1_data[, -which(colMeans(is.na(sec1_data)) > 0.7)]
sec2_data_clean = sec2_data[, -which(colMeans(is.na(sec2_data)) > 0.7)]
sec3_data_clean = sec3_data[, -which(colMeans(is.na(sec3_data)) > 0.7)]
sec4_data_clean = sec4_data[, -which(colMeans(is.na(sec4_data)) > 0.7)]
sec5_data_clean = sec5_data[, -which(colMeans(is.na(sec5_data)) > 0.7)]
sec6_data_clean = sec6_data[, -which(colMeans(is.na(sec6_data)) > 0.7)]
sec7_data_clean = sec7_data[, -which(colMeans(is.na(sec7_data)) > 0.7)]
sec8_data_clean = sec8_data[, -which(colMeans(is.na(sec8_data)) > 0.7)]
see9_data_clean = sec9_data[, -which(colMeans(is.na(sec9_data)) > 0.7)]
sec10_data_clean = sec10_data[, -which(colMeans(is.na(sec10_data)) > 0.7)]
sec11_data_clean = sec11_data[, -which(colMeans(is.na(sec11_data)) > 0.7)]

#creating grp1 selecting same variables
sec12356781011_data_grp1 = rbind(sec1_data_clean,sec2_data_clean,sec3_data_clean,sec5_data_clean,
                                 sec6_data_clean,sec7_data_clean,sec8_data_clean,sec10_data_clean,
                                 sec11_data_clean)

#Creating grp2
sec4_data_grp2 = sec4_data_clean

#Creating grp3
sec9_data_grp3 = sec9_data_clean



################# Check Multicolinearity ###############################################################
library(caret)
#Dropping dependent variable
data.drop.dep = subset(sec12356781011_data_grp1, select = -c(ClassInd,ActionTaken))

#Identifying numeric variables
numericData <- data.drop.dep[sapply(data.drop.dep, is.numeric)]

#Calculating Correlation
#descrCor <- cor(numericData, use = "pairwise.complete.obs")
descrCor <- cor(numericData, use = "complete.obs")
highlyCorrelated <- findCorrelation(descrCor, cutoff=0.75)
highlyCorrelated

#Identifying Variable Names of Highly Correlated Variables
highlyCorCol <- colnames(numericData)[highlyCorrelated]

#Print highly correlated attributes
highlyCorCol

#Remove highly correlated variables and create a new dataset
data_selected <- sec12356781011_data_grp1[, -which(colnames(sec12356781011_data_grp1) %in% highlyCorCol)]
dim(data_selected)


