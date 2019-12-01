#install.packages("xgboost")
#install.packages("cvAUC")
library(xgboost)
library(Matrix)
library(cvAUC)
# Load 2-class HIGGS dataset
#train <- read.csv("data/higgs_train_10k.csv")
#test <- read.csv("data/higgs_test_5k.csv")
# Set seed because we column-sample

# Make split index
train_index <- sample(1:nrow(data_grp1_selected1), nrow(data_grp1_selected1)*0.75)
# Full data set
data_variables <- as.matrix(data_grp1_selected1[,-85])
data_label <- data_grp1_selected1[,"ClassInd"]
data_matrix <- xgb.DMatrix(data = as.matrix(data_grp1_selected1), label = data_label)
# split train data and make xgb.DMatrix
train_data   <- data_variables[train_index,]
train_label  <- data_label[train_index]
dtrain <- xgb.DMatrix(data = train_data, label = train_label)
# split test data and make xgb.DMatrix
test_data  <- data_variables[-train_index,]
test_label <- data_label[-train_index]
dtest <- xgb.DMatrix(data = test_data, label = test_label)


train.gdbt <- xgb.train(params = list(objective = "multi:softprob",
                                      num_class = 5,
                                      eval_metric = "mlogloss",
                                      eta = 0.3,
                                      max_depth = 5,
                                      subsample = 1,
                                      colsample_bytree = 0.5), 
                        data = dtrain, 
                        nrounds = 70, 
                        watchlist = list(train = dtrain, test = dtest))
# Generate predictions on test dataset
preds <- predict(train.gdbt, newdata = dtest)
labels <- test[,y]

# Compute AUC on the test set
cvAUC::AUC(predictions = preds, labels = labels)
confusionMatrix(preds, levels)
#Advanced functionality of xgboost
#install.packages("Ckmeans.1d.dp")
library(Ckmeans.1d.dp)

# Compute feature importance matrix
names <- dimnames(data.matrix(train[,-1]))[[2]]
importance_matrix <- xgb.importance(names, model = train.gdbt)

# Plot feature importance
xgb.plot.importance(importance_matrix[1:10,])


OOF_prediction <- data.frame(train.gdbt$pred) %>%
  mutate(max_prob = max.col(., ties.method = "last"),
         label = train_label + 1)
head(OOF_prediction)

# confusion matrix
confusionMatrix = confusionMatrix(factor(OOF_prediction$max_prob),
                                  factor(OOF_prediction$label),
                                  mode = "everything")