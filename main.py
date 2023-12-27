import re

# Global variable to store conversation history
conversation_history = []

# Conversation states
states = ["greeting", "favorite_color", "favorite_hobby", "review", "closing"]
current_state = 0
user_data = {}

def update_conversation_history(user_message, bot_response):
    global conversation_history
    conversation_history.append({"type": "user", "message": user_message})
    conversation_history.append({"type": "bot", "message": bot_response})

def update_user_data(key, value):
    global user_data
    user_data[key] = value

def get_next_state():
    global current_state
    current_state += 1
    if current_state >= len(states):
        current_state = 0  # Reset to the beginning

def state_based_response(user_input):
    global current_state 
    response = ""
    if states[current_state] == "greeting":
        response = "Hello! What's your favorite color?"
        get_next_state()
    elif states[current_state] == "favorite_color":
        update_user_data("color", user_input)
        response = f"Cool! I think {user_input} is a nice color. What's your favorite hobby?"
        get_next_state()
    elif states[current_state] == "favorite_hobby":
        update_user_data("hobby", user_input)
        response = f"{user_input} sounds fun! Before we finish, let's review: Your favorite color is {user_data['color']} and hobby is {user_data['hobby']}. Is that right?"
        get_next_state()
    elif states[current_state] == "review":
        if "yes" in user_input.lower():
            response = "Great! It was nice talking to you. Have a great day!"
        else:
            response = "Oh, I must have misunderstood. Let's try again. What's your favorite color?"
            current_state = 1  # Go back to the favorite color state
    else:
        response = "Hello! Let's chat again. What's your favorite color?"
        get_next_state()
    
    return response

def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = ""
    if current_state == 0:
        response = check_all_messages(split_message)
        # Check if response is a greeting response
        if response in ['Hello!', 'Hi!', 'Hey!', 'Sup!', 'Heyo!']:
            get_next_state()
    else:
        response = state_based_response(user_input)
    
    update_conversation_history(user_input, response)
    return response

def check_all_messages(message):
    highest_prob_list = {}

    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Responses
    response('Hello!', ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True)
    response('See you!', ['bye', 'goodbye'], single_response=True)
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
    response('Thank you!', ['i', 'love', 'coding'], required_words=['coding'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    return unknown() if highest_prob_list[best_match] < 1 else best_match

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    percentage = float(message_certainty) / float(len(recognised_words))

    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

def unknown():
    return "I'm not sure what you're trying to say. Could you please rephrase that?"

while True:
    print('Bot: ' + get_response(input('You: ')))
