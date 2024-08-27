from flask import Flask, render_template, request

app = Flask(__name__)

# Sorular ve cevaplar
questions = [
    {"soru": "Python nedir?", "secenekler": ["Programlama dili", "Hayvan", "Oyun", "Yemek"], "dogru_cevap": "Programlama dili"},
    {"soru": "Flask nedir?", "secenekler": ["Veritabanı", "Web çerçevesi", "Python modülü", "Metin düzenleyici"], "dogru_cevap": "Web çerçevesi"},
    {"soru": "SQLAlchemy nedir?", "secenekler": ["Veritabanı ORM'i", "Python kütüphanesi", "Web çerçevesi", "Veritabanı dili"], "dogru_cevap": "Veritabanı ORM'i"},
    {"soru": "Python'da bir liste nasıl tanımlanır?", "secenekler": ["{} ile", "[] ile", "() ile", "'' ile"], "dogru_cevap": "[] ile"},
    {"soru": "Python'da döngü hangi kelime ile başlar?", "secenekler": ["for", "while", "do", "repeat"], "dogru_cevap": "for"},
    {"soru": "Python hangi yıl ortaya çıkmıştır? (Serbest cevap)", "secenekler": [], "dogru_cevap": "1991"}
]

# En yüksek skoru dosyadan okuma
def get_highest_score():
    try:
        with open('highest_score.txt', 'r') as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0

# En yüksek skoru dosyaya yazma
def set_highest_score(score):
    with open('highest_score.txt', 'w') as file:
        file.write(str(score))

# `enumerate` fonksiyonunu Jinja2'ye ekleme
def enumerate_helper(iterable, start=0):
    return list(enumerate(iterable, start=start))

app.jinja_env.globals.update(enumerate=enumerate_helper)

# Ana sayfa rotası
@app.route('/')
def index():
    highest_score = get_highest_score()
    return render_template('index.html', questions=questions, highest_score=highest_score)

# Cevap gönderme ve sonucu gösterme rotası
@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    for idx, question in enumerate(questions):
        if question['secenekler']:
            # Çoktan seçmeli soru
            selected_option = request.form.get(f'question{idx}')
            if selected_option == question['dogru_cevap']:
                score += 1
        else:
            # Serbest cevaplı soru
            user_answer = request.form.get(f'question{idx}')
            if user_answer.strip().lower() == question['dogru_cevap'].lower():
                score += 1

    # En yüksek skoru güncelle
    highest_score = get_highest_score()
    if score > highest_score:
        set_highest_score(score)
        highest_score = score  # Güncellenmiş en yüksek skoru kullanıcıya göster

    return render_template('result.html', score=score, total_questions=len(questions), highest_score=highest_score)

if __name__ == '__main__':
    app.run(debug=True)
