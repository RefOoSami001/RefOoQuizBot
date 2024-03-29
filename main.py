import requests
import re
import telebot
from keep_alive import keep_alive

bot = telebot.TeleBot("6982141096:AAFpEspslCkO0KWNbONnmWjUU_87jib__g8")
def parse_data(data):
    organized_data = {}

    # Extracting questions and correct answers using regular expressions
    questions = re.findall(r"### (\d+)\. (.+?)(?=\n[a-d]\.|\n\n)", data, re.DOTALL)
    correct_answers = re.findall(r"\d+\.\s([a-d])", data)

    # Extracting options for each question separately
    options_pattern = r"([a-d])\. (.+?)(?=\n[a-d]\.|\n\n)"
    options_matches = re.findall(options_pattern, data, re.DOTALL)

    # Creating the dictionary
    for i, (question_number, question_text) in enumerate(questions):
        question_data = {}
        question_data["question"] = question_text.strip()
        question_data["answers"] = [match[1].strip() for match in options_matches[i * 4: (i + 1) * 4]]
        # Get index of correct answer in the list of answers
        correct_answer_index = ord(correct_answers[i]) - ord('a')
        question_data["correct_answer"] = correct_answer_index
        organized_data[f"Question {question_number}"] = question_data

    return organized_data

def send_user_details(chat_id, user):
    user_details = f"New user started ChatBot:\n\nUsername: @{user.username}\nFirst Name: {user.first_name}\nLast Name: {user.last_name}\nUser ID: {user.id}"
    bot.send_message(chat_id, user_details)

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row_width = 2  # Set row width to 2 for two buttons in each row
    markup.add(telebot.types.InlineKeyboardButton("أنشاء اختبار🫣", callback_data="start_quiz"),
                telebot.types.InlineKeyboardButton("تواصل📞", url="https://t.me/RefOoSami"))
    bot.send_message(message.chat.id, "اهلا بيك\ي👋😍\nاضغط/ي علي 'انشاء اختبار' للبدء😋", reply_markup=markup)
    send_user_details(854578633, message.from_user)
@bot.callback_query_handler(func=lambda call: call.data == "start_quiz")
def start_quiz(call):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, "برجاء ارسال موضوع المحاضرة في رسالة🤖")
    bot.register_next_step_handler(call.message, get_topic)

def get_topic(message):
    topic = message.text
    bot.send_message(message.chat.id, "ارسل/ي عدد الاسئلة المطلوبة😊")
    bot.register_next_step_handler(message, lambda msg: get_num_questions(msg, topic))

def arabic_to_unicode(text):
    unicode_text = ""
    for char in text:
        if char.isdigit():
            # Convert Arabic numeral to Unicode character
            unicode_text += chr(int(char) + 1632)
        else:
            unicode_text += char
    return unicode_text

def get_num_questions(message, topic):
    try:
        unicode_text = arabic_to_unicode(message.text)
        num_questions = int(unicode_text)
        if num_questions > 0:
            if num_questions >= 3:
                send_quiz(message, topic, num_questions)
            else:
                bot.send_message(message.chat.id, "الحد الادني هو 3😢")
                get_topic(message)
        else:
            bot.send_message(message.chat.id, "لا يمكنك ادخال عدد بالسالب😒")
            get_topic(message)
    except (TypeError, ValueError):
        bot.send_message(message.chat.id, "Please enter a valid number.")
        get_topic(message)

    
def send_quiz(message, topic, num_questions):
    # Send the wait message and GIF
    wait_message = bot.send_message(message.chat.id, "برجاء الانتظار...\nجاري معالجة البيانات🫣")
    # Make the request to fetch the questions and answers
    s = requests.Session()
    headers = {
        'authority': 'auth.magicschool.ai',
        'accept': '*/*',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRudXB6eGZqcnVrc3VsdmZ5YW5sIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODIwNTIzNzIsImV4cCI6MTk5NzYyODM3Mn0.NxmabzXOOYo4zMqwJpEtNDewILVImuIxWZSPIuRaE2o',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://app.magicschool.ai',
        'referer': 'https://app.magicschool.ai/',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'x-client-info': 'supabase-js-web/2.38.4',
    }

    params = {
        'grant_type': 'password',
    }

    json_data = {
        'email': 'raafatsami101@gmail.com',
        'password': 'Ref@osami826491375',
        'gotrue_meta_security': {},
    }

    response = s.post('https://auth.magicschool.ai/auth/v1/token', params=params, headers=headers, json=json_data)
    headers = {
        'authority': 'app.magicschool.ai',
        'accept': '*/*',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': 'Bearer ' + response.cookies['sb-access-token'],
        'content-type': 'application/json',
        'origin': 'https://app.magicschool.ai',
        'referer': 'https://app.magicschool.ai/tools/mc-assessment',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

    json_data = {
        'id': 'mc-assessment',
        'gradeLevel': 'university',
        'numQuestions': str(num_questions),
        'topic': topic,
        'locale': 'en-us',
        'role': 'teacher',
    }

    response = s.post('https://app.magicschool.ai/api/generations',headers=headers, json=json_data)
    data = response.text
    parsed_data = parse_data(data)
    
    bot.delete_message(message.chat.id, wait_message.message_id)

    # Send each question as a poll
    for question_number, question_data in parsed_data.items():
        # Prepare the poll options
        options = [f"{chr(97 + i)}. {option}" for i, option in enumerate(question_data["answers"])]
        # Check the length of options before sending the poll
        if any(len(option) > 100 for option in options):
            # Skip invalid poll
            continue
        # Send the poll
        bot.send_poll(
            chat_id=message.chat.id,
            question=question_data["question"],
            options=options,
            is_anonymous=False,  # To show poll results to users
            type="quiz",  # Set poll type to quiz
            correct_option_id=question_data["correct_answer"],  # Set the correct answer index
            open_period=0,  # To disable the "open for" duration

        )
    send_user_details(854578633, message.from_user)
@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    start(message)

if __name__ == "__main__":
    while True:
        try:
            keep_alive()
            bot.polling()
        except:
            pass
