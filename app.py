from flask import Flask, redirect, url_for, render_template, request
from functions import initialize_conversation, get_chat_model_completions, moderation_check,required_properties_populated_confirmation_layer,dictionary_present, generate_python_script

app = Flask(__name__)

conversation_bot = []
conversation = initialize_conversation()
introduction = get_chat_model_completions(conversation)
conversation_bot.append({'bot':introduction})
python_script = ""


@app.route("/")
def default_func():
    global conversation_bot, conversation, python_script
    return render_template("chatbot.html", name_xyz = conversation_bot)

@app.route("/end_conv", methods = ['POST','GET'])
def end_conv():
    global conversation_bot, conversation, python_script
    conversation_bot = []
    conversation = initialize_conversation()
    introduction = get_chat_model_completions(conversation)
    conversation_bot.append({'bot':introduction})
    return redirect(url_for('default_func'))

@app.route("/codegen", methods = ['POST'])
def code_gen():
    global conversation_bot, conversation, python_script
    user_input = request.form["user_input_message"]
    prompt = 'Remember your system message and that you are an NSX Config Generator AI assistant. So, you only help with questions around NSX.'
    moderation = moderation_check(user_input)
    if moderation == 'Flagged':
        return redirect(url_for('end_conv'))

    if python_script == "":
        conversation.append({"role": "user", "content": user_input + prompt})
        conversation_bot.append({'user':user_input})

        response_assistant = get_chat_model_completions(conversation)

        moderation = moderation_check(response_assistant)
        if moderation == 'Flagged':
            return redirect(url_for('end_conv'))

        confirmation = required_properties_populated_confirmation_layer(response_assistant)
        print(confirmation)

        moderation = moderation_check(confirmation)
        if moderation == 'Flagged':
            return redirect(url_for('end_conv'))

        if "No" in confirmation:
            conversation.append({"role": "assistant", "content": response_assistant})
            conversation_bot.append({'bot':response_assistant})
        else:
            print(response_assistant)
            response = dictionary_present(response_assistant)

            moderation = moderation_check(response)
            if moderation == 'Flagged':
                return redirect(url_for('end_conv'))

            conversation_bot.append({'bot':"Thank you for providing all the information. Kindly wait, while I generate the python script: \n"})
            python_script = generate_python_script(response)

            conversation_bot.append({'bot':python_script})
            conversation_bot.append({'bot':"This is bot generated code. Please verify code with experts before executing"})

            print(python_script + '\n')
    return redirect(url_for('default_func'))

if __name__ == '__main__':
    app.run(debug=True, host= "0.0.0.0")