##memory clear
rm(list = ls())

#Set working directory To Project Directory 
setwd("D:\\Stock_Prediction")

#loadning data
library(readxl)
stock_data <- read_excel("D:/Stock_Prediction/owner_2018Q2.xlsx")
View(stock_data)

#Necessary data to apply model (High Fund Value)
grp1_data = subset(stock_data, Sector_ID==1)
grp2_data = subset(stock_data, Sector_ID==2)
grp3_data = subset(stock_data, Sector_ID==3)
grp5_data = subset(stock_data, Sector_ID==5)
grp6_data = subset(stock_data, Sector_ID==6)
grp7_data = subset(stock_data, Sector_ID==7)
grp8_data = subset(stock_data, Sector_ID==8)
grp10_data = subset(stock_data, Sector_ID==10)
grp11_data = subset(stock_data, Sector_ID==11)

#Combining all dataframe
comb_data = rbind(grp1_data,grp2_data,grp3_data,grp5_data,grp6_data,grp7_data,grp10_data,grp11_data)
comb_data1 = as.data.frame(comb_data)

#remove zero variance variables
comb_data2 = subset(comb_data1, select = -c(IsOwner, ActivePassive, InvestorStyle, AUM, Turnover))
#Manually remove few variables
comb_data3 = subset(comb_data2, select = -c(fund_id,stock_id, QDate))

#Investordata
Investor_data = comb_data3[,1:16]

#making stock price numeric
#Investor_data1 <- as.data.frame(sapply(Investor_data$stock_price, as.numeric)) #<- sapply is here
#colnames(Investor_data1) = "stock_price"

#Fund data
fund_data = comb_data3[, 17:97]

#Convert to numeric
fund_data1 <- as.data.frame(sapply(fund_data, as.numeric)) #<- sapply is here

## Remove columns with more than 60% NA
fund_data2 = fund_data1[, -which(colMeans(is.na(fund_data1)) > 0.6)]

#Final_data
final_data = cbind(Investor_data,fund_data2)



################# Check Multicolinearity ###############################################################
library(caret)
#Dropping dependent variable
data.drop.dep = subset(final_data, select = -c(ClassInd,ActionTaken))

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
data_selected <- final_data[, -which(colnames(final_data) %in% highlyCorCol)]
dim(data_selected)







#########################################################################################################

learn.cart <- ofw(comb_data1, as.factor(ClassInd), type = "CART",
                  ntree = 150, nforest = 2500, mtry = 5)
learn.svm <- ofw(srbct, as.factor(ClassInd), type = "SVM",
                    nsvm = 30000, mtry = 5)







# ensure results are repeatable
set.seed(7)
# load the library
library(mlbench)
library(caret)
# load the dataset
#data(PimaIndiansDiabetes)
# prepare training scheme
control <- trainControl(method="repeatedcv", number=10, repeats=3)
# train the model
model <- train(ClassInd~., data=comb_data1, method="lvq", preProcess="scale", trControl=control)
# estimate variable importance
importance <- varImp(model, scale=FALSE)
# summarize importance
print(importance)
# plot importance
plot(importance)

# Sampling (0.7 , 0.3)
set.seed(1234)
ind<- sample(2, nrow(data_linear), replace=TRUE, prob=c(0.7,0.3))
trainData=data_linear[ind==1,]
testData=data_linear[ind==2,]
#feature engineering
#Information value and Weight of evidence
library(woe)
library(riv)

library(devtools)

install_github("tomasgreif/riv","tomasgreif",force=TRUE)

library(woe)

#information value calcuation
iv_df <- iv.mult(comb_data, y="ClassInd", summary=TRUE, verbose=TRUE)
#iv <- iv.mult(selected_var, y="STSPOL", summary=FALSE, verbose=TRUE)







#Sampling (splitting dataframe for trainning and testing)
train_rows = sample( 1:nrow( comb_data2 ), floor( 0.8*nrow( comb_data2 ) ) )
train_df = comb_data2[ train_rows, ] ; test_df = comb_data2[ -train_rows, ]

#model building (Stochastic Gradient Boosting)
library(caret)
library(MLmetrics)
objControl <- trainControl(method='cv', number=3, returnResamp='none', summaryFunction = multiClassSummary, classProbs = TRUE)
objModel <- train(train_df[,setdiff(names(train_df),'ActionTaken')], train_df[,'ActionTaken'], 
                  method='gbm', 
                  trControl=objControl,  
                  metric = "ROC",
                  preProc = c("center", "scale"))

#model summary
summary(objModel)
print(objModel)