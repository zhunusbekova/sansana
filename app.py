from flask import Flask, request, render_template_string, send_from_directory
import os

app = Flask(__name__)

# Логика калькулятора
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

# HTML-шаблон
HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Калькулятор Сюцай</title>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to right, #4facfe, #00f2fe);
            color: #333;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 15px;
        }
        .container {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            text-align: center;
            width: 100%;
            max-width: 400px;
            animation: fadeIn 0.6s ease-in-out;
        }
        h1 {
            margin-bottom: 5px;
            color: #4facfe;
            font-size: 24px;
        }
        .subtitle {
            font-size: 12px;
            color: #666;
            margin-bottom: 20px;
        }
        input {
            padding: 12px;
            width: 100%;
            border-radius: 8px;
            border: 1px solid #ccc;
            margin-bottom: 15px;
            font-size: 16px;
            box-sizing: border-box;
        }
        button {
            padding: 12px;
            width: 100%;
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
            word-wrap: break-word;
        }
        .footer {
            margin-top: 20px;
            font-size: 12px;
            color: #777;
        }
        .footer a {
            color: #777;
            text-decoration: none;
        }
        .footer a:hover {
            text-decoration: underline;
            color: #4facfe;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Введите текст</h1>
        <div class="subtitle">(на латинице, без пробелов)</div>
        <form method='POST'>
            <input name='user_input' placeholder='Например: abc123' required>
            <button type='submit'>Рассчитать</button>
        </form>
        {% if result is not none %}
            <div class="result">Сумма: {{ result }}</div>
        {% endif %}
        <div class="footer">
            created by <a href="https://instagram.com/araiym.live" target="_blank">@araiym.live</a>
        </div>
    </div>
</body>
</html>
"""

# Маршрут для favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, ''),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Главная страница
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        user_input = request.form.get("user_input", "")
        result = calculate_sum(user_input)
    return render_template_string(HTML_TEMPLATE, result=result)

# Запуск для Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
