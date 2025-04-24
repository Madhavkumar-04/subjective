import os
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader
from flask_mysqldb import MySQL
import numpy as np

def fine_tune_sentence_transformer(mysql, model_path='./saved_model'):
    # Initialize the model
    if not os.path.exists(model_path):
        model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        model.save(model_path)
    else:
        model = SentenceTransformer(model_path)

    # Fetch data from database
    cur = mysql.connection.cursor()
    query = """
        SELECT ea.answer_text, sa.answer_text, sa.corrected_score, sa.score
        FROM StudentAnswers sa
        JOIN ExpectedAnswers ea ON sa.question_id = ea.question_id
        WHERE sa.score IS NOT NULL
    """
    cur.execute(query)
    data = cur.fetchall()
    cur.close()

    # Prepare training examples
    train_examples = []
    for row in data:
        expected_answer, student_answer, corrected_score, computed_score = row
        # Use corrected_score if available, else fall back to computed_score
        label = corrected_score / 10 if corrected_score is not None else computed_score / 10
        # Ensure label is in [0,1]
        label = max(0.0, min(1.0, float(label)))
        train_examples.append(InputExample(texts=[expected_answer, student_answer], label=label))

    # Skip training if insufficient data
    if len(train_examples) < 10:
        print("Insufficient data for fine-tuning. Need at least 10 examples.")
        return False

    # Create DataLoader
    train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)
    train_loss = losses.CosineSimilarityLoss(model)

    # Fine-tune the model
    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=1,
        warmup_steps=100,
        show_progress_bar=True
    )

    # Save the fine-tuned model
    model.save(model_path)
    print(f"Fine-tuned model saved to {model_path}")
    return True