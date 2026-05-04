import pandas as pd
import numpy as np
import tensorflow as tf
import ast
import sys
import os

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense, Dropout
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping

# ==========================
# CHECK ARGUMENT
# ==========================

if len(sys.argv) != 2:
    print("Usage: python src/train_dkt.py [math|physics|programming]")
    sys.exit()

subject = sys.argv[1].lower()

DATA_PATH = f"data/eval/{subject}_train.csv"
MODEL_PATH = f"models/dkt_{subject}.keras"

MAX_SEQ_LEN = 100
EMBED_DIM = 64
LSTM_UNITS = 100
BATCH_SIZE = 32
EPOCHS = 5

print(f"Loading {subject.capitalize()} training data...")

df = pd.read_csv(DATA_PATH)

# ==========================
# Convert string sequences
# ==========================

df["skill_sequence"] = df["skill_sequence"].apply(
    lambda x: ast.literal_eval(x) if isinstance(x, str) else x
)

df["correct_sequence"] = df["correct_sequence"].apply(
    lambda x: ast.literal_eval(x) if isinstance(x, str) else x
)

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
# BUILD DKT MODEL
# ==========================

skill_input = Input(shape=(MAX_SEQ_LEN,))

embedding = Embedding(
    input_dim=num_skills,
    output_dim=EMBED_DIM,
    mask_zero=True
)(skill_input)

lstm_out = LSTM(
    LSTM_UNITS,
    return_sequences=True
)(embedding)

drop = Dropout(0.2)(lstm_out)

output = Dense(1, activation="sigmoid")(drop)

model = Model(inputs=skill_input, outputs=output)

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

print(f"Training DKT {subject.capitalize()} model...")

model.fit(
    X,
    y,
    batch_size=BATCH_SIZE,
    epochs=EPOCHS,
    callbacks=[early_stop]
)

# ==========================
# SAVE MODEL
# ==========================

os.makedirs("models", exist_ok=True)
model.save(MODEL_PATH)

print(f"DKT {subject.capitalize()} model saved successfully ✅")
