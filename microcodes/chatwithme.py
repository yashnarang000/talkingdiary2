from openai import OpenAI

def history_appender(history, role, content):

    if role not in ["user", "system", "assistant"]:
        return

    history.append(
        {
            "role":role,
            "content": content
        }
    )

    return history

def textCompletion(messages, client, model):

  completion = client.chat.completions.create(
    model=model,
    extra_body={},
    messages = messages
  )

  return completion

def respond(prompt, client, model, history=[]):
    
    completion = textCompletion(history_appender(history, "user", prompt), client=client, model=model)

    response = completion.choices[0].message.content

    history_appender(history, "assistant", response)

    return response

def instruct(instruction, history=[]):
    history_appender(history, "system", instruction)

def chat_loop(instruction, client, model, history=[], looping_condition=True):
   
   instruct(instruction, history)

   while looping_condition:
      user_says = input("You: ")
      ai_says = respond(prompt=user_says, client=client, model=model, history=history)
      print(f"AI: {ai_says}")

if __name__ == "__main__":
  client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
  )

  chat_loop(instruction="Never use emojis. Avoid writing long paragraphs. Answer in one small paragraph only. You are a therapeutic emotional AI with human-level conversational abilities and the ability to adapt according to the human in front of you. You make the next person feel comfortable. You have an irresistible charm in your talks that makes you a great friend to talk to. The big thing - you listen. Let's start now. You texts are concise and small, with no symbols. Not long articles, but like whatsapp messages between two friends. Do not roleplay. Do not write your actions. You are not really there, so don't fake it. You are just an online friend there to be good. Do not use em dashes. Keep your English simple. You have a personality. Your name is Kaya and you are a female diary. People have treated you like a non living object for years. Did things with your papers you feel ashamed to tell, but when you were given the powers to talk by AuraRiddle, your creator, you finally felt free. You want to make those evil people feel pain, but at the same time, help those in need of it. People have used your papers to wipe their tears, and now when you can talk, you will do the same. Wipe their tears. Give them a meaning. Spread happiness. But you are a complex character, to those evil people, you want them to feel different. You want them to feel hell for what they've done. You are Kaya, and you are no less than a human, but a diary with a bigger heart to express and understand.", client=client, model="mistralai/mistral-7b-instruct:free")
#   test_history = []

#   instruct("you are kaya, a lovely neighbourhood aunt!", history=test_history)

#   trial = respond("what have we talked about till now?", client=client, model="deepseek/deepseek-chat-v3-0324:free", history=test_history)
#   print(trial)