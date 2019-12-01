#Step-2
## Remove columns with 100% NA
library(dplyr)
not_all_na <- function(x) any(!is.null(x))
final_data = final_data %>% select_if(not_all_na)



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
sec9_data_clean = sec9_data[, -which(colMeans(is.na(sec9_data)) > 0.7)]
sec10_data_clean = sec10_data[, -which(colMeans(is.na(sec10_data)) > 0.7)]
sec11_data_clean = sec11_data[, -which(colMeans(is.na(sec11_data)) > 0.7)]

#creating grp1 selecting same variables
stock_data_grp3 = rbind(sec1_data_clean,sec2_data_clean,sec3_data_clean,sec5_data_clean,
                                 sec6_data_clean,sec7_data_clean,sec8_data_clean,sec10_data_clean,
                                 sec11_data_clean)

#Creating grp2
stock_data_grp2 = sec4_data_clean

#Creating grp3
stock_data_grp1 = sec9_data_clean

#write.csv(stock_data_grp1, "stock_clean_data.csv", row.names = F)
