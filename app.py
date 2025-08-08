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
        :root {
            --bg-gradient: linear-gradient(to right, #4facfe, #00f2fe);
            --container-bg: white;
            --text-color: #333;
            --subtitle-color: #666;
            --button-bg: #4facfe;
            --button-hover: #00c3ff;
            --footer-color: #777;
        }
        body.dark {
            --bg-gradient: linear-gradient(to right, #141e30, #243b55);
            --container-bg: #1f2937;
            --text-color: #f3f4f6;
            --subtitle-color: #9ca3af;
            --button-bg: #374151;
            --button-hover: #4b5563;
            --footer-color: #9ca3af;
        }
        body {
            font-family: Arial, sans-serif;
            background: var(--bg-gradient);
            color: var(--text-color);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 15px;
            transition: background 0.3s;
        }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px) scale(0.98); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes buttonClick {
            0% { transform: scale(1); background-color: var(--button-bg); }
            50% { transform: scale(0.95); background-color: var(--button-hover); }
            100% { transform: scale(1); background-color: var(--button-bg); }
        }
        .container {
            background: var(--container-bg);
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            text-align: center;
            width: 100%;
            max-width: 400px;
            animation: fadeInUp 0.6s ease-out forwards;
            transition: background 0.3s;
        }
        h1 {
            margin-bottom: 5px;
            color: var(--button-bg);
            font-size: 24px;
            opacity: 0;
            animation: fadeIn 0.8s ease-out forwards;
        }
        .subtitle {
            font-size: 12px;
            color: var(--subtitle-color);
            margin-bottom: 20px;
            opacity: 0;
            animation: fadeIn 0.8s ease-out forwards;
            animation-delay: 0.1s;
        }
        input {
            padding: 12px;
            width: 100%;
            border-radius: 8px;
            border: 1px solid #ccc;
            margin-bottom: 15px;
            font-size: 16px;
            box-sizing: border-box;
            opacity: 0;
            animation: fadeIn 1s ease-out forwards;
            animation-delay: 0.2s;
        }
        button {
            padding: 14px;
            width: 100%;
            background: var(--button-bg);
            border: none;
            border-radius: 8px;
            color: white;
            font-size: 16px;
            cursor: pointer;
            transition: background 0.3s;
            opacity: 0;
            animation: fadeIn 1.2s ease-out forwards;
            animation-delay: 0.4s;
        }
        button:hover {
            background: var(--button-hover);
        }
        button.clicked {
            animation: buttonClick 0.25s ease;
        }
        .result {
            margin-top: 15px;
            font-size: 18px;
            font-weight: bold;
            color: var(--text-color);
            word-wrap: break-word;
            opacity: 0;
            transition: opacity 0.6s ease;
        }
        .result.show {
            opacity: 1;
        }
        .footer {
            margin-top: 20px;
            font-size: 12px;
            color: var(--footer-color);
            opacity: 0;
            animation: fadeIn 1.6s ease-out forwards;
            animation-delay: 0.8s;
        }
        .footer a {
            color: var(--footer-color);
            text-decoration: none;
        }
        .footer a:hover {
            text-decoration: underline;
            color: var(--button-bg);
        }
        .theme-toggle {
            position: absolute;
            top: 15px;
            right: 15px;
            background: none;
            border: none;
            font-size: 20px;
            cursor: pointer;
            color: white;
        }
    </style>
</head>
<body>
    <button class="theme-toggle">🌙</button>
    <div class="container">
        <h1>Введите текст</h1>
        <div class="subtitle">(на латинице, без пробелов)</div>
        <form method='POST'>
            <input id="user_input" name='user_input' placeholder='Например: abc123' required>
            <button type='submit'>Рассчитать</button>
        </form>
        {% if result is not none %}
            <div class="result" data-value="{{ result }}">Сумма: {{ result }}</div>
        {% endif %}
        <div class="footer">
            created by <a href="https://instagram.com/araiym.live" target="_blank">@araiym.live</a>
        </div>
    </div>

    <script>
        document.addEventListener("DOMContentLoaded", function() {
            const input = document.getElementById("user_input");
            const resultBlock = document.querySelector(".result");
            const form = document.querySelector("form");
            const button = form.querySelector("button");
            const themeToggle = document.querySelector(".theme-toggle");

            // Автофокус
            input.focus();

            // Восстановление значения
            input.value = localStorage.getItem("user_input") || "";
            input.addEventListener("input", () => {
                localStorage.setItem("user_input", input.value);
            });

            // Анимация результата (count-up)
            if (resultBlock) {
                setTimeout(() => resultBlock.classList.add("show"), 50);
                const finalValue = parseInt(resultBlock.dataset.value);
                if (!isNaN(finalValue)) {
                    let current = 0;
                    const step = Math.ceil(finalValue / 30);
                    const interval = setInterval(() => {
                        current += step;
                        if (current >= finalValue) {
                            current = finalValue;
                            clearInterval(interval);
                        }
                        resultBlock.textContent = "Сумма: " + current;
                    }, 20);
                }
            }

            // Плавное исчезновение результата при повторном вводе
            form.addEventListener("submit", () => {
                if (resultBlock) {
                    resultBlock.classList.remove("show");
                }
                button.classList.add("clicked");
                setTimeout(() => button.classList.remove("clicked"), 250);
            });

            // Переключение темы
            themeToggle.addEventListener("click", () => {
                document.body.classList.toggle("dark");
                themeToggle.textContent = document.body.classList.contains("dark") ? "☀️" : "🌙";
            });
        });
    </script>
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

# Запуск
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
