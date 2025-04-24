from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def enhanced_sentence_match(expected_answer, student_answer):
    model = SentenceTransformer('./saved_model')
    embeddings_expected = model.encode([expected_answer])
    embeddings_student = model.encode([student_answer])
    similarity = cosine_similarity([embeddings_expected.flatten()], [embeddings_student.flatten()])[0][0]
    return similarity

def semantic_similarity_score(expected_answer, student_answer):
    model = SentenceTransformer('./saved_model')
    embeddings_expected = model.encode([expected_answer])
    embeddings_student = model.encode([student_answer])
    similarity = cosine_similarity([embeddings_expected.flatten()], [embeddings_student.flatten()])[0][0]
    return similarity