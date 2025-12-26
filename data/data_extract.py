import pandas as pd

df = pd.read_parquet('0000.parquet')
texts = df['text'].tolist()

with open('all_data.txt', 'w', encoding='utf-8') as f:
    for text in texts:
        clean_text = text.replace('\n', ' ') 
        f.write(clean_text + '\n')