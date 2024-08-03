import streamlit as st
import openai
import os
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# Load embeddings and metadata from JSON file
def load_embeddings_and_metadata(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data['embeddings'], data['metadata']

# Load data
embeddings, metadata = load_embeddings_and_metadata('embeddings_and_metadata.json')

# Function to find the most similar embeddings
def find_similar_embeddings(query_embedding, embeddings, top_k=5):
    similarities = cosine_similarity([query_embedding], embeddings)
    top_indices = similarities[0].argsort()[-top_k:][::-1]
    
    # Print cosine similarity values to console
    print("Cosine Similarity Values:")
    for idx in top_indices:
        print(f"Index: {idx}, Similarity: {similarities[0][idx]}")
    
    return top_indices

# Function to get a response from GPT-4 based on context
def get_gpt_response(query, context):
    try:
        # Combine context into a prompt
        prompt = f"Based on the following information, answer the user's query:\n\nContext:\n{context}\n\nUser Query: {query}"
        
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[
                {'role': 'user', 'content': prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI setup
st.title("News Chatbot")
st.write("Ask me about the latest news articles!")

# User input
user_query = st.text_input("Your question:")

if st.button("Ask"):
    if user_query:
        # Get embedding for the user query
        try:
            query_response = openai.Embedding.create(input=[user_query], model='text-embedding-ada-002')
            query_embedding = query_response['data'][0]['embedding']
        except Exception as e:
            st.error(f"Error getting query embedding: {str(e)}")
            st.stop()

        # Find similar embeddings
        top_indices = find_similar_embeddings(query_embedding, embeddings)
        
        # Prepare context from relevant articles
        context = ""
        relevant_articles = []
        valid_indices = [index for index in top_indices if index < len(metadata)]
        
        if valid_indices:
            for index in valid_indices:
                doc = metadata[index]
                relevant_articles.append(doc)
                context += f"Title: {doc.get('title', 'N/A')}\nSummary: {doc.get('summary', 'N/A')}\nDate: {doc.get('date', 'N/A')}\n\n"
        else:
            context = "No relevant articles found."
        
        # Display relevant articles
        st.subheader("Relevant Articles:")
        if relevant_articles:
            for doc in relevant_articles:
                st.write(f"- **Title:** {doc.get('title', 'N/A')}")
                st.write(f"  **Summary:** {doc.get('summary', 'N/A')}")
                st.write(f"  **Date:** {doc.get('date', 'N/A')}")
        else:
            st.write("No relevant articles found.")

        # Get response from GPT-4 based on context
        gpt_response = get_gpt_response(user_query, context)
        
        # Display GPT-4 response
        st.subheader("GPT-4 Response:")
        st.write(gpt_response)
    else:
        st.warning("Please enter a question.")
