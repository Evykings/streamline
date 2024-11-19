
import streamlit as st
import numpy as np
import pandas as pd


print(openpyxl.__version__)

#define functions 
def style_negative(v, props=''):
    "'' Style negative values in dataframe""" 
    try:
        return props if v < 0 else None 
    except:
        pass
def style_positive(v, props=''):
    "''Style positive values in dataframe""" 
    try:
        return props if v > 0 and v < 100 else None 
    except:
        pass

# Loading the dataset into python
df = pd.read_excel('bedcdataset.xlsx')



# printing all the missing values
print("Missing Data:\n",df.isnull().sum())



# Droping all rows with missing values
df = df.dropna(subset=["tariffclassname", "tariffrates", "readconsumption", "energycharges", "updateddssname"])

# Checking the numbers of missing values again
print("Missing Data:\n",df.isnull().sum())



# Filling all missing values with 0
df = df.fillna(0)

print("Missing Data:\n",df.isnull().sum())


dfc = df.copy()
dfc = dfc.drop_duplicates()
dff = df.copy()

# Summary statistics for numerical features
df.describe()



# Creating a new dataset for the numerical columns
numerical_col= df[['tariffrates','previousreading', 'presentreading', 'readconsumption', 'cap', 'energycharges', 'billedamount', 'previouspayments' ]]

median_agg = numerical_col.median()

# printing the first 10 rows of the dataset
numerical_col.head(10)

mean_diff_agg = (numerical_col - median_agg).div(median_agg)

# Get the numerical column indices from the original DataFrame 'df'
numerical_col_indices = [df.columns.get_loc(col) for col in numerical_col.columns]

# Use the numerical indices to select and modify the columns in 'dfc'
dfc.iloc[:, numerical_col_indices] = (dfc.iloc[:, numerical_col_indices] - median_agg).div(median_agg)



add_sidebar = st.sidebar.selectbox("Aggregate or Individual Substation", ("Aggregate Metrics For The Region","Individual Distribution Substation Analysis"))



if add_sidebar == 'Aggregate Metrics For The Region':
    st.metric('Previous Payment', median_agg['previouspayments'], delta = "{:.2%}".format((median_agg['previouspayments'] - 13999.86)/13999.86))
    st.metric('Billed Amount', median_agg['billedamount'], delta = "{:.2%}".format((median_agg['billedamount'] - 13999.86)/13999.86))
    st.metric('Emergy Charge', median_agg['energycharges'], delta = "{:.2%}".format((median_agg['energycharges'] - 13999.86)/13999.86))
    st.metric('Read Consumption', median_agg['readconsumption'])
    
    df_agg_diff_final = dfc.loc[:,['globalaccountnumber','energycharges','billedamount','previouspayments','updateddssname']]

    # Get the numerical column names from df_agg_diff_final
    numerical_cols = ['globalaccountnumber','energycharges', 'billedamount', 'previouspayments']  

    # Get the numerical column indices from df_agg_diff_final
    numerical_col_indices = [df_agg_diff_final.columns.get_loc(col) for col in numerical_cols if col in df_agg_diff_final.columns]

    # Apply styling
    
    st.dataframe(df_agg_diff_final.iloc[:, numerical_col_indices].style.applymap(style_negative, props='color:red;').applymap(style_positive, props='color:green;'))

if add_sidebar == 'Individual Distribution Substation Analysis':    
    dss = tuple(dff['updateddssname'])
    dssselect = st.selectbox('Select the Distribution Substation (dss) for your Analysis', dss)
    dss_filter = dff[dfc['updateddssname'] == dssselect]
    st.metric('Customers Count', dss_filter['updateddssname'].count())
    st.dataframe(dss_filter)
    
    dss_filter = dss_filter.set_index('globalaccountnumber')
    st.bar_chart(dss_filter['previouspayments'], x_label= 'Customers', y_label= 'Previous Payment')
    
