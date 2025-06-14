import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer
import torch
from sklearn.metrics import classification_report

df = pd.read_csv("dataset.csv")
texts = df["text"].tolist()
labels = df["label"].tolist()

train_texts, test_texts, train_labels, test_labels = train_test_split(
    texts, labels, test_size=0.2, random_state=42
)

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
test_encodings = tokenizer(test_texts, truncation=True, padding=True)

# Dataset
class NewsDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels
    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item
    def __len__(self):
        return len(self.labels)

test_dataset = NewsDataset(test_encodings, test_labels)
model = AutoModelForSequenceClassification.from_pretrained("./results/checkpoint-3")

trainer = Trainer(model=model)
preds = trainer.predict(test_dataset)
pred_labels = preds.predictions.argmax(-1)

print(classification_report(test_labels, pred_labels))
