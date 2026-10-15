import requests, pandas as pd, matplotlib.pyplot as plt
 
URL = 'https://mars.nasa.gov/rss/api/?feed=weather&category=msl&feedtype=json'
df = pd.DataFrame(requests.get(URL).json()['soles'])
 
num_cols = ['sol', 'ls', 'min_temp', 'max_temp', 'pressure',
            'min_gts_temp', 'max_gts_temp']
df[num_cols] = df[num_cols].apply(pd.to_numeric, errors='coerce')   # '--' becomes NaN
df['terrestrial_date'] = pd.to_datetime(df['terrestrial_date'])
df = df.sort_values('sol').reset_index(drop=True)
 
# flag readings far from their neighbours instead of deleting by eye
rolling = df['min_temp'].rolling(15, center=True, min_periods=5).median()
df['min_temp_outlier'] = (df['min_temp'] - rolling).abs() > 15
print(df['min_temp_outlier'].sum(), 'suspicious min temp readings')
 
clean = df[~df['min_temp_outlier']]
plt.scatter(clean['ls'], clean['pressure'], s=4,
            c=clean['terrestrial_date'].dt.year, cmap='viridis')
plt.colorbar(label='Earth year')
plt.xlabel('solar longitude (deg)'); plt.ylabel('pressure (Pa)')
plt.title('Gale Crater pressure through the Martian year')
plt.savefig('gale_pressure.png',dpi=200)
plt.show()