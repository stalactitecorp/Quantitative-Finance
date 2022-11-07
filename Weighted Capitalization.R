###Coded by: Yorgos Protonotarios###


# Web Scraping: List of S&P 500 stocks
install.packages("reshape2")
install.packages("plyr")
library(plyr)
library(reshape2)
library(ggplot2)
library(rvest)
library(magrittr) # needs to be run every time you start R and want to use %>%
library(quantmod)
library(comprehenr) # used for list comprehension
# get the URL for the wikipedia page with all SP500 symbols
url <- "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
# use that URL to scrape the SP500 table using rvest
tickers <- url %>%
  # read the HTML from the webpage
  read_html() %>%
  # one way to get table
  #html_nodes(xpath='//*[@id="mw-content-text"]/div/table[1]') %>%
  # easier way to get table
  html_nodes(xpath = '//*[@id="constituents"]') %>% 
  html_table()
#create a vector of tickers
sp500tickers <- tickers[[1]]
sp500tickers$Symbol
sp500tickers = sp500tickers %>% mutate(Symbol = case_when(Symbol == "BRK.B" ~ "BRK-B",
                                                          Symbol == "BF.B" ~ "BF-B",
                                                          TRUE ~ as.character(Symbol)))
?sp500 = sp500tickers$Symbol

giveSymbolsList = function(){
  x <- read.delim("/Users/yorgos/Desktop/stockSymbolsFile.txt", header = TRUE, sep = "\t",)
  #x <- scan("C:\\Users\\yorgos\\Desktop\\stockSymbolsFile.txt", what = list(stockNo = 0, stockName = ""))
  x = x[ , order(colnames(x))]
  return(x)
}
Listy = giveSymbolsList()
print(Listy)
Current_Stocks = to_vec(for(i in 1:length(Listy)) getQuote(colnames(Listy[i]), warnings = FALSE, auto.assign = FALSE)[,2])
Current_Vol = to_vec(for(i in 1:length(Listy)) getQuote(colnames(Listy[i]), warnings = FALSE, auto.assign = FALSE)[,5])
Current_Cap = Current_Stocks*Current_Vol
#Current_Cap_Squared = (Current_Cap)^2
Current_Mu = Current_Cap/sum(Current_Cap)
#Total_Cap = sum(Current_Cap)
Total_Cap_Squared = Current_Mu^2/sum(Current_Mu^2)
M = as.data.frame(Total_Cap_Squared)
Numbers_Capitalization = matrix(0, nrow = 1, ncol = length(Listy))
for (i in 1:length(Listy)){
  Current_Mu = c(Current_Mu, Current_Cap[i]/Total_Cap)
}

for (i in 1:length(Listy)){
  Numbers_Capitalization[1,i] = (Current_Cap_Squared[i])/(sum(Current_Cap_Squared))
}
rownames(M) = colnames(Listy)

