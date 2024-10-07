import streamlit as st

st.header("Data")
st.write("The data used to build the graph and maps come from NASA Datasets. Below is a little bit more about them")
st.divider()


st.header("GOSAT-based Top-down Total and Natural Methane Emissions")
st.subheader("About it")
st.write("""
         Countries have been requested to provide records in regard to the emission of greenhouse gases to guide their efforts in the reduction of such emissions under the global stocktake. 
         The NASA Carbon Monitoring System Flux team has used satellite data from Japan's Greenhouse gases Observing SATellite to produce modeled total CH₄ emissions with associated uncertainties at 1-degree by 1-degree resolution for 2019. 
         This dataset includes GOSAT data in a model to predict total emissions, including from wetlands-the largest natural source of methane-and from human-related activities that include fossil fuel extraction, transport, agriculture, waste, and fire. 
         An advanced mathematical methodology combined with a global chemistry transport model to calculate annual CH₄ emissions along with their uncertainties. It is expressed in teragrams of CH₄ per year (Tg/yr). 
         Note that only the total emissions and those derived from wetlands will be carried in the US GHG Center while the source dataset contain the emissions for all other anthropogenic sources.
         """)
st.subheader("Accuracy")
st.write("""The accuracy of the data depends on the understanding of the uncertainties of model emission. The uncertainties from the bottom up are checked for consistency between the various studies and emission models, as well as against remote-sensing data and expert opinions, particularly for estimates where the difficulty is felt. Recent studies indicate that aquatic emissions, together with those from fossil fuel sources, may be higher than assumed and, therefore, either the current methane budgets have incorrect allocations or the atmospheric methane removal mechanisms are not well understood. It is also important to note that top-down uncertainties can be large models' errors in remote sensing that relate the measurements to concentrations and also model transport errors that add uncertainty during the conversion of concentrations to fluxes. The flux inversion for this dataset jointly estimates hydroxyl radical (OH) and CH₄ emissions to minimize variability impacts on methane emissions. A latitudinal correction mitigates stratospheric chemistry and transport errors; other systematic errors were not characterized but are assumed minor. The Bayesian approach allows explicit quantification of smoothing error as one of the dominant contributors to emission uncertainty with limited risk from additional biases in the projection of fluxes back to emissions. Note that the uncertainties apply only at a resolution of the 1-degree grid cells.
""")
st.link_button("Visit Website", "https://earth.gov/ghgcenter/data-catalog/gosat-based-ch4budget-yeargrid-v1")



st.divider()

st.header("Atmospheric Methane Concentrations Since 1984")
st.subheader("About it")

st.subheader("Accuracy")
st.write("""Uncertainties in global monthly means are estimated using two methods. The first is a bootstrap (resampling) method that varies the sites in our NOAA ESRL cooperative global air sampling network, creating pseudo-networks with repeated and excluded sites. The second method is a Monte Carlo approach that randomly adjusts the data to reflect measurement uncertainty. Both methods generate 100 globally averaged time series, from which standard deviations of the monthly means are calculated. The uncertainties from the network and analytical methods are combined using quadrature. A default value of -9.9 indicates that uncertainty has not been calculated for that month.
         """)
st.link_button("Visit Website", "https://climate.nasa.gov/vital-signs/methane/?intent=121")
