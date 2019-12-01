#stock.hex = data_grp1_selected1
#install.packages("h2o")
library(h2o)
#setwd("D:\\Stock_Prediction\\data\\data10.03")
#h2o.shutdown(prompt = FALSE)  #if required
#h2o.init(nthreads = -1)  #Start a local H2O cluster using nthreads = num available cores
h2o.init()
stock_data.hex <- h2o.importFile("D:\\Rajib Documents\\MEGAsync\\MEGAsync\\UpWork\\Stock Market\\INTC Historical Data.csv")



drops <- c("Date", "open_indicator", "high_indicator", "low_indicator")
Stock_data = stock_data.hex[ , !(names(stock_data.hex) %in% drops)]


Stock_data$Vol.= substr(Stock_data$Vol.,1,nchar(Stock_data$Vol.)-1)

Stock_data1 <- data.frame(sapply(Stock_data, function(x) as.numeric(gsub("%", "", x))))
dataset = Stock_data1
# Make split index

stock_data.split <- h2o.splitFrame(dataset, ratios = c(0.2, 0.7))
test = stock_data.split[[1]]
train = stock_data.split[[2]]
validate = stock_data.split[[3]]


print(dim(train))
print(dim(test))
print(dim(validate))

# Identity the response column
y <- "ClassInd"

# Identify the predictor columns
x <- setdiff(names(train), y)

# Convert response to factor
train[,y] <- as.factor(train[,y])
test[,y] <- as.factor(test[,y])

# Number of CV folds (to generate level-one data for stacking)
nfolds <- 5

# Train & Cross-validate a (shallow) XGB-GBM
my_xgb1 <- h2o.automl(x = x,
                       y = y,
                       training_frame = train,
                       distribution = "multinomial",
                       ntrees = 50,
                       max_depth = 3,
                       min_rows = 2,
                       learn_rate = 0.2,
                       nfolds = nfolds,
                       fold_assignment = "Modulo",
                       keep_cross_validation_predictions = TRUE,
                       seed = 1)
summary(my_xgb1)
h2o.confusionMatrix(my_xgb1, valid=TRUE)

























# Train an H2O GBM model
model <- h2o.gbm(x = x,
                 y = y,
                 training_frame = train,
                 validation_frame = test, 
                 distribution = "multinomial",
                 ntrees = 100,
                 learn_rate = 0.3,
                 sample_rate = 1.0,
                 max_depth = 5,
                 col_sample_rate_per_tree = 0.5,
                 seed = 1)
# Get model performance on a test set
perf <- h2o.performance(model, test)
print(perf)
# To retreive individual metrics
h2o.auc(perf)

summary(model)

# Print confusion matrix
h2o.confusionMatrix(perf)
# Plot scoring history over time
plot(model)
# Retreive feature importance
vi <- h2o.varimp(model)
vi[1:10,]
# Plot feature importance
barplot(vi$scaled_importance,
        names.arg = vi$variable,
        space = 1,
        las = 2,
        main = "Variable Importance: H2O GBM")
