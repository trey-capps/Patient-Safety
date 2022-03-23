library(tidyverse)
g6 = read.csv("./dexcomG6.csv")
g5 = read.csv("./dexcomG5.csv")
g4 = read.csv("./dexcomG4.csv")

g4$DATE_RECEIVED =substr(g4$DATE_RECEIVED, 1,7)
g5$DATE_RECEIVED =substr(g5$DATE_RECEIVED, 1,7)
g6$DATE_RECEIVED =substr(g6$DATE_RECEIVED, 1,7)

g4$DATE_RECEIVED = as.Date(paste0(g4$DATE_RECEIVED,"-01"))
g5$DATE_RECEIVED = as.Date(paste0(g5$DATE_RECEIVED,"-01"))
g6$DATE_RECEIVED = as.Date(paste0(g6$DATE_RECEIVED,"-01"))
#area graphs
total = count(g4, DATE_RECEIVED)
Type="G4"
g4_data = data.frame(total,Type)

total = count(g5, DATE_RECEIVED)
Type="G5"
g5_data = data.frame(total,Type)

total = count(g6, DATE_RECEIVED)
Type="G6"
g6_data = data.frame(total,Type)

devices = rbind(g6_data,g5_data,g4_data)
devices <- devices[-c(2,35,36,37,92,93,94,1,38),]

#line plot
p=ggplot(devices, aes(x=DATE_RECEIVED, y=n, color = Type))
p+geom_line()+scale_x_date(date_labels = "%m/%y",date_breaks="2 months")+labs(x="Month Reported",y="Number of Reports", title = "Model Device Reports by Month")+theme(axis.text.x = element_text(angle=90))

#individual plots
ggplot(g4, aes(x=DATE_RECEIVED))+geom_area(stat="bin", fill = "blue")+scale_x_date(date_labels = "%m/%y",date_breaks="2 months")+labs(x="Month Reported",y="Number of Reports", title = "G4 Model Device Reports by Month")+theme(axis.text.x = element_text(angle=90))
ggplot(g5, aes(x=DATE_RECEIVED))+geom_area(stat="bin", fill = "green")+scale_x_date(date_labels = "%m/%y",date_breaks="2 months")+labs(x="Month Reported",y="Number of Reports", title = "G5 Model Device Reports by Month")+theme(axis.text.x = element_text(angle=90))
ggplot(g6, aes(x=DATE_RECEIVED))+geom_area(stat="bin", fill = "orange")+scale_x_date(date_labels = "%m/%y",date_breaks="2 months")+labs(x="Month Reported",y="Number of Reports", title = "G6 Model Device Reports by Month")+theme(axis.text.x = element_text(angle=90))

#stacked area graph
p=ggplot(devices, aes(x=DATE_RECEIVED, y=n, fill = Type))
p+geom_area()+labs(x="Count",y="Number of Reports", title="Stacked Area Graph of Model Device Reports")+scale_x_date(date_labels = "%m/%y",date_breaks="2 months")+theme(axis.text.x = element_text(angle=90))

#proportional graph
p=ggplot(devices, aes(x=DATE_RECEIVED, y=n, fill = Type))
p+geom_area(position="fill")+labs(x="Count",y="Number of Reports", title="Proportional Area Graph of Model Device Reports")+scale_x_date(date_labels = "%m/%y",date_breaks="2 months")+theme(axis.text.x = element_text(angle=90))
