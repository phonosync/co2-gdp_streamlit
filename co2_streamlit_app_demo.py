import streamlit as st
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt


@st.cache_data
def get_data():
    url='https://drive.switch.ch/index.php/s/BrEq5fWfSW5sUEq/download' #'https://drive.switch.ch/index.php/s/cxW0xrmQXdGL1VJ/download'
    return pd.read_csv(url, sep=';')

@st.cache_data
def get_regions():
    url='https://drive.switch.ch/index.php/s/hUkzz67kE1YkLE9/download' #'https://drive.switch.ch/index.php/s/cxW0xrmQXdGL1VJ/download'
    return pd.read_csv(url, sep=';')

df_regions = get_regions()
df_regions = df_regions[['Code', 'World Region according to the World Bank']]
df_regions.columns = ['iso_code', 'region']

df = get_data()

df['gdp_per_capita'] = df['gdp']/df['population']

df = df[['country', 'iso_code', 'year', 'population', 'co2', 'gdp', 'co2_per_capita', 'gdp_per_capita']]

df = pd.merge(df, df_regions, left_on='iso_code', right_on='iso_code', how='left')

df = df[~df['region'].isna()]

st.title(body='CO2-Emissions and GDP')
st.markdown('Exploring the CO2 emission dataset from [Our World in Data](https://ourworldindata.org/grapher/co2-emissions-vs-gdp). [Data repository](https://github.com/owid/co2-data/tree/master)')

st.subheader('Dataset overview')
st.markdown('The following table displays a random sample from the dataset:')
st.dataframe(data=df.sample(10, random_state=23), use_container_width=True, hide_index=True,
             column_config={
                'country': st.column_config.TextColumn(
                     'Country',
                    help="Name of the country",
                ),
                'year': st.column_config.NumberColumn(
                    help="The price of the product in USD",
                    min_value=0,
                    max_value=3000,
                    step=1,
                    format="%d"
                )
             }
            )


st.header('CO2 Emissions and GDP in one year')

year_selected = 1964
year_selected = st.slider('Select the year', df.year.min(), df.year.max(), 1964)
df_selected = df[df['year']== year_selected]

st.subheader('CO2 emissions vs. GDP in {}'.format(year_selected))

fig, ax = plt.subplots()
for loc in ['top', 'right']:
    ax.spines[loc].set_visible(False)
ax.tick_params(axis='x', labelsize=14)
ax.tick_params(axis='y', labelsize=14)
ax.set_xlabel('GDP per capita (international-$ at 2011 prices)', fontsize=14)
ax.set_ylabel('CO2 emissions per capita (t)', fontsize=14)

# Convert the y-axis to a logarithmic scale
ax.set_yscale('log')
ax.set_xscale('log')

# Format the x-tick labels with a thousands separator
ax.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x/1000)))


# Create a scatter plot for each unique category in the 'region' column
for region in df_selected['region'].unique():
    ax.scatter(x='gdp_per_capita', y='co2_per_capita', data=df_selected[df_selected['region'] == region], label=region)

# Add a legend
ax.legend()

st.pyplot(fig)


left_column, right_column = st.columns(2)
with left_column:
    st.subheader('CO2 emissions per region')
    st.markdown('The following bar chart displays CO2 emissions in {} aggregated by region'.format(year_selected))

    co2_per_region = df_selected.groupby('region')['co2_per_capita'].sum()
    co2_per_region.sort_values(inplace=True, ascending=True)

    fig, ax = plt.subplots()
    ax.spines[:].set_visible(False)
    ax.spines['top'].set_visible(True)
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    ax.set_xlabel('CO2 emissions per capita (t)', fontsize=14)  

    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis='y', labelsize=14, length=0)

    ax.barh(co2_per_region.index, co2_per_region.values)

    st.pyplot(fig)

with right_column:
    st.subheader('GDP per region')
    st.markdown('The following bar chart displays the Gross Domestic Product (GDP) in {} aggregated by region'.format(year_selected))

    gdp_per_region = df_selected.groupby('region')['gdp_per_capita'].sum()
    gdp_per_region.sort_values(inplace=True, ascending=True)

    fig, ax = plt.subplots()
    ax.spines[:].set_visible(False)
    ax.spines['top'].set_visible(True)
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    ax.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda x, pos: '{:,.0f}k'.format(x/1000)))
    ax.set_xlabel('GDP per capita (international-$ at 2011 prices)', fontsize=14)

    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis='y', labelsize=14, length=0)

    ax.barh(gdp_per_region.index, gdp_per_region.values)

    st.pyplot(fig)

