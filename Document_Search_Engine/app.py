import os
import glob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Directory with all the text files
DATA_DIR = "./documents"

def read_files(filepaths):
    """Read and return the content of the given text files."""
    documents = []
    for filepath in filepaths:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            documents.append(content)
    return documents

def search_documents(query, documents, filepaths):
    """Search and rank documents based on their relevance to the query."""
    # Create a new TfidfVectorizer and transform the documents to vectors
    vectorizer = TfidfVectorizer(stop_words='english')
    doc_vectors = vectorizer.fit_transform(documents)

    # Transform the query using the same vectorizer
    query_vector = vectorizer.transform([query])

    # Compute the cosine similarity between query and documents
    cosine_similarities = linear_kernel(query_vector, doc_vectors).flatten()

    # Rank documents by similarity score
    ranked_scores = [(filepaths[i], score) for i, score in enumerate(cosine_similarities)]
    ranked_scores.sort(key=lambda x: x[1], reverse=True)

    return ranked_scores

def main():
    filepaths = glob.glob(os.path.join(DATA_DIR, "*.txt"))
    documents = read_files(filepaths)

    query = input("Enter your search query: ")
    ranked_docs = search_documents(query, documents, filepaths)

    print("\nTop 5 relevant documents:")
    for i, (doc, score) in enumerate(ranked_docs[:5]):
        print(f"{i+1}. {os.path.basename(doc)} with a score of {score:.4f}")

if __name__ == "__main__":
    main()
