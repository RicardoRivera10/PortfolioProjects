# Dataset obtained from Kaggle at https://www.kaggle.com/datasets/thedevastator/unlock-profits-with-e-commerce-sales-data


import numpy as np # linear algebra
import pandas as pd # data processing
import matplotlib.pyplot as plt
import seaborn as sns 
import plotly.express as px
import plotly.graph_objects as go
import missingno as msno 
import warnings 
warnings.filterwarnings("ignore")
# import holidays



Amazon_df = pd.read_csv("Python/Ecommerce_Cleaning_Transform/Amazon Sale Report.csv")
# Cloud_Warehouse_df = pd.read_csv("Python/Ecommerce_Cleaning_Transform/Cloud Warehouse Compersion Chart.csv") 
# Expense_df = pd.read_csv("Python/Ecommerce_Cleaning_Transform/Expense IIGF.csv")
# international_sale_report_df = pd.read_csv("Python/Ecommerce_Cleaning_Transform/International sale Report.csv")
# May2022_df = pd.read_csv("Python/Ecommerce_Cleaning_Transform/May-2022.csv")
# PLMarch2021_df = pd.read_csv("Python/Ecommerce_Cleaning_Transform/P  L March 2021.csv")
# Sale_report_df = pd.read_csv("Python/Ecommerce_Cleaning_Transform/Sale Report.csv")



## Starting with Amazon, let's preview the data
## Goals: Overall to increase revenue and improve product performance, section off by category of the products


#################################################
# print(Amazon_df)
Amazon_df["Qty"]
# print(Amazon_df.columns)
# Amazon_df.info()

Amazon_df['Date'] = pd.to_datetime(Amazon_df['Date'])
# daily_sales = Amazon_df.groupby('Date').agg(total_qty=('Qty', 'sum'), total_amount=('Amount', 'sum')).reset_index()
# print(daily_sales)
# plt.figure(figsize=(10, 5))
# sns.lineplot(data=daily_sales, x='Date', y='total_qty', label='Total Quantity Sold', color='blue', linewidth=2)


# plt.title('Sales Trends Over Time')
# plt.xlabel('Date')
# plt.ylabel('Sales')
# plt.xticks(rotation=45)  
# plt.legend()
# plt.grid(True)
plt.show()
######################################

# Let's find the unique values in our Amazon dataframe, this will help us know what we need to filter out before visualizing our data
# print(Amazon_df.nunique().to_frame(name='Count of unique values'))
Amazon_df.apply(pd.unique).to_frame(name='Unique Values')



### DATA CLEANING ###
# print(Amazon_df.isnull().sum())

# Drop unecessary columns
Amazon_df.drop(columns= ['index','Unnamed: 22', 'fulfilled-by', 'ship-country', 'currency', 'Sales Channel '], inplace = True)

# Drop any duplicates we can find
Amazon_df[Amazon_df.duplicated(['Order ID','ASIN'], keep=False)]

print(len(Amazon_df)-len(Amazon_df.drop_duplicates(['Order ID','ASIN'])))
Amazon_df.drop_duplicates(['Order ID','ASIN'],inplace = True,ignore_index=True)


## By looking at the data previously in the unique values, we saw NaN values can be found, I will fill them in the next step

Amazon_df['Courier Status'].fillna('unknown',inplace=True)
Amazon_df['promotion-ids'].fillna('no promotion',inplace=True)
Amazon_df[Amazon_df['Amount'].isnull()]['Status'].value_counts(normalize=True).apply(lambda x: format(x, '.2%'))
Amazon_df['Amount'].fillna(0,inplace=True)
Amazon_df['ship-city'].fillna('unknown', inplace = True)
Amazon_df['ship-state'].fillna('unknown', inplace = True)
Amazon_df['ship-postal-code'].fillna('unknown', inplace = True)

# The following step is just to have a consistent naming pattern for all (undercase), fix any mistakes in the spelling, and eliminate the spaces for certain columns
mapper = {'Order ID':'order_ID', 'Date':'date', 'Status':'ship_status','Fulfilment':'fullfilment',
          'ship-service-level':'service_level', 'Style':'style', 'SKU':'sku', 'Category':'product_category', 
          'Size':'size', 'ASIN':'asin', 'Courier Status':'courier_ship_status', 'Qty':'order_quantity', 
          'Amount':'order_amount_($)', 'ship-city':'city', 'ship-state':'state', 'ship-postal-code':'zip', 
          'promotion-ids':'promotion','B2B':'customer_type'}

Amazon_df.rename(columns=mapper, inplace =True)
amz = Amazon_df
# Referring back to the information, I see we have a key value of "Amount" (renamed to order_amount_($)) that needs to be converted to USD (from INR)
# Grabbed latest exchange rate rounded to neared thousandth from google on 11/27/2024
exchange_rate = 0.012
amz['order_amount_($)'] = amz['order_amount_($)'].apply(lambda x: x * exchange_rate)


# Creating datetime
amz['date'] = pd.to_datetime(amz['date'])
# Filter to only include dates in March
# march_dates = amz['date'][amz['date'].dt.month == 3]

# Get the number of unique days in March
# march_dates.dt.day.nunique()

## dropping March dates from the dataset, THIS CAN BE DONE TO EXCLUDE OUTLIERS IN THE DATA FROM THE BEGINNING
amz = amz[(amz['date'].dt.month != 3)]
amz['month'] = amz['date'].dt.month
amz["month"].unique()
month_map = {4: 'april',5: 'may',6: 'june'}
amz['month'] = amz['date'].dt.month.map(month_map)


# Define the desired order of months
month_order = ['april', 'may', 'june']


# Convert the month column to a categorical data type with the desired order
amz['month'] = pd.Categorical(amz['month'], categories=month_order, ordered=True)
print(f'This dataset contains the months {amz["month"].unique()} for 2022')
print(f'The earliest date is {amz["date"].min()}')
print(f'The latest date is {amz["date"].max()}')

# Convert customer type column
amz['customer_type'].replace(to_replace=[True,False],value=['business','customer'], inplace=True)





## Now I want to order the column titled "size" so it can be in an order that is easily understood and vizualized
order_size = ['Free','XS', 'S', 'M', 'L', 'XL', 'XXL', '3XL', '4XL', '5XL', '6XL']

# Create an ordered categorical variable for the 'size' column
amz['size'] = pd.Categorical(amz['size'], categories = order_size, ordered = True)

print(amz['size'])

## I want to look over my dataset right now to check and see how the values look like. This will help me know of any final changes I may want to make before visualizing
print(amz.columns)
amz.info()
print(amz.head)
print(amz.nunique().to_frame(name='Count of unique values'))
print(amz.apply(pd.unique).to_frame(name='Unique Values'))

# print(amz.describe(include='all', datetime_is_numeric=True))
# ^ here, I was getting an error even through my datetime datatype is correct, I forgot the second part is not needed anymore in newer python, therefor the next lines:
# print(amz['date'])
# print(amz.describe(include='all'))
# print(amz.isnull().sum())
## Just as a brief overview, it seems we are good to go, if other inconsistencies occur later, they can be filtered through PowerBI or we can go back and add to our code

### DATA VISUALIZATION PYTHON ###



# Here, I want to set up a general Sales trend graph over time using the plt tool with a line plot
daily_sales = amz.groupby('date').agg(total_qty=('order_quantity', 'sum'), total_amount=('order_amount_($)', 'sum')).reset_index()
plt.figure(figsize=(10, 5))
sns.lineplot(data=daily_sales, x='date', y='total_qty', label='Total Quantity Sold', color='blue', linewidth=2)

print(daily_sales)
plt.title('Sales Trends Over Time')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.xticks(rotation=45)  
plt.legend()
plt.grid(True)
plt.show()


## I want to get a quick view of the top 5 product categories by order amount 
Top5_Products = amz.groupby('product_category')['order_amount_($)'].sum().to_frame().sort_values(by=['order_amount_($)'],ascending=False).head(5)
# print(Top5_Products)
Top5_Products.plot(kind='bar',color='#f0bda7')
plt.title('Total Amount by Category', fontsize=18, weight='bold')
plt.ylabel('Total Amount (in millions)', fontsize=14)
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.xticks(rotation=45, ha="right")
plt.legend()
plt.tight_layout()
plt.show()

## Profit and Loss Analysis by month







## Before I do too many graphs, I want to get a base understanding of the outstanding values that would be important to a business:
# 1. Revenue by month (Revenue defined by order amount as it is our measure for sale of goods)
# 2. Percentage Change from month to month
# 3. Total cancelled and returned
RevByMonth = amz.groupby('month')['order_amount_($)'].sum()
percent_decrease_apr_to_may = (RevByMonth['april'] - RevByMonth['may']) / RevByMonth['april'] * 100
percent_decrease_may_to_jun = (RevByMonth['may'] - RevByMonth['june']) / RevByMonth['may'] * 100
total_decrease = (RevByMonth['april'] - RevByMonth['june']) / RevByMonth['april'] * 100
print(f"Total revenue for April 2022: ${RevByMonth['april']:,.2f}")
print(f"Total revenue for May 2022: ${RevByMonth['may']:,.2f}, which is a -{percent_decrease_apr_to_may:.2f}% decrease from April.")
print(f"Total revenue for June 2022: ${RevByMonth['june']:,.2f}, which is a -{percent_decrease_may_to_jun:.2f}% decrease from May.")
print(f"Total revenue for Q2 2022 decreased by -{total_decrease:.2f}%")
print("\n")

revenue_by_category = amz.groupby('product_category')['order_amount_($)'].sum().sort_values(ascending=False)
print("Total revenue by product category:")
print(revenue_by_category.apply(lambda x: "${:,.2f}".format(x)))
print("\n")

revenue_by_category = amz.groupby('product_category')['order_amount_($)'].sum()
percent_revenue_by_category = ((revenue_by_category / revenue_by_category.sum()) * 100).sort_values(ascending=False)
percent_revenue_by_category = percent_revenue_by_category.apply(lambda x: "{:.2f}%".format(x))
print("Percentage of revenue by product category:")
print(percent_revenue_by_category)
print("\n")

avg_price_by_category = amz.groupby('product_category')['order_amount_($)'].mean()
avg_price_by_category = avg_price_by_category.sort_values(ascending=False)
print("Top 5 product categories by average price:")
print(avg_price_by_category.head(5))
print("\n")



cancelled_orders = amz[amz['ship_status'].isin(['Cancelled', 'Shipped - Lost in Transit'])]
returned_orders = amz[amz['ship_status'].isin(['Shipped - Returned to Seller', 'Shipped - Returning to Seller', 'Shipped - Rejected by Buyer', 'Shipped - Damaged'])]
# Use len function to get the amount of orders for each
total_cancelled = len(cancelled_orders)
total_returned = len(returned_orders)
total_cancelled_returned = total_cancelled + total_returned


percent_cancelled = total_cancelled / len(amz) * 100
percent_returned = total_returned / len(amz) * 100
percent_cancelled_returned = total_cancelled_returned / amz['order_quantity'].sum() * 100

print(f"Total cancelled orders: {total_cancelled}, which is {percent_cancelled:.2f}% of all orders inluded.")
print(f"Total returned orders: {total_returned}, which is {percent_returned:.2f}% of all orders included.")
print(f"This represents {percent_cancelled_returned:.2f}% of all orders.")
print("\n")

# monthly_order_data = amz.groupby(pd.Grouper(key='date', freq='M')).agg({'order_amount_($)': 'mean', 'order_quantity': 'mean'})
# monthly_order_data = monthly_order_data.rename(columns={'order_amount_($)': 'average_order_amount', 'order_quantity': 'average_order_quantity'})
# print(monthly_order_data)
# print("\n")

# popular_category_by_state = amz.groupby(['state', 'product_category'])['order_quantity'].sum().reset_index()
# popular_category_by_state = popular_category_by_state.sort_values(['state', 'order_quantity'], ascending=[True, False])
# popular_category_by_state = popular_category_by_state.drop_duplicates(subset=['state'])
# print("Most popular product category in each state:")
# print(popular_category_by_state)
# print("\n")

# avg_order_amount_by_customer_type = amz.groupby('customer_type')['order_amount_($)'].mean()
# print("Average order amount by customer type:")
# print(avg_order_amount_by_customer_type.apply(lambda x: "${:,.2f}".format(x)))




#################################################################
# Group the data by month and calculate the total sales revenue
monthly_sales = amz.groupby(pd.Grouper(key='date', freq='M')).agg({'order_amount_($)': 'sum'})

# Get latest month revenue and average quarterly revenue
latest_month_revenue = monthly_sales.tail(1).iloc[0][0]
avg_quarterly_revenue = monthly_sales.tail(3).head(2).mean()[0]

# Compute percentage below average revenue for quarter
below_avg = round((1 - (latest_month_revenue / avg_quarterly_revenue)) * 100, 1)

# Plot the monthly sales revenue
fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.bar(monthly_sales.index.strftime('%b'), monthly_sales['order_amount_($)'], color='#878787')

# Add label above each bar with the percentage below the average revenue for the quarter
for i, bar in enumerate(bars):
    if i == len(bars) - 1 or i < len(bars) - 2:
        continue
    month_sales = monthly_sales.iloc[i]['order_amount_($)']
    below_avg = round((1 - (month_sales / avg_quarterly_revenue)) * 100, 1)
    ax.annotate(f'{below_avg}% below avg.', 
                xy = (bar.get_x() + bar.get_width()/2, bar.get_height()-7000), 
                xytext = (0, 5), textcoords = 'offset points',  fontweight='bold', 
                ha = 'center', va = 'bottom', fontsize = 14)

# Add label above the latest bar with the percentage below the average revenue for the quarter
latest_bar = bars[-1]
latest_month_sales = latest_bar.get_height()
below_avg = round((1 - (latest_month_sales / avg_quarterly_revenue)) * 100, 1)
ax.annotate(f'{below_avg}% below avg.', 
            xy = (latest_bar.get_x() + latest_bar.get_width()/2, latest_bar.get_height()-7000), 
            xytext=(0, 5), textcoords = 'offset points',  fontweight='bold',
            ha = 'center', va = 'bottom', fontsize=14)
if below_avg > 0:
    label_text = f'{below_avg}% below avg.'
else:
    label_text = f'{abs(below_avg)}% above avg.'




# Add horizontal line at the average quarterly revenue
plt.axhline(avg_quarterly_revenue, linestyle='--', color='orange',linewidth=2, label='Q2 Average Revenue')

# We know these are India sales as we converted our currency from Indian Rupees to USD
ax.set_title('Amazon India Net Revenue', fontsize=20, x=.19, y=1.05)
ax.text(-.08, 1.02, 'Q2 FY22', fontsize=15, color='#878787', transform=ax.transAxes)
ax.set_xlabel(None)
ax.set_yticklabels(list(range(0,41,5)))
ax.set_ylabel('Net Revenue in 10,000 dollars', fontsize=12, labelpad=3)

ax.yaxis.grid(linestyle='--', color='gray', linewidth=0.5, dashes=(8, 5))
ax.xaxis.grid(False)


plt.legend(bbox_to_anchor=(1,1.05), fontsize=12, fancybox=True)

ax.tick_params(axis='both', labelsize=12)
# Remove top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_linewidth(2)
ax.spines['bottom'].set_color('black')
plt.show()


# After this practice on python, with help from both stack overflow and previous projects, I want to take a look at the data using a tool like PowerBI

amz.to_csv("UpdatedAmazonSaleReport.csv", index = False)