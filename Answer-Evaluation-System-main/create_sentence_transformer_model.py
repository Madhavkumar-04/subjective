from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader
import os

def fine_tune_sentence_transformer(model_path='./saved_model'):
    # Initialize the base model
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    # Manually defined training data for "What is photosynthesis?"
    training_data = [
        # Expected Answer: "Photosynthesis is the process by which green plants, algae, and some bacteria use sunlight, water, and carbon dioxide to produce glucose and oxygen."
        ("Photosynthesis is the process by which green plants, algae, and some bacteria use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
         "Photosynthesis is how plants use sunlight to make food from carbon dioxide and water, producing oxygen.", 9),
        ("Photosynthesis is the process by which green plants, algae, and some bacteria use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
         "It’s the process where plants make glucose using light, water, and CO2, releasing oxygen.", 10),
        ("Photosynthesis is the process by which green plants, algae, and some bacteria use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
         "Plants use sunlight to convert water and carbon dioxide into sugar.", 8),
        ("Photosynthesis is the process by which green plants, algae, and some bacteria use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
         "Photosynthesis is when plants make their own food.", 6),
        ("Photosynthesis is the process by which green plants, algae, and some bacteria use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
         "It’s how plants grow using sunlight.", 4),
        ("Photosynthesis is the process by which green plants, algae, and some bacteria use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
         "Plants take in sunlight and make oxygen.", 5),
        ("Photosynthesis is the process by which green plants, algae, and some bacteria use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
         "Photosynthesis uses chlorophyll to make energy.", 6),
        ("Photosynthesis is the process by which green plants, algae, and some bacteria use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
         "It’s a process that makes glucose in plants with light.", 7),
        ("Photosynthesis is the process by which green plants, algae, and some bacteria use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
         "Plants use carbon dioxide and water to make food in sunlight, giving off oxygen.", 9),
        ("Photosynthesis is the process by which green plants, algae, and some bacteria use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
         "Photosynthesis is the process of plants making food with sunlight, water, and air.", 8),
        ("Photosynthesis is the process by which green plants, algae, and some bacteria use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
         "It’s when plants use sunlight to make sugar and oxygen from CO2 and water.", 10),
        ("Photosynthesis is the process by which green plants, algae, and some bacteria use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
         "Plants make energy from sunlight.", 5),
        ("Photosynthesis is the process by which green plants, algae, and some bacteria use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
         "Photosynthesis is how plants breathe and make food.", 4),
        ("Photosynthesis is the process by which green plants, algae, and some bacteria use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
         "It’s a chemical reaction in plants using sunlight.", 6)
    ]

    # Prepare training examples
    train_examples = []
    for expected_answer, student_answer, score in training_data:
        # Scale score to 0-1 (assuming input scores are 0-10)
        label = score / 10
        label = max(0.0, min(1.0, float(label)))
        train_examples.append(InputExample(texts=[expected_answer, student_answer], label=label))

    # Check if sufficient data is available
    if len(train_examples) < 10:
        print(f"Insufficient data for fine-tuning. Found {len(train_examples)} examples, need at least 10.")
        return False

    # Create data loader
    train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)
    train_loss = losses.CosineSimilarityLoss(model)

    # Fine-tune the model
    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=1,
        warmup_steps=100,
        show_progress_bar=True
    )

    # Save the model
    os.makedirs(model_path, exist_ok=True)
    model.save(model_path)
    print(f"Fine-tuned model saved to {model_path}")
    return True

if __name__ == '__main__':
    success = fine_tune_sentence_transformer()
    print(f"Fine-tuning {'succeeded' if success else 'failed'}")