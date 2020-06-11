library(tidyverse)
library(lubridate)

cases <- read_csv('cases_england.csv') %>%
  mutate(Date = dmy(Date))

multiplier = round(max(cases$Total_cases)/max(cases$New_cases))

cases %>% 
  ggplot() +
  geom_col(aes(Date, New_cases), width=0.5) +
  geom_line(aes(Date, Total_cases/multiplier), size=1, colour="deeppink2") +
  scale_y_continuous("New Cases", sec.axis = sec_axis(trans=~.*multiplier, name = "Total Cases"))

deaths <- read_csv('deaths.csv') %>%
  mutate(Date = dmy(Date))

multiplier = round(max(deaths$Total_deaths)/max(deaths$New_deaths))

deaths %>% 
  ggplot() +
  geom_col(aes(Date, New_deaths), width=0.5) +
  geom_line(aes(Date, Total_deaths/multiplier), size=1, colour="deeppink2") +
  scale_y_continuous("New Deaths", sec.axis = sec_axis(trans=~.*multiplier, name = "Total Deaths"))
