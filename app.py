import os
import numpy as np
from flask import Flask, render_template, request, redirect, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

IMG_SIZE = (128, 128)
model = load_model('model/model_buah.h5')

# Urutan label 
LABELS = {
    0: {"kelas": "Busuk", "status": "Tidak layak"},
    1: {"kelas": "Segar", "status": "Layak konsumsi"}
}


def predict_image(filepath):
    img = load_img(filepath, target_size=IMG_SIZE)
    arr = img_to_array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)

    pred = model.predict(arr)[0]

    if len(pred) == 1:  # output sigmoid (1 neuron)
        prob_busuk = pred[0]
        idx = 1 if prob_busuk > 0.5 else 0
        confidence = prob_busuk if idx == 1 else 1 - prob_busuk
    else:  # output softmax (2 neuron)
        idx = int(np.argmax(pred))
        confidence = pred[idx]

    label = LABELS[idx]
    return label["kelas"], label["status"], round(float(confidence) * 100, 2)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    file = request.files.get('file')
    if not file or not file.filename:
        return redirect(url_for('index'))

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    kelas, status, confidence = predict_image(filepath)
    result = {"kelas": kelas, "status": status, "confidence": confidence}

    return render_template('result.html', result=result, filename=filename)


if __name__ == '__main__':
    app.run(debug=True)