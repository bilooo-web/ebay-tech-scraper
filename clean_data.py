import pandas as pd

df = pd.read_csv('ebay_tech_deals.csv', dtype=str)

df['price'] = df['price'].str.replace('US \$', '', regex=True)
df['price'] = df['price'].str.replace(',', '', regex=True) 
df['price'] = df['price'].str.strip()

df['original_price'] = df['original_price'].str.replace('US \$', '', regex=True)
df['original_price'] = df['original_price'].str.replace(',', '', regex=True)
df['original_price'] = df['original_price'].str.strip()

df['original_price'] = df['original_price'].replace(['N/A', ''], pd.NA)
df['original_price'] = df['original_price'].fillna(df['price'])

df['shipping'] = df['shipping'].replace(['N/A', '', ' '], 'Shipping info unavailable')


df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['original_price'] = pd.to_numeric(df['original_price'], errors='coerce')

df['discount_percentage'] = ((df['original_price'] - df['price']) / df['original_price']) * 100

df['discount_percentage'] = df['discount_percentage'].round(2)

# Save the cleaned data as 'cleaned_ebay_deals.csv'
df.to_csv('cleaned_ebay_deals.csv', index=False)

print("Data cleaning completed and saved to 'cleaned_ebay_deals.csv'.")
