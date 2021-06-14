weather<-readRDS("C:/Users/amith/OneDrive/MTech/Sem1/DSC513_IntroductionToAIAndDataScience/LAB_Dataset/weather.rds")
bmi<-read.csv("C:/Users/amith/OneDrive/MTech/Sem1/DSC513_IntroductionToAIAndDataScience/LAB_Dataset/BMI.csv")
sales<- read.csv("C:/Users/amith/OneDrive/MTech/Sem1/DSC513_IntroductionToAIAndDataScience/LAB_Dataset/sales.csv",stringsAsFactors=FALSE)
flying_etiquette<-read.csv("C:/Users/amith/OneDrive/MTech/Sem1/DSC513_IntroductionToAIAndDataScience/LAB_Dataset/flying_etiquette.csv",na.strings=c(""),stringsAsFactors=TRUE) 
#MiniProject
raw.data.confirmed <- read.csv('C:/Users/amith/OneDrive/MTech/Sem1/DSC513_IntroductionToAIAndDataScience/LAB_Dataset/COVID_Dataset/time_series_covid19_confirmed_global.csv')
raw.data.deaths <- read.csv('C:/Users/amith/OneDrive/MTech/Sem1/DSC513_IntroductionToAIAndDataScience/LAB_Dataset/COVID_Dataset/time_series_covid19_deaths_global.csv')
raw.data.recovered <- read.csv('C:/Users/amith/OneDrive/MTech/Sem1/DSC513_IntroductionToAIAndDataScience/LAB_Dataset/COVID_Dataset/time_series_covid19_recovered_global.csv')