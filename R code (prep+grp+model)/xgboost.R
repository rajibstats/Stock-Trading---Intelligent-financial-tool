#remove zero variance variables
data_grp1_selected1 = subset(stock_data_grp3, select = -c(ActivePassive, InvestorStyle, AUM, Turnover))

# Sampling (0.7 , 0.3)
set.seed(1234)
ind<- sample(2, nrow(data_grp1_selected1), replace=TRUE, prob=c(0.7,0.3))
trainData=data_grp1_selected1[ind==1,]
testData=data_grp1_selected1[ind==2,]



#Train data
data_grp1_Train = trainData[,4:89]

#Test Data
data_grp1_Test = testData[,4:89]


#remove zero variance variables
data_Train = data_grp1_Train
data_Test = data_grp1_Test

data_Train$ClassInd[data_Train$ClassInd == -1] <- 2
data_Train$ClassInd[data_Train$ClassInd == 0] <-3

library(xgboost)

train <- data.matrix(data_Train)
classes <- as.numeric(data_Train$ClassInd)

numberOfClasses <- length(unique(classes))
xgb <- xgboost(data = train, 
               label = classes, 
               eta = 0.1,
               max_depth = 6, 
               nround=100, 
               objective = "multi:softmax",
               num_class = numberOfClasses+1,
               nthread = 3)

result   <- predict(xgb, data.matrix(data_Test))
