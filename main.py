from flask import Flask, request

app = Flask(__name__)

def parse_matrix(matrix_str):
    return [[int(x) for x in row.split(',')] for row in matrix_str.strip().split('\n')]

def multiply_matrices(A, B):
    result = []
    for i in range(len(A)):
        result_row = []
        for j in range(len(B[0])):
            sum = 0
            for k in range(len(A[0])):
                sum += A[i][k] * B[k][j]
            result_row.append(sum)
        result.append(result_row)
    return result

@app.route('/')
def index():
    return '''
    <html>
    <head>
        <title>Matrix Multiplier</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                background-color: white;
                padding: 30px 40px;
                border-radius: 12px;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
                text-align: center;
                width: 400px;
            }
            textarea {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border-radius: 6px;
                border: 1px solid #ccc;
                font-family: monospace;
            }
            input[type="submit"] {
                background-color: #007bff;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 16px;
            }
            input[type="submit"]:hover {
                background-color: #0056b3;
            }
            h2 {
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Matrix Multiplication</h2>
            <form action="/multiply" method="post">
                <label><strong>Matrix A (comma-separated rows):</strong></label><br>
                <textarea name="matrix_a" rows="4">1,2\n3,4</textarea><br>
                <label><strong>Matrix B (comma-separated rows):</strong></label><br>
                <textarea name="matrix_b" rows="4">5,6\n7,8</textarea><br>
                <input type="submit" value="Multiply">
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/multiply', methods=['POST'])
def multiply():
    try:
        matrix_a = parse_matrix(request.form['matrix_a'])
        matrix_b = parse_matrix(request.form['matrix_b'])

        if len(matrix_a[0]) != len(matrix_b):
            return "<p style='color:red; text-align:center;'>Matrix A columns must equal Matrix B rows.<br><a href='/'>Try Again</a></p>"

        result = multiply_matrices(matrix_a, matrix_b)
        result_str = '<br>'.join(['[' + ', '.join(map(str, row)) + ']' for row in result])

        return f'''
        <html>
        <head>
            <title>Result</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    text-align: center;
                    padding-top: 100px;
                    background-color: #f4f4f4;
                }}
                .result {{
                    display: inline-block;
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
                }}
                a {{
                    display: inline-block;
                    margin-top: 20px;
                    color: #007bff;
                    text-decoration: none;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            <div class="result">
                <h3>Multiplication Result:</h3>
                <p>{result_str}</p>
                <a href="/">Try another</a>
            </div>
        </body>
        </html>
        '''
    except Exception as e:
        return f"<p style='color:red; text-align:center;'>Error: {e}<br><a href='/'>Go Back</a></p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
