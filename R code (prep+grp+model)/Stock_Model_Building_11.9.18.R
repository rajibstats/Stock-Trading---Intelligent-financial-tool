#Link: https://github.com/ledell/useR-machine-learning-tutorial/blob/master/gradient-boosting-machines.Rmd

#
data_grp1_selected = stock_data_grp1[,5:93]
data_grp1_selected$ClassInd[data_grp1_selected$ClassInd == -1] <- 2
data_grp1_selected$ClassInd[data_grp1_selected$ClassInd == 0] <-3

#remove zero variance variables
data_grp1_selected1 = subset(data_grp1_selected, select = -c(ActivePassive, InvestorStyle, AUM, Turnover))

# Sampling (0.7 , 0.3)
set.seed(1234)
ind<- sample(2, nrow(data_grp1_selected1), replace=TRUE, prob=c(0.7,0.3))
trainData=data_grp1_selected1[ind==1,]
testData=data_grp1_selected1[ind==2,]
#install.packages("gbm")
#install.packages("cvAUC")
library(gbm)
library(cvAUC)
# Load 2-class HIGGS dataset
#train <- read.csv("data/higgs_train_10k.csv")
#test <- read.csv("data/higgs_test_5k.csv")
set.seed(1)
model <- gbm(formula = ClassInd ~ ., 
             distribution = "gaussian",
             data = trainData,
             n.trees = 70,
             interaction.depth = 5,
             shrinkage = 0.3,
             bag.fraction = 0.5,
             train.fraction = 1.0,
             n.cores = NULL)  #will use all cores by default
print(model)
# Generate predictions on test dataset
preds <- predict(model, newdata = testData, n.trees = 70)
labels <- testData[,"ClassInd"]



# Compute AUC on the test set
cvAUC::AUC(predictions = preds, labels = labels)
