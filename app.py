from flask import Flask, request, jsonify, render_template_string, send_from_directory
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
    # Сведение к одной цифре
    while sum_letters > 9:
        sum_letters = sum(int(d) for d in str(sum_letters))
    
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
        --error-color: #e74c3c;
    }
    body.dark {
        --bg-gradient: linear-gradient(to right, #141e30, #243b55);
        --container-bg: #1f2937;
        --text-color: #f3f4f6;
        --subtitle-color: #9ca3af;
        --button-bg: #374151;
        --button-hover: #4b5563;
        --footer-color: #9ca3af;
        --error-color: #ff7675;
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
    .container {
        background: var(--container-bg);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        text-align: center;
        width: 100%;
        max-width: 400px;
        transition: background 0.3s;
    }
    h1 {
        margin-bottom: 5px;
        color: var(--button-bg);
        font-size: 24px;
    }
    .subtitle {
        font-size: 12px;
        color: var(--subtitle-color);
        margin-bottom: 20px;
    }
    input {
        padding: 12px;
        width: 100%;
        border-radius: 8px;
        border: 1px solid #ccc;
        margin-bottom: 10px;
        font-size: 16px;
        box-sizing: border-box;
        outline: none;
        transition: border 0.3s;
    }
    input.error {
        border: 2px solid var(--error-color);
    }
    .error-message {
        font-size: 12px;
        color: var(--error-color);
        margin-bottom: 10px;
        display: none;
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
    }
    button:hover {
        background: var(--button-hover);
    }
    button.clicked {
        animation: clickVibe 0.2s ease;
    }
    @keyframes clickVibe {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(0.95); }
    }
    .result {
        margin-top: 15px;
        font-size: 18px;
        font-weight: bold;
        color: var(--text-color);
    }
    .footer {
        margin-top: 20px;
        font-size: 12px;
        color: var(--footer-color);
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
    <input id="user_input" placeholder="Например: abc123" required>
    <div class="error-message" id="error_msg">Допустимы только латинские буквы и цифры без пробелов</div>
    <button id="calc_btn" type="button">Рассчитать</button>
    <div class="result" id="result"></div>
    <div class="footer">
        created by <a href="https://instagram.com/araiym.live" target="_blank">@araiym.live</a>
    </div>
</div>

<script>
document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("user_input");
    const btn = document.getElementById("calc_btn");
    const resultBlock = document.getElementById("result");
    const errorMsg = document.getElementById("error_msg");
    const themeToggle = document.querySelector(".theme-toggle");

    // Переключение темы
    themeToggle.addEventListener("click", () => {
        document.body.classList.toggle("dark");
        themeToggle.textContent = document.body.classList.contains("dark") ? "☀️" : "🌙";
    });

    // Обработка клика
    btn.addEventListener("click", () => {
        btn.classList.add("clicked");
        setTimeout(() => btn.classList.remove("clicked"), 200);

        const value = input.value.trim();
        const pattern = /^[A-Za-z0-9]+$/;

        if (!pattern.test(value)) {
            input.classList.add("error");
            errorMsg.style.display = "block";
            resultBlock.textContent = "";
            return;
        } else {
            input.classList.remove("error");
            errorMsg.style.display = "none";
        }

        fetch("/calculate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: value })
        })
        .then(res => res.json())
        .then(data => {
            resultBlock.textContent = "Сумма: " + data.result;
        });
    });
});
</script>
</body>
</html>
"""

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, ''),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    text = data.get("text", "")
    return jsonify({"result": calculate_sum(text)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
