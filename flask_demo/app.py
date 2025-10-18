import pandas as pd
from flask import Flask, request

import model

app = Flask(__name__)


# http://localhost:5000/
@app.route("/")
def my_first_function():
    return "<h1>Hello Flask!</h1>"

# http://127.0.0.1:5000/greet/<your_name>
@app.route("/greet/<your_name>")
def greet(your_name):
    return f"<h1>Hello {your_name}!</h1>"

# http://127.0.0.1:5000/two_sum/<x>/<y>
@app.route("/two_sum/<x>/<y>")
def two_sum(x, y):
    return str(int(x) + int(y))

# http://127.0.0.1:5000/two_sum_2/<int:x>/<int:y>
@app.route("/two_sum_2/<int:x>/<int:y>")
def two_sum_2(x, y):
    return str(x + y)

# [GET] http://127.0.0.1:5000/api/v2/get_emp_info/<str:bu_id>/<int:emp_id>

# http://127.0.0.1:5000/hello_get?name=Allen&age=22
@app.route("/hello_get")
def hello_get():
    name = request.args.get("name")
    age = request.args.get("age")

    if not name:
        return "What is your name?"
    if not age:
        return f"Hello {name}."

    return f"Hello {name}, your are {age} years old."

@app.route("/hello_post", methods=["GET", "POST"])
def hello_post():
    form_html = """
    <form method="POST">
        <input name="username">
        <button>SUBMIT</button>
    </form>
    """
    if request.method == "POST":
        username = request.form.get("username")
        form_html += f"""
        <h3>Hello {username}</h3>
        """

    return form_html

@app.route('/show_staff')
def hello_google():
    staff_data = model.getStaff()
    column = ['ID', 'Name', 'DeptId', 'Age', 'Gender', 'Salary']
    return pd.DataFrame(
        data=staff_data,
        columns=column,
    ).to_json()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
