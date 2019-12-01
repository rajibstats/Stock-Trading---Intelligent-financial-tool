# Stock-Trading---Intelligent-financial-tool
an intelligent Financial Prediction Model for extracting investor behavior in the USA stock market, in order to analyze institutional investors’ interests.

Who is the Client?

The Client is an artificial intelligence (AI) platform that matches corporate executives with the institutional investors that are most likely to buy, or sell, their stock in the next 90 days -- while simultaneously offering all users data discovery technologies to efficiently prepare for all types of corporate-investor access events.
The Client was seeking an intelligent Financial Prediction Model for extracting investor behavior in the USA stock market, in order to analyze institutional investors’ interests.

What services did Data-Core provide?

The key objective was to develop an intelligent Financial Prediction Model for extracting investor behavior in the USA stock market, so as to increase the availability of decision support data and hence increase investor satisfaction. The model was built based on quarterly data and deals with stock portfolio analysis of the institutional investors.

Key Objectives:

•	Individually evaluate the relationship with an investor and a stock for Owner & Non-Owner models in the Russell 3000
•	Use Azure data mining model and statistical technique (Algorithm)
•	Handle “imbalance classification of data using Python-scripts” in MS Azure ML Studio
The Challenge was to identify characteristics of investors that are most predictive in signaling that they are likely incremental buyers, as well as those characteristics that suggest an investor is at risk of reducing their position.
•	Breadth: Be able to get 30 recommendations for each company in the Russell 3000 (10 new buys / 10 incremental buys / 10 incremental sells)
•	Accuracy: Move accuracy from current ~ 54% to > 65%
•	Automation of scripts using Python to make report

In Summary...

Provided the Client interactive & integrated dashboards to help investors and corporates more efficiently prepare for meetings by quickly identifying themes, trends and outlier data that is most likely to warrant discussion. This was accomplished with easy to use analytics to quickly compare fundamental, valuation and sentiment factors relative to peers. 


1. Collect Data & Identity Target:

o	Pull MySQL Data tables --> extracted to IA Server after every 45 days.
o	IA Server. Run ETL Scheduler weekly (Intro-Act Job)
o	Data Cleanup, Transformation & data Preparation of Training Set & Test Set for ML Data Input
o	Prepared Data Sets (Training Set & Test Set) in IA Server
o	Pull Data from IA Server to IA Azure ML Studio (Training Set & Test Set)
o	Identify response variable “Action Taken”. For Owner case target variable was Multiclass (Increase, Decrease, Hold) and for Non-Owner case target variable was Binary (NA and Buy).

2. Univariate Analysis

o	Check missing for all columns and Initially removed those variables which has > 70 % missing
o	The variables still have missing, are replace by median for categorical variables and by average for numerical variables
o	 There was no outlier in the data set

3. Sampling

o	Development and Validation sample
 Use last 12 QTR data for model development (train data)
 last QTR be used for validating the model (test data)
•	Based on final model predict for upcoming QTR


4. Variable transformation

Minmax normalization is a normalization strategy which linearly transforms x to y= (x-min)/(max-min), where min and max are the minimum and maximum values in X, where X is the set of observed values of x. This means, the minimum value in X is mapped to 0 and the maximum value in X is mapped to 1.


5. Segmentation

Why Segmentation?
 It is necessary to segregate the portfolio into several groups that behave similarly but are significantly different as a group from other groups
 Segmentation significantly improves the accuracy of the model
 Guide organization to manage portfolio in more accurate level
 Model will be built separately for each segment

For Owner Model we haven’t segment our portfolio but for Non-Owner model we segment out portfolio sector wise. As we had 11 sectors, so we built 11 models. 

6. Feature Importance

PCA are improved data visualization, and optimization of resource use by the learning algorithm. The Principal Component Analysis module in Azure Machine Learning Studio takes a set of feature columns in the provided dataset and creates a projection of the feature space that has lower dimensionality.

7. Modeling

Supervised learning is where you have input variables (x) and an output variable (Y) and you use an algorithm to learn the mapping function from the input to the output.
In Our project, as we know our target variable, so this was completely a Supervised ML Technique. 
a)	For Owner Model we have used following algorithms:
•	Multiclass Decision Forest
•	Multiclass Decision Jungle
•	Multiclass Logistic Regression
•	Multiclass Neural Network

b)	For Non-Owner Model we have used following algorithms:
•	Two-Class Decision Forest
•	Two-Class Decision Jungle
•	Two-Class Logistic Regression
•	Two-Class Neural Network
•	Two-Class Boosted Decision
•	Two-Class Support Vector Machine

8. Final Model and Model Validation:

As It was a classification problem, we finalized our model based on the Accuracy score on validation sample. Also check validation statistics like Precision, Recall and F1 Score. 

Precision and recall are two extremely important model evaluation metrics. While precision refers to the percentage of your results which are relevant, recall refers to the percentage of total relevant results correctly classified by your algorithm.
 
 
•	After achieving > 60% accuracy, we save the output result in to Azure blob storage and Local machine as CSV file.  
•	Read the CSV file from blob storage and store the data in SQL server.
•	Show the data in the dashboard from SQL server

ML Results converted to requested Report formats:

Detailed Steps using Python Script

1. Read raw data from csv (local) file generated from Azure ML.
2. Import MasterSheet
3. Sync Headers with MasterSheet and CSV
4. Create a new DF with required format 
5. Export two xlsx files for company analysis and fund analysis

Company Analysis and Fund Analysis for Owner and Non-Owner Model
Step 1  - Divide the DF to 3 different files (Increment, Decrement, Hold for Owner model ) & (NA , Buy for Non-Owner model)
Step 2 - Add condition where Action taken = Scored labels (True positive)
Step 3 - Add condition where Action taken!=Scored labels(False positive)
Step 4 - Original column will be the total action taken value
Step5 - Prediction column will be the total scored labels value
Step 6 - If Scored labels != Action Taken (False Negative)








