import openai
import tiktoken
from utilities.helper import LLMHelper
import time
class openAI_helper:

    LLMHelper = LLMHelper()
    def get_chatgpt_answer(self, question, history):
        
        user_message = {"role":"user", "content":question}

        # messages.append(user_message)
        # 히스토리 데이터 이전 20개만 보냄
        response = openai.ChatCompletion.create(
            model="gpt-35-turbo",
            engine= 'gpt35test', 
            messages=history[-12:]+[user_message]
        )
        
        reply = response.choices[0].message.content

        return user_message, {"role": "assistant", "content": reply}
        # extract_chain = LLMChain(llm=self.llm, prompt=EXTRACT_SUB_PROMPT, verbose=True)
        # result = extract_chain({"question": question, "history": history})

        # subs_info = result['text'].replace(' ','').split(',')
        # result['answer'] = dict([(subs_info[0].split(':')[0],subs_info[0].split(':')[1]),
        #                          ( subs_info[1].split(':')[0],subs_info[1].split(':')[1]  )   ])        
        # return question, result['answer']
        

        
    def get_encoder(model):
        if model == "text-search-davinci-doc-001":
            return tiktoken.get_encoding("p50k_base")
        elif model == "text-embedding-ada-002":
            return tiktoken.get_encoding("cl100k_base")
        elif model == "gpt-35-turbo": 
            return tiktoken.get_encoding("cl100k_base")
        elif model == "gpt-4-32k":
            return tiktoken.get_encoding("cl100k_base")
        elif model == "gpt-4":
            return tiktoken.get_encoding("cl100k_base")                
        elif model == "text-davinci-003":
            return tiktoken.get_encoding("p50k_base")       
        else:
            return tiktoken.get_encoding("gpt2")
        

    def get_model_max_tokens(model):
        if model == "text-search-davinci-doc-001":
            return 2047
        elif model == "text-search-davinci-query-001":
            return 2047      
        elif model == "text-davinci-003":
            return 4000        
        elif model == "text-embedding-ada-002":
            return 4095
        elif model == "gpt-35-turbo":
            return 8193       
        elif model == "gpt-4-32k":
            return 32768    
        elif model == "gpt-4":
            return 8192             
        else:
            return 4095


    def get_encoding_name(model):
        if model == "text-search-davinci-doc-001":
            return "p50k_base"
        elif model == "text-embedding-ada-002":
            return "cl100k_base"
        elif model == "gpt-35-turbo": 
            return "cl100k_base"
        elif model == "gpt-4-32k":
            return "cl100k_base"
        elif model == "gpt-4":
            return "cl100k_base"               
        elif model == "text-davinci-003":
            return "p50k_base"  
        else:
            return "gpt2"        
            
    def openai_summarize(text, completion_model, max_output_tokens = LLMHelper.max_output_token , lang='en'):
        prompt = get_summ_prompt(text)
        return contact_openai(prompt, completion_model, max_output_tokens)        
    
    def get_summ_prompt(text):

        prompt = f"""
        Summarize the following text.

        Text:
        ###
        {text}
        ###

        Summary:
        """

        return prompt

    def contact_openai(prompt, completion_model = LLMHelper.comp_model, max_output_tokens = LLMHelper.max_output_token , stream = False, verbose = True):
        if verbose: print("\n########################### Calling OAI Completion API - start call")

        #gen = get_generation(completion_model)
        gen = 3.5
        try:
            b = time.time()

            if (gen == 4) or (gen == 3.5):
                openai.api_version = "2023-03-15-preview"

                if not isinstance(prompt, list):
                    prompt = [{'role':'user', 'content': prompt}]
        
                resp = openai.ChatCompletion.create(
                        messages=prompt,
                        temperature=0.7,                        
                        model="gpt-35-turbo",
                     #   max_tokens=max_output_tokens,
                        engine='gpt35test',
                        stream = False
                    )
                a = time.time()
                if verbose: print(f"Using GPT-4 - Chat Completion - with stream {stream} - OpenAI response time: {a-b}")   
                if stream: return resp
                #else: return resp["choices"][0]["message"]['content'].strip(" \n")
                else: return resp.choices[0].message.content

            else:
  
                openai.api_version = "2023-03-15-preview"
                resp = openai.Completion.create(
                                prompt=prompt,
                                temperature=LLMHelper.temperature,
                                max_tokens=max_output_tokens,
                                model=LLMHelper.comp_model,
                                deployment_id=LLMHelper.deployment_name,
                                stream = stream
                            )

                a = time.time()
                if verbose: print(f"Using GPT-3 - Chat Completion - with stream {stream} - OpenAI response time: {a-b}")                         
                if stream: return resp
                else: return resp["choices"][0]["text"].strip(" \n")

        except Exception as e:
            # logging.warning(f"Error in contact_openai: {e}")
            print(e)
            raise e

    
