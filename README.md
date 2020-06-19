![RAWR](presentation/coronasaurus_logo.png)

This repository is coronasaurus's entry to NERC's [COVID-19 Hackathon 2: Recovery](https://digitalenvironment.org/home/covid-19-digital-sprint-hackathons/covid-19-hackathon-2-recovery/).

# Executive Summary

## Introduction
The unprecedented global response to the COVID-19 pandemic has resulted in huge population behavioural changes; from the cessation of travel to a transition to remote working. We don't often see changes of this magnitude, which offers researchers the unique opportunity to evaluate the impact of lockdown measures.

One particular area of interest is the impact on greenhouse gas emissions. As a signatory of the Paris Agreement the UK has a responsibility to limit the global average temperature rise to below 2&deg;C, but this is an ambitious task! Can we use data from this event to evaluate the sort of changes that might need to be made to meet these climate goals?

## The brief
[![alt text](https://i2.wp.com/digitalenvironment.org/wp-content/uploads/2020/05/covid-19_banner-800.png?w=800&ssl=1)](https://digitalenvironment.org/home/covid-19-digital-sprint-hackathons/)

This is an entry for [COVID-19 Hackathon 2: Recovery](https://digitalenvironment.org/home/covid-19-digital-sprint-hackathons/covid-19-hackathon-2-recovery/), run by the Natural Environment Research Council on behalf of UKRI. The brief is:

> - What are the positive and negative aspects of lockdown and recovery measures on meeting Paris and net zero targets?
> - Using multivariate signals to highlight these impacts and their inter-relationships to inform decision making.
>
> Multivariate signals and their interrelationships can be used to highlight the path to recovery. The pandemic is essentially a large unplanned experiment, allowing us to consider the ex-ante/mid-post/ex-post aspects of the effectiveness of the lockdown measures. It further allows us to study the positive and negative aspects of lockdown behaviours and to differentiate between the two. It can also help us to better understand the challenges associated with reaching the 8% target of the Paris Accord and reaching net zero (lockdown restrictions have currently delivered both a 5% reduction in emissions, and a 14% reduction in GDP). Solutions addressing this theme can draw from a variety of data sources including EO, social media and other potential sources.

### Our Approach

Team Coronasaurus examined the effects of the lockdown, seen through publicly available data (UK government, NERc, etc), to examine the effects of the UK populations changes in lifestyle, living arrangements, social interaction and work patterns both going into and out of lockdown could be "read across" towards long term carbon dioxide reduction and climate change mitigation. The "read across" was examined to answer the question "What climate change effects could be achieved if the UK's working population made changes to their working hours and working location ?". 

In short, Team Coronasaurus has been examining if a 4 day working week (with potentially longer days and including 2 days home working) would help reduce UK CO2 and help mitigate climate change ?   

### Presentation

### Interactive notebook
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/aricooperdavis/coronasaurus_NERCHackathonTwo_Multivariate/master?urlpath=%2Ftree%2Fcoronasaurus.ipynb)

You can "play along" online with our analysis using our interactive binder notebook - just click the link above and it'll be served for you. Alternatively, you can download the notebook and run it locally using `jupyter`.

### Team Coronasaurus Contributors

Ari Cooper-Davies - https://www.cooper-davis.net/
James Rand - https://researchportal.bath.ac.uk/en/persons/james-rand


### Folders, Files and Directories

<b>emissions</b>
> - emissions/ - CO2 emmissions data over lockdown period
> - emissions/Figures_CO2.ipynb  - notebook analysing atmospheric CO2 during Covid 19 pandemic
> - emissions/...csv - atmospheric CO2 data from:

>Quere et al (2020) https://www.nature.com/articles/s41558-020-0797-x



<b>covid</b>
> - covid/ - Rates of Infection and Death form Covid 19 in the UK.
> - covid/Cases and Deaths.ipynb - notbook analysising rates of Infection and Death form Covid 19 in the UK.
> - covid/...csv - Covid 19 data from:

>https://www.gov.uk/government/publications/covid-19-track-coronavirus-cases


<b>Fuel</b> 
> - fuel/ - Examining the retail price Petrol and Diesel fuel and the associated fuel duty during the Covid 19 pandemic (fuel not used in analysis).



<b>Grid</b>
> - grid/ Gas and Electrical Energy Consumption (domestic and commercial), Forecasting and Generation
> - grid/octopus - all data downloaded from Octopus energy supply company
> - grid/Electricity and Gas.ipynb - notebook detailing consumption of gas and electricity during Covid 19 pandemic
> - grid/Grid Demand.ipynb - notebook detailing gas and electricity demand from the national grid during Covid 19 pandemic 
> - grid/...p/py/png - supporting graphics and tools
> - grid/...csv - electrical and gas data and taken from:

>https://demandforecast.nationalgrid.com/efs_demand_forecast/faces/DataExplorer

>https://tech.octopus.energy/data-discourse/2020-social-distancing/index.html

>https://www.ofgem.gov.uk/gas/retail-market/monitoring-data-and-statistics/typical-domestic-consumption-values



<b>Presentation</b> 	
> - presentation/ - Interactive Team Coronasaurus Presentation
> - presentation/...py/csv/png/html supporting files. Data from all other folders.



<b>Society</b>
> - society/ - data, code and output files examining society issues during Covid 19 pandemic.
> - society/...ipynb/py - output files graphing and analysing social trends looking at inpact of lockdown on the UK population
> - society/...csv - social data taken from:

>https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork 

>https://data.london.gov.uk/dataset/london-community-response-survey 

>https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthandwellbeing/bulletins/coronavirusandthesocialimpactsongreatbritain/12june2020



<b>Timeline</b>
> - timeline/ - data, code and output files showing important events during the Covid 19 pandemic.
> - timeline/...ipynb/py - timeline generators
> - timeline/...csv - timeline data taken from:

>https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_the_United_Kingdom

>https://appeasement.org/



<b>Transport</b>
> - transport/ - includes data sets, codes and output files and figures related to the effect of lockdown on traffic volume.
> - transport/Traffic.py - includes class Traffic, which allow to import data and analyse them (see notebook).
> - Transport/Figures - includes output figures produced by Traffic class methods
> - Transport/Model_diagnostics - includes output graphs allowing to diagnose the interrupted linear models implemented in Traffic class
> - Transport/Summary - includes csv files with summary of the interrupted linear models implemented in Traffic class (summary consist the goodness of fit and credibility intervals for all model parameters)
> - Transport/..UK_transport.csv - includes traffic volume data for different modes of transport from: 

>https://www.gov.uk/government/statistics/transport-use-during-the-coronavirus-covid-19-pandemic.

> - Transport/UK_weather.csv - includes daily weather data from:

>https://www.accuweather.com/en/gb/london/ec4a-2/january-weather/328328 (daily data)

>https://www.statista.com/statistics/322658/monthly-average-daily-temperatures-in-the-united-kingdom-uk/ (monthly averages)
