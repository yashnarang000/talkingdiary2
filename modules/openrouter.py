from openai import OpenAI
import copy

class History:
    def __init__(self):
        self._data = []
    
    def fork(self):
        forked = History()
        forked._data = copy.deepcopy(self._data)
        return forked

    def pretend_save(self, role, content):
        temp_history = copy.deepcopy(self._data)

        if role in ["user", "system", "assistant"]:
            temp_history.append(
                {
                    "role":role,
                    "content":content
                }
            )

            return temp_history
        
        else:
            return None
    
    def save(self, role, content):
        if role not in ["user", "system", "assistant"]:
            return None
        
        self._data.append(
            {
                "role":role,
                "content":content
            }
        )
        
    def dump(self):
        return copy.deepcopy(self._data)
        
    def __str__(self):
        return f"<OPENROUTER::{self.__class__.__name__.upper()}>"
    
    def __repr__(self):
        return f"<OPENROUTER::{self.__class__.__name__.upper()}>"
    
class Response:
    def __init__(self, origin_prompt, response_text, read_from, save_to):
        self.__prompt = origin_prompt
        self.__response_text = response_text
        self.__read_from = read_from
        self.__save_to = save_to

    @property
    def content(self):
        return self.__response_text
    
    @property
    def origin(self):
        return self.__prompt
    
    @property
    def read_from(self):
        return self.__read_from
    
    @property
    def save_to(self):
        return self.__save_to
    
    def __str__(self):
        return f"<OPENROUTER::{self.__class__.__name__.upper()}>"

    def __repr__(self):
        return f"<OPENROUTER::{self.__class__.__name__.upper()}>"
    
# History and Response classes are made to encapsulate their content.
    
class Chatbot:
    def __init__(self, API_KEY, model):
        self.__API = API_KEY

        self.model = model

        self.__client = OpenAI(base_url="https://openrouter.ai/api/v1",
                               api_key=self.__API)
        


    def response(self, prompt, read_from=None, save_to=None, model=None):
        if model==None: model = self.model

        if read_from is None:
            read_from = History()


        completion = self.__client.chat.completions.create(
            model = model,
            extra_body={},
            messages = read_from.pretend_save("user", prompt)
        )

        response_text = completion.choices[0].message.content

        if save_to is not None:
            save_to.save("user", prompt)
            save_to.save("assistant", response_text)

        return Response(prompt, response_text, read_from, save_to)

    def instruct(self, instruction, save_to):
        save_to.save(role="system", content=instruction)

    def __str__(self):
        return f"<OPENROUTER::{self.__class__.__name__.upper()}>"
    
    def __repr__(self):
        return f"<OPENROUTER::{self.__class__.__name__.upper()}>"