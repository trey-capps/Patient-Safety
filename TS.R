# time series analysis

# packages
library(tidyverse)
library(FitAR)
library(forecast)
library(lubridate)
library(tseries)
library(xts)

# ARIMA(autoregressive integrated moving average)

############# G4

# Convert into time series data
data_g4_og <- read_csv("./data/export/dexcomG4.csv")
data_g4 <- data_g4_og
data_g4$DATE_RECEIVED <- substr(data_g4$DATE_RECEIVED, 1,7)
data_g4$DATE_RECEIVED <- as.Date(paste0(data_g4$DATE_RECEIVED,"-01"))
data_g4_month <- count(data_g4, DATE_RECEIVED)
data_g4_month <- data_g4_month[-c(1:3),]
tsData4 = ts(data_g4_month$n, frequency=12)

# Tests for stationarity
adf.test(tsData4) ## p-value large, fail to reject H0, TS is not stationary, d !=0
kpss.test(tsData4) ## p-value small, reject H0, TS is not trend stationary

# STL decomposition (Seasonal and Trend decomposition using Loess)
decomp <- stl(tsData4, s.window = "periodic")
plot(decomp, main = "G4 Seasonal and Trend decomposition using Loess")


################ G5

data_g5_og <- read_csv("./data/export/dexcomG5.csv")
data_g5 <- data_g5_og
data_g5$DATE_RECEIVED <- substr(data_g5$DATE_RECEIVED, 1,7)
data_g5$DATE_RECEIVED <- as.Date(paste0(data_g5$DATE_RECEIVED,"-01"))
data_g5_month <- count(data_g5, DATE_RECEIVED)
data_g5_month <- data_g5_month[-c(1:4),]
tsData5 = ts(data_g5_month$n, frequency=12)

# Tests for stationarity
adf.test(tsData5) ## p-value large, fail to reject H0, TS is not stationary, d !=0
kpss.test(tsData5) ## p-value small, reject H0, TS is not trend stationary

# STL decomposition (Seasonal and Trend decomposition using Loess)
decomp <- stl(tsData5, s.window = "periodic")
plot(decomp, main = "G5 Seasonal and Trend decomposition using Loess")


################# G6

data_g6_og <- read_csv("./data/export/dexcomG6.csv")
data_g6 <- data_g6_og
data_g6$DATE_RECEIVED <- substr(data_g6$DATE_RECEIVED, 1,7)
data_g6$DATE_RECEIVED <- as.Date(paste0(data_g6$DATE_RECEIVED,"-01"))
data_g6_month <- count(data_g6, DATE_RECEIVED)
data_g6_month <- data_g6_month[-c(1:2),]
tsData6 = ts(data_g6_month$n, frequency=12)

# Tests for stationarity
adf.test(tsData6) ## p-value large, fail to reject H0, TS is not stationary, d !=0
#kpss.test(tsData6) ## p-value small, reject H0, TS is not trend stationary

# STL decomposition (Seasonal and Trend decomposition using Loess)
decomp <- stl(tsData6, s.window = "periodic")
plot(decomp, main = "G6 Seasonal and Trend decomposition using Loess")

# seasonal differencing
seas_diff <- diff(tsData6, lag = frequency(tsData6), differences = 1)
adf.test(seas_diff)
kpss.test(seas_diff)
plot(seas_diff)

seas_diff2 <- diff(seas_diff)
adf.test(seas_diff2)
kpss.test(seas_diff2)
plot(seas_diff2)

seas_diff3 <- diff(seas_diff2)
adf.test(seas_diff3)
kpss.test(seas_diff3)
plot(seas_diff3)
# p-value finally small enough, d = 3

## seasonality: yearly pattern

# Find order of AR term: p
# PACF: partial autocorrelation function

pacf(seas_diff3, lag.max=100)
## p =0

# Find order of MA term: q
# ACF: autocorrelation function

acf(seas_diff3, lag.max=100)
## q = 1

# fit the ARIMA model

fit_arima <- arima(tsData6, order = c(0,1,0),seasonal = list(order = c(0,1,0), period = 12),method="ML")


# forecast with ARIMA model
forecast(fit_arima, 12)
plot(forecast(fit_arima,12, level = c(95)))

# Checking the residuals for fit 
arima_res <- fit_arima$residuals
acf(arima_res)
qqnorm(arima_res)
qqline(arima_res)

# auto arima to find best model

auto_arima <- auto.arima(tsData6, trace = TRUE)
autoplot(forecast(auto_arima, level = c(80,95))) + ylab("Report Count") + xlab("Year")

pred_g6 <- forecast(auto_arima, level = c(80,95))
pred_g6_val <- as.numeric(pred_g6[[4]])
summary(auto_arima)

# Checking the residuals for fit 
arima_res <- auto_arima$residuals
acf(arima_res)
qqnorm(arima_res)
qqline(arima_res)
### Next steps, import data from 2021, and compare (error plot)

data_21_og <- read_csv("./data/export/dexcomG6_21.csv")
data_21 <- data_21_og
data_21$DATE_RECEIVED <- substr(data_21$DATE_RECEIVED, 1,7)
data_21$DATE_RECEIVED <- as.Date(paste0(data_21$DATE_RECEIVED,"-01"))
data_21_month <- count(data_21, DATE_RECEIVED)
data_comp <- cbind(data_21_month, pred_g6_val[1:10])
data_comp <- cbind(data_comp, data_comp[,3]-data_comp[,2])

colnames(data_comp) <- c("Time", "Actual", "Predicted", "Error")

# Make comparison graph
p_comp <- ggplot(data = data_comp, mapping = aes(x= Time)) + 
  geom_line(mapping = aes(y = Actual), col = "firebrick") +
  geom_text(data = data_comp[9,], aes(label = "Actual", x = Time, y = Actual), vjust = -0.5, hjust = 1.5, color = "firebrick") +
  geom_line(mapping = aes(y = Predicted), col = "royalblue", linetype = "twodash") +
  geom_text(data = data_comp[10,], aes(label = "Predicted", x = Time, y = Predicted), vjust = 2, hjust = 2, color = "royalblue") +
  labs(y = "Report Count", title = "Dexcom G6 Device Report Count (Actual vs. Predicted) Jan-Oct 2021")

p_comp

# make prediction error graph
p_err <- ggplot(data = data_comp, mapping = aes(x= Time)) +
  geom_line(mapping = aes(y = Error)) +
  geom_hline(yintercept = 0, col = "royalblue") +
  labs(title = "G6 Prediction Error 2021")
p_err
