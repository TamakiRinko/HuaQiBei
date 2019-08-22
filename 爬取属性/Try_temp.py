import pandas as pd


df = pd.DataFrame({
'p_str': ['10.33%','23.22%','56%','35.786%','99.0009%']
})
print(df)
p_float = df['p_str'].str.strip("%").astype(float)/100
print(p_float)
print(type(p_float))