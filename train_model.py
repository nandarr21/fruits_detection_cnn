import json
import tensorflow as tf
from tensorflow.keras import layers, models

IMG_SIZE = (128, 128)
BATCH_SIZE = 32
EPOCHS = 10

# Load Dataset
train_ds = tf.keras.utils.image_dataset_from_directory(
    "dataset/train", image_size=IMG_SIZE, batch_size=BATCH_SIZE)

val_ds = tf.keras.utils.image_dataset_from_directory(
    "dataset/test", image_size=IMG_SIZE, batch_size=BATCH_SIZE)

class_names = train_ds.class_names
print("Kelas:", class_names)

# Normalisasi
normalization_layer = layers.Rescaling(1. / 255)
train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))

# Model CNN
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
    layers.MaxPooling2D((2, 2)),

    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),

    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),

    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(len(class_names), activation='softmax')
])

model.compile(optimizer='adam',
               loss='sparse_categorical_crossentropy',
               metrics=['accuracy'])

model.summary()

# Training
history = model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS)

# Evaluasi
test_loss, test_acc = model.evaluate(val_ds)
print(f"\nAkurasi pada data uji: {test_acc:.4f}")

# Simpan Model & Label
model.save("model/model_buah.h5")

with open("model/class_names.json", "w") as f:
    json.dump(class_names, f)

print("Model dan label kelas berhasil disimpan di folder 'model/'")
