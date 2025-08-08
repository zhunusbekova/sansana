HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Калькулятор Сюцай</title>
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
            max-width: 100%;
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
    </div>
</body>
</html>
"""
