#Link: https://rpubs.com/mharris/multiclass_xgboost

#
data_grp1_selected = stock_data_grp3[,5:93]
data_grp1_selected$ClassInd[data_grp1_selected$ClassInd == -1] <- 2
data_grp1_selected$ClassInd[data_grp1_selected$ClassInd == 0] <-3

#remove zero variance variables
data_grp1_selected1 = subset(data_grp1_selected, select = -c(ActivePassive, InvestorStyle, AUM, Turnover))


library("xgboost")  # the main algorithm
library("archdata") # for the sample dataset
library("caret")    # for the confusionmatrix() function (also needs e1071 package)
library("dplyr")    # for some data preperation
#library("Ckmeans.1d.dp") # for xgb.ggplot.importance

# Make split index
train_index <- sample(1:nrow(data_grp1_selected1), nrow(data_grp1_selected1)*0.75)
# Full data set
data_variables <- as.matrix(data_grp1_selected1[,-85])
data_label <- data_grp1_selected1[,"ClassInd"]
data_matrix <- xgb.DMatrix(data = as.matrix(data_grp1_selected1), label = data_label)
# split train data and make xgb.DMatrix
train_data   <- data_variables[train_index,]
train_label  <- data_label[train_index]
train_matrix <- xgb.DMatrix(data = train_data, label = train_label)
# split test data and make xgb.DMatrix
test_data  <- data_variables[-train_index,]
test_label <- data_label[-train_index]
test_matrix <- xgb.DMatrix(data = test_data, label = test_label)



numberOfClasses <- length(unique(data_grp1_selected1$ClassInd))
xgb_params <- list("objective" = "multi:softprob",
                   "eval_metric" = "mlogloss",
                   "num_class" = numberOfClasses+1)
nround    <- 50 # number of XGBoost rounds
cv.nfold  <- 5

# Fit cv.nfold * cv.nround XGB models and save OOF predictions
cv_model <- xgb.cv(params = xgb_params,
                   data = train_matrix, 
                   nrounds = nround,
                   nfold = cv.nfold,
                   verbose = FALSE,
                   prediction = TRUE)




OOF_prediction <- data.frame(cv_model$pred) %>%
  mutate(max_prob = max.col(., ties.method = "last"),
         label = train_label + 1)
head(OOF_prediction)

# confusion matrix
confusionMatrix = confusionMatrix(factor(OOF_prediction$max_prob),
                factor(OOF_prediction$label),
                mode = "everything")


confusionMatrix

bst_model <- xgb.train(params = xgb_params,
                       data = train_matrix,
                       nrounds = nround)




# Predict hold-out test set
test_pred <- predict(bst_model, newdata = test_matrix)
test_prediction <- matrix(test_pred, nrow = numberOfClasses+1,
                          ncol=length(test_pred)/numberOfClasses+1) %>%
  t() %>%
  data.frame() %>%
  mutate(label = test_label + 1,
         max_prob = max.col(., "last"))
# confusion matrix of test set
confusionMatrix(factor(test_prediction$max_prob),
                factor(test_prediction$label),
                mode = "everything")



# predict for softmax returns num_class probability numbers per case:
pred <- predict(bst_model, newdata = test_matrix)
str(pred)
# reshape it to a num_class-columns matrix
pred <- matrix(pred, ncol=numberOfClasses, byrow=TRUE)
# convert the probabilities to softmax labels
pred_labels <- max.col(pred) - 1
