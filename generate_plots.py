import matplotlib.pyplot as plt
import numpy as np

# Simulated data for evaluation metrics
metrics = ['Exact Match', 'Partial Match', 'Cosine Similarity', 'Sentiment Analysis',
           'Enhanced Match', 'Naive Bayes', 'Semantic Similarity', 'Coherence', 'Relevance', 'Combined']
errors = [2.5, 1.3, 1.5, 1.8, 1.2, 1.2, 0.9, 1.4, 1.3, 1.0]

# Bar chart for average error
plt.figure(figsize=(10, 6))
plt.bar(metrics, errors, color='#3182ce')
plt.title('Average Error of Evaluation Metrics')
plt.xlabel('Metric')
plt.ylabel('Average Error (Points)')
plt.xticks(rotation=45, ha='right')
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('error_plot.png', bbox_inches='tight')
plt.close()

# Simulated data for scatter plot (AES vs. manual scores)
np.random.seed(42)
manual_scores = np.random.uniform(4, 10, 10)  # Simulated manual scores (4-10)
aes_scores = manual_scores + np.random.normal(0, 1.0, 10)  # Simulated AES scores with noise
aes_scores = np.clip(aes_scores, 0, 10)  # Ensure scores are within 0-10

# Scatter plot for AES vs. manual scores
plt.figure(figsize=(8, 6))
plt.scatter(manual_scores, aes_scores, color='#3182ce', alpha=0.6)
plt.plot([0, 10], [0, 10], 'r--', label='Ideal Line')
plt.title('AES Scores vs. Manual Scores')
plt.xlabel('Manual Scores (Points)')
plt.ylabel('AES Scores (Points)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.savefig('scatter_plot.png', bbox_inches='tight')
plt.close()

# Simulated data for error distribution
errors_simulated = np.random.normal(1.0, 0.5, 50)  # Simulated errors centered around 1.0
errors_simulated = np.clip(errors_simulated, 0, 5)  # Ensure errors are realistic

# Histogram for error distribution
plt.figure(figsize=(8, 6))
plt.hist(errors_simulated, bins=10, color='#3182ce', edgecolor='black')
plt.title('Error Distribution of AES Scores')
plt.xlabel('Error (Points)')
plt.ylabel('Frequency')
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.savefig('error_dist_plot.png', bbox_inches='tight')
plt.close()