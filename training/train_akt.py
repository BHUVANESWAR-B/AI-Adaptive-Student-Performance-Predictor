import pandas as pd
import numpy as np
import tensorflow as tf
import ast
import sys
import os

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, MultiHeadAttention
from tensorflow.keras.layers import LayerNormalization, Dropout, Dense, Add
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping

# ==========================
# SUBJECT ARGUMENT
# ==========================

if len(sys.argv) < 2:
    print("Usage: python src/train_akt.py [math|physics|programming]")
    sys.exit(1)

SUBJECT = sys.argv[1].lower()

DATA_PATH = f"data/eval/{SUBJECT}_train.csv"
MODEL_PATH = f"models/akt_{SUBJECT}.keras"

print(f"Training AKT for {SUBJECT.upper()}")

# ==========================
# CONFIG
# ==========================

MAX_SEQ_LEN = 100
EMBED_DIM = 64
NUM_HEADS = 4
DROPOUT_RATE = 0.2
BATCH_SIZE = 32
EPOCHS = 5

# ==========================
# LOAD DATA
# ==========================

df = pd.read_csv(DATA_PATH)

if "skill_sequence" in df.columns:
    df["skill_sequence"] = df["skill_sequence"].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else x
    )

    df["correct_sequence"] = df["correct_sequence"].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else x
    )
else:
    df = df.sort_values(["user_id", "order_id"])
    grouped = df.groupby("user_id")

    df = pd.DataFrame({
        "skill_sequence": grouped["skill_encoded"].apply(list),
        "correct_sequence": grouped["correct"].apply(list)
    })

print("Total students:", len(df))

# ==========================
# PAD SEQUENCES
# ==========================

X = pad_sequences(
    df["skill_sequence"].tolist(),
    maxlen=MAX_SEQ_LEN,
    padding="post",
    truncating="post"
)

y = pad_sequences(
    df["correct_sequence"].tolist(),
    maxlen=MAX_SEQ_LEN,
    padding="post",
    truncating="post"
)

y = np.expand_dims(y, -1)

num_skills = int(np.max(X)) + 1
print("Total skills:", num_skills)

# ==========================
# BUILD AKT MODEL
# ==========================

skill_input = Input(shape=(MAX_SEQ_LEN,))
embedding = Embedding(num_skills, EMBED_DIM, mask_zero=True)(skill_input)

attention = MultiHeadAttention(
    num_heads=NUM_HEADS,
    key_dim=EMBED_DIM
)(embedding, embedding)

x = Add()([embedding, attention])
x = LayerNormalization()(x)
x = Dropout(DROPOUT_RATE)(x)

output = Dense(1, activation="sigmoid")(x)

model = Model(skill_input, output)

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# ==========================
# TRAIN
# ==========================

early_stop = EarlyStopping(
    monitor="loss",
    patience=2,
    restore_best_weights=True
)

model.fit(
    X,
    y,
    batch_size=BATCH_SIZE,
    epochs=EPOCHS,
    callbacks=[early_stop]
)

# ==========================
# SAVE
# ==========================

os.makedirs("models", exist_ok=True)
model.save(MODEL_PATH)

print(f"AKT {SUBJECT.upper()} model saved successfully ✅")
