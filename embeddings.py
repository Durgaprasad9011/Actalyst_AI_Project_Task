# import openai
# import json
# import pandas as pd

# # Load OpenAI API key from environment variable
# import os
# openai.api_key = os.getenv('OPENAI_API_KEY')

# def load_csv(file_path):
#     return pd.read_csv(file_path)

# def get_embeddings(texts, model='text-embedding-ada-002'):
#     response = openai.Embedding.create(input=texts, model=model)
#     return [embedding['embedding'] for embedding in response['data']]

# def save_embeddings_as_json(embeddings, file_path):
#     with open(file_path, 'w') as f:
#         json.dump(embeddings, f)

# def main():
#     # Load scraped data
#     df = load_csv('news_data.csv')
#     texts = df['Title'].tolist() + df['Summary'].tolist()
    
#     # Get embeddings
#     embeddings = get_embeddings(texts)
    
#     # Save embeddings as JSON
#     save_embeddings_as_json(embeddings, 'embeddings.json')

# if __name__ == "__main__":
#     main()

# import openai
# import json
# import pandas as pd
# import os

# openai.api_key = os.getenv('OPENAI_API_KEY')

# def load_csv(file_path):
#     return pd.read_csv(file_path)

# def get_embeddings(texts, model='text-embedding-ada-002'):
#     response = openai.Embedding.create(input=texts, model=model)
#     return [embedding['embedding'] for embedding in response['data']]

# def save_embeddings_and_metadata_as_json(embeddings, metadata, file_path):
#     data = {"embeddings": embeddings, "metadata": metadata}
#     with open(file_path, 'w') as f:
#         json.dump(data, f)

# def main():
#     # Load scraped data
#     df = load_csv('news_data.csv')
#     texts = df['Title'].tolist() + df['Summary'].tolist()
    
#     # Get embeddings
#     embeddings = get_embeddings(texts)
    
#     # Prepare metadata
#     metadata = []
#     for i, (title, summary) in enumerate(zip(df['Title'], df['Summary'])):
#         metadata.append({"id": str(i), "title": title, "summary": summary})
    
#     # Save embeddings and metadata as JSON
#     save_embeddings_and_metadata_as_json(embeddings, metadata, 'embeddings_with_metadata.json')

# if __name__ == "__main__":
#     main()


import openai
import json
import pandas as pd
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

def load_csv(file_path):
    return pd.read_csv(file_path)

def get_embeddings(texts, model='text-embedding-ada-002'):
    response = openai.Embedding.create(input=texts, model=model)
    return [embedding['embedding'] for embedding in response['data']]

def save_embeddings_and_metadata_as_json(embeddings, metadata, file_path):
    data = {"embeddings": embeddings, "metadata": metadata}
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)  # Use indent=4 for pretty printing

def main():
    # Load scraped data
    df = load_csv('news_data.csv')
    
    # Ensure 'Date' column exists
    if 'Date' not in df.columns:
        raise ValueError("CSV file must contain a 'Date' column")
    
    texts = df['Title'].tolist() + df['Summary'].tolist()
    
    # Get embeddings
    embeddings = get_embeddings(texts)
    
    # Prepare metadata
    metadata = []
    for i, (title, summary, date) in enumerate(zip(df['Title'], df['Summary'], df['Date'])):
        metadata.append({"id": str(i), "title": title, "summary": summary, "date": date})
    
    # Save embeddings and metadata as JSON
    save_embeddings_and_metadata_as_json(embeddings, metadata, 'embeddings_and_metadata.json')

if __name__ == "__main__":
    main()
