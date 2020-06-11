library(tidyverse)
library(lubridate)

transport <- read_csv('transport.csv') %>%
  mutate(Date = dmy(Date)) %>%
  gather('Type', 'Fraction_normal', Cars:Cycling)

transport %>%
  ggplot() +
  geom_line(aes(Date, Fraction_normal)) +
  facet_wrap(~Type, scales='free_y') +
  xlab('Date') + ylab('Fraction of Usual') +
  theme_classic() + 
  theme(strip.background = element_rect(color="black", fill="azure2", size=0.0, linetype="solid"))

transport %>%
  ggplot() +
  geom_line(aes(Date, Fraction_normal, group=Type, colour=Type)) +
  xlab('Date') + ylab('Fraction of Usual') +
  theme_classic()

transport %>%
  filter(Type != 'Cycling') %>%
  ggplot() +
  geom_line(aes(Date, Fraction_normal, group=Type, colour=Type)) +
  xlab('Date') + ylab('Fraction of Usual') +
  theme_classic()
