from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

def calculate_sum(num):
    sum_letters = 0
    for letter in str(num).lower():
        if letter in ["a", "i", "j", "q", "y"]:
            sum_letters += 1
        elif letter in ["b", "k", "r"]:
            sum_letters += 2
        elif letter in ["c", "l", "s", "g"]:
            sum_letters += 3
        elif letter in ["d", "m", "t"]:
            sum_letters += 4
        elif letter in ["e", "h", "n", "x"]:
            sum_letters += 5
        elif letter in ["u", "v", "w"]:
            sum_letters += 6
        elif letter in ["o", "z"]:
            sum_letters += 7
        elif letter in ["f", "p"]:
            sum_letters += 8
        else:
            try:
                sum_letters += int(letter)
            except:
                pass
    return sum_letters

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>Сумма букв и чисел</title>
</head>
<body>
    <h1>Введите текст на латинице:</h1>
    <form method='POST'>
        <input name='user_input' placeholder='Введите значение' required>
        <button type='submit'>Рассчитать</button>
    </form>
    {% if result is not none %}
        <h2>Сумма: {{ result }}</h2>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        user_input = request.form.get("user_input", "")
        result = calculate_sum(user_input)
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host="0.0.0.0", port=port)
