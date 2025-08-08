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
    <meta charset="utf-8">
    <title>Калькулятор СЮЦАЙ</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to right, #4facfe, #00f2fe);
            color: #333;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            text-align: center;
            width: 350px;
        }
        h1 {
            margin-bottom: 20px;
            color: #4facfe;
        }
        input {
            padding: 10px;
            width: 80%;
            border-radius: 8px;
            border: 1px solid #ccc;
            margin-bottom: 15px;
            font-size: 16px;
        }
        button {
            padding: 10px 20px;
            background: #4facfe;
            border: none;
            border-radius: 8px;
            color: white;
            font-size: 16px;
            cursor: pointer;
            transition: background 0.3s;
        }
        button:hover {
            background: #00c3ff;
        }
        .result {
            margin-top: 15px;
            font-size: 18px;
            font-weight: bold;
            color: #333;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Введите текст на латинице</h1>
        <form method='POST'>
            <input name='user_input' placeholder='Введите значение' required>
            <br>
            <button type='submit'>Рассчитать</button>
        </form>
        {% if result is not none %}
            <div class="result">Сумма: {{ result }}</div>
        {% endif %}
    </div>
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
