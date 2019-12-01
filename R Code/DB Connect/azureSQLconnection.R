#required library
library(RMySQL)
library(DBI)
library(RODBC)

#connection string
con <- dbConnect(odbc::odbc(), 
                 Driver = "{ODBC Driver 13 for SQL Server}",
                 Server = "52.168.37.160",
                 Database = "IntroActML",
                 UID = "sa", 
                 Pwd = "bd@m1n#Intr0@ct",
                 timeout = 30)

tables = dbListTables(con)

dbListFields(con, "Owner_2018Q2_Russel3000_top1000")

# Run an SQL statement by creating first a resultSet object)
rs <- dbSendQuery(con, statement = paste("SELECT * from NonOwner_2018Q3_BroaderRussel"))

#required tables
#"Owner_2018Q2_BroaderRussel3000_top1000"              
#"Owner_2018Q2_Russel3000_top1000"

# we now fetch records from the resultSet into a data.frame
data = dbReadTable(con, "NonOwner_2018Q3_BroaderRussel")
dim(data)

# Save an object to a file
saveRDS(data, file = "D:\\Stock_Prediction\\data\\Non_Owner\\Non_Owner_Data.rds")
#save(data, file = "D:\\Stock_Prediction\\data\\NewR\\NewStockData.RData")
#save.image(file = "D:\\Stock_Prediction\\data\\NewR\\NewStockDataIMG.RData")

#Save and restore one single R object: saveRDS(object, file), my_data <- readRDS(file)
#Save and restore multiple R objects: save(data1, data2, file = "my_data.RData"), load("my_data.RData")
#Save and restore your entire workspace: save.image(file = "my_work_space.RData"), load("my_work_space.RData")
  