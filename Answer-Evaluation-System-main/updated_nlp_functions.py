from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os

def enhanced_sentence_match(expected_answer, student_answer):
    model_path = './saved_model'
    try:
        if os.path.exists(model_path) and os.path.isfile(os.path.join(model_path, 'config.json')):
            model = SentenceTransformer(model_path)
        else:
            raise ValueError("Invalid model path")
    except Exception as e:
        print(f"Error loading fine-tuned model: {e}. Falling back to default model.")
        model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embeddings_expected = model.encode([expected_answer])
    embeddings_student = model.encode([student_answer])
    similarity = cosine_similarity([embeddings_expected.flatten()], [embeddings_student.flatten()])[0][0]
    return similarity

def semantic_similarity_score(expected_answer, student_answer):
    model_path = './saved_model'
    try:
        if os.path.exists(model_path) and os.path.isfile(os.path.join(model_path, 'config.json')):
            model = SentenceTransformer(model_path)
        else:
            raise ValueError("Invalid model path")
    except Exception as e:
        print(f"Error loading fine-tuned model: {e}. Falling back to default model.")
        model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embeddings_expected = model.encode([expected_answer])
    embeddings_student = model.encode([student_answer])
    similarity = cosine_similarity([embeddings_expected.flatten()], [embeddings_student.flatten()])[0][0]
    return similarity