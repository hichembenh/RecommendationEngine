import pandas as pd

df = pd.read_csv('links_out.csv')

print('df')
print("There is", len(df), "Hotel, in", len(df.Country.unique()), "country")
print(df.isnull().sum())

print('\n')

new_df = df.dropna()
print('new_df')
print("There is", len(new_df), "Hotel, in", len(new_df.Country.unique()), "country")
print(new_df.isnull().sum())

new_df = new_df[~new_df["link_to_hotel"].str.contains("https")]

print("There is", len(new_df), "Hotel with accessible URL, in", len(new_df.Country.unique()), "country")

new_df['link_to_hotel'] = 'www.expedia.fr' + df['link_to_hotel'].astype(str)
print(new_df.head())

new_df.to_csv("links_ready.csv", encoding='utf-8')

