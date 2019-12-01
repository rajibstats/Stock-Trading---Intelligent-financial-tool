library("RODBC")

con = odbcDriverConnect(
  'driver = {SQL Server};
  Server = xxxxxx;
  Database = xxxxx;
  User Id= xxxxx;
  Password= xxxxx;')


library(odbc)
con <- dbConnect(odbc(),
                 Driver = "{ODBC Driver 13 for SQL Server}",
                 Server = "52.168.37.160",
                 Database = "IntroActML",
                 UID = "sa",
                 PWD = "bd@m1n#Intr0@c")
                 #Port = 1433)
myConn <-odbcDriverConnect("Driver={ODBC Driver 13 for SQL Server};Dbq=IntroActML;Uid=sa;Pwd=bd@m1n#Intr0@c;")


library(RODBC)
dbhandle <- odbcDriverConnect('driver={ODBC Driver 13 for SQL Server};server=52.168.37.160;UID =sa,
                 PWD =bd@m1n#Intr0@c;
                              database=IntroActML;trusted_connection=true')


res <- sqlQuery(dbhandle, 'select * from information_schema.tables')



library(RODBC)

driver.name <- "{ODBC Driver 13 for SQL Server}"
db.name <- "IntroActML"
port <-""
server.name <-"52.168.37.160"
user.name <- "sa"
pwd <- "bd@m1n#Intr0@c"
# Use a full connection string to connect to a SAMPLE database
con.text <- paste("DRIVER=",driver.name,
                  ";Database=",db.name,
                  ";Server=",server.name,
                  ";Port=",port,
                  ";PROTOCOL=TCPIP",
                  ";UID=", user.name,
                  ";PWD=",pwd,sep="")

con1 <- odbcDriverConnect(con.text)

dbconnection <- odbcDriverConnect("Driver=ODBC Driver 13 for SQL Server;
                Server=52.168.37.160; Database=IntroActML; 
                Uid=sa; Pwd=bd@m1n#Intr0@c; trusted_connection=yes")
