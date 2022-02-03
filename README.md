# Ironhack Proyect-3

# The blackout: myth or reality?

The purpose of this proyect was to establish a simple prediction about if an electrical blackout could actually be a possibility and therefore when shall it happen.
Two datasets have been used for the analysis: one real-time updated with the global population, and another one with anual energy variation, which is updated regularly, with different subcategories.
The analysis was focused on finding a potential moment where the energy consumption would be higher than the energy production.

### 🗂️ You may download the complete datasets from the 'data' folder. 

## The data sources

(A) The energy dataset was obtained from a variation of the collection of energy key metrics provided by [Our world in data](https://ourworldindata.org/energy). This variation was developed by Hannah Ritchie, Max Roser and Edouard Mathieu, as part of their own [project](https://github.com/owid/energy-data), which is as well based on:

  - *Energy consumption (primary energy, energy mix and energy intensity):** this data is sourced from a combination of two sources—the [BP Statistical Review of World Energy](https://www.bp.com/en/global/corporate/energy-economics/statistical-review-of-world-energy.html) and [SHIFT Data Portal](https://www.theshiftdataportal.org/energy).
  - *Electricity consumption (electricity consumption, and electricity mix):** this data is sourced from a combination of two sources—the [BP Statistical Review of World Energy](https://www.bp.com/en/global/corporate/energy-economics/statistical-review-of-world-energy.html) and [EMBER – Global Electricity Dashboard](https://ember.shinyapps.io/GlobalElectricityDashboard/).
  - *Other variables:** this data is collected from a variety of sources (United Nations, World Bank, Gapminder, Maddison Project Database, etc.).

(B) The first population dataset was taken from the website [Wordometers](https://www.worldometers.info/), using an API named 'World population' created by Aldair Sanchez. It was used for establishing a permanently updated point of reference for the population.  
Author: Worldometers.info
Publishing Date: 8 November, 2021
Place of publication: Dover, Delaware, U.S.A.

(C) The second population dataset was extracted from the [UUNN Department of Economic and Social Affairs](https://population.un.org/wpp/Download/Standard/CSV/) website. It was used for obtaining an estimation of the population annual variation.  
United Nations, Department of Economic and Social Affairs, Population Division (2019). World Population Prospects 2019, Online Edition. Rev. 1.

## Resources

- [RapidAPI](https://rapidapi.com/aldair.sr99/api/world-population/): source of the API.
- [Wordometers](https://www.worldometers.info/): source of real-time population info.
- [UUNN Department of Economic and Social Affairs](https://population.un.org/wpp/Download/Standard/CSV/): estimation of interannual population variation.
- The ['api_functions.py'](https://github.com/TheIronhidex/Proyect-3/blob/main/src/api_functions.py) file contains the functions related to managing and downloading info from the different APIs.
- The ['cleaning_functions.py'](https://github.com/TheIronhidex/Proyect-3/blob/main/src/cleaning_functions.py) file contains the functions related to the cleaning operations.
- There are four different notebooks:  
    (1) [API_adquisition](https://github.com/TheIronhidex/Proyect-3/blob/main/notebooks/API_adquisition.ipynb): contains the code for downloading and filtering the information from Wordometers through the API.  
    (2) [Database_csv_managing](https://github.com/TheIronhidex/Proyect-3/blob/main/notebooks/Database_csv_managing.ipynb): includes most of the processes of cleaning and transforming the information.  
    (3) [Dataframe_analysis](https://github.com/TheIronhidex/Proyect-3/blob/main/notebooks/dataframe_analysis.ipynb): has the last operations of optimization. From this stage have been created the graphs in the last notebook.  
    (4) Storytelling: there are the analysis of the hypothesis, the graphs, and the conclusions.  
- There are six different .csv documents, corresponding to different stages:
    (1) 'population-data' - original current total population.  
    (2) 'avg-rate' - interannual population variation.  
    (3) 'pop_avg_rate' - innterannual energy production rate.  
    (4) 'energy_pop_2020' - current total population, updated to the number of countries considered in the energy database.  
    (5) 'energy-var' - interannual energy consumption rate.  
    (6) 'owid-energy-data' - original energy data.  

## Changelog

- On November 8, 2021, was the first release (version 1.0).

## License

All visualizations, data, and code produced by _TheIronhidex_ are completely open access under the [Creative Commons BY license](https://creativecommons.org/licenses/by/4.0/). You have the permission to use, distribute, and reproduce these in any medium, provided the source and authors are credited.
