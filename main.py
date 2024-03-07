from flask import Flask, render_template, request, redirect, url_for, jsonify
from database_connection import cursor, database
from email.mime.text import MIMEText
import smtplib
import random
import string

app = Flask(__name__)


# main
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
    account = cursor.fetchone()

    if account:
        return redirect(url_for('main_page'))
    else:
        return redirect(url_for('wrong_password'))


# If account is true, main page
@app.route('/main_page')
def main_page():
    return render_template('/main_page.html')


# if user or pass is wrong
@app.route('/wrong_password')
def wrong_password():
    return 'Wrong password'

# render ng forgot password page
@app.route('/forgot_password')
def forgot_password():
    return render_template('/forgot_password.html')


########################## FORGOT PASSWORD CODE ##############################
def email_exists(email):
    cursor.execute('SELECT COUNT(*) FROM accounts WHERE email = %s', (email,))
    count = cursor.fetchone()[0]
    return count > 0


def generate_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))


# Function para sa send email
def send_email(email, password):
    sender_email = "j.vincentd35@gmail.com"
    receiver_email = email
    password = password

    message = MIMEText(f"Your new password is: {password}")
    message['Subject'] = 'New Password'
    message['From'] = sender_email
    message['To'] = receiver_email

    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login(sender_email, 'cwiz glux jidz mrpv')
    smtp_server.sendmail(sender_email, receiver_email, message.as_string())
    smtp_server.quit()


# Send email button sa forgot_password.html
@app.route('/forg_pw', methods=['POST'])
def send_to_email():
    email = request.form['email']
    if email_exists(email):
        new_password = generate_password()
        send_email(email, new_password)

        # Update pass
        cursor.execute('UPDATE accounts SET password = %s WHERE email = %s', (new_password, email))
        database.commit()

        return redirect(url_for('redirect_to_success_page'))
    else:
        return redirect(url_for('unsuccessful_send'))


######################## SUCCESS_SEND.HTML PAGE ####################$########


@app.route('/redirect_to_success_page')
def redirect_to_success_page():
    return render_template('/success_send.html')


######################## UNSUCCESSFUL_SEND PAGE ##########$##################


@app.route('/unsuccessful_send')
def unsuccessful_send():
    return render_template('/unsuccessful_send.html')


############################ RETURN TO MAIN #################################


@app.route('/back-to-index', methods=['POST'])
def back_to_login():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
    