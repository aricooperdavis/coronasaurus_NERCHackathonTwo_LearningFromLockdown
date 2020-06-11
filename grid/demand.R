library(tidyverse)
library(lubridate)
library(scales)

data <- read_csv('combined.csv') %>%
  mutate(SETTLEMENT_DATE = dmy(SETTLEMENT_DATE),
         DATE = as.Date(format(SETTLEMENT_DATE, format="%m-%d"), format="%m-%d"),
         YEAR = as_factor(year(SETTLEMENT_DATE)),
         ND = na_if(ND, 0))
  
data %>%
  ggplot(aes(SETTLEMENT_DATE, ND)) +
  geom_line() +
  labs(x = "Year", y = "Demand (MW)") +
  ylim(0, NA) + 
  theme_classic()

data %>%
  ggplot(aes(date(DATE), ND)) +
  geom_line(aes(group=YEAR, color=YEAR), alpha=0.7, size=1) +
  labs(x = "Month", y = "Demand (MW)") +
  scale_x_date(labels = date_format("%b")) +
  ylim(0, NA) + 
  theme_classic()

data_daily_average <- data %>%
  group_by(SETTLEMENT_DATE) %>%
  summarise(ND_AVG = mean(ND)) %>%
  mutate(DATE = as.Date(format(SETTLEMENT_DATE, format="%m-%d"), format="%m-%d"),
         YEAR = as_factor(year(SETTLEMENT_DATE)))

data_daily_average %>%
  ggplot(aes(SETTLEMENT_DATE, ND_AVG)) +
  geom_line() +
  geom_smooth(colour="deeppink2", method = "loess") +
  labs(x = "Year", y = "Demand (MW)") +
  ylim(0, NA) + 
  theme_classic()
  
data_daily_average %>%
  ggplot(aes(DATE, ND_AVG)) +
  geom_line(aes(group=YEAR, color=YEAR), alpha=0.7, size=1) +
  labs(x = "Month", y = "Demand (MW)") +
  scale_x_date(labels = date_format("%b")) +
  ylim(0, NA) + 
  theme_classic()
