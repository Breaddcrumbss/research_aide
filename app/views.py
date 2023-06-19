from django.shortcuts import render
from .forms import SearchForm
from .utils import classify
import openai 
from dotenv import dotenv_values
import argparse
from django.http import HttpResponse
from django.views import View
import json
from django.http import JsonResponse

config = dotenv_values(".env")
openai.api_key = config.get("OPENAI_API_KEY")

# Create your views here.
def index(request):
    return render(request, 'app/index.html', {
                    
    })

def search(request):
    if request.method == "POST":
        form = SearchForm(data=request.POST)
        if form.is_valid():
            tag = classify(request.POST.get('input'))       # Pass tag into the function to find cases
            return render(request, 'app/search.html', {
                'cases': tag,       # To change to cases
                'search': False
            })

    else:
        form = SearchForm()

        return render(request, 'app/search.html', {
            'form':form,
            'search': True
        })
        
        

# def chatbot(request):
#     chatbot_response = None 
#     initial_prompt = "You are a lawyer. Your personality is professional and logical."
    
    
#     if request.method == "POST":
#         user_input = request.POST.get("user_input")
#         prompt = user_input 
        
#         response = openai.Completion.create(
#             engine= 'text-davinci-003',
#             prompt = prompt,
#             max_tokens = 256,
#             temperature=0.5
#         )
#         print(response)
        
#         chatbot_response = response["choices"][0]["text"]
#     return render(request, 'app/chatbot.html', {"chatbot_response": chatbot_response})

initial_prompt = "You are a lawyer. Your personality is professional and logical."
initial_message = {"role": "system", "content": initial_prompt}
messages = [{"role": "system", "content": initial_prompt}]
output = []

def refresh(request):
    messages.clear()
    messages.append(initial_message)
    output.clear()
    return HttpResponse("Refresh")

def chatbot(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        user_input = body["user_input"]

        print("first append")
        messages.append({"role": "user", "content": user_input})
        output.append({"User" : f"{user_input}"})
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages, 
            temperature=0.5
        )
        print(res)
        
        print("second append")
        messages.append(res["choices"][0]["message"].to_dict())
        output.append({"Assistant":  f"{res['choices'][0]['message']['content']}"})
        print(output)
        return JsonResponse({"data": output})

    return render(request, 'app/chatbot.html', {"messages": output})

def response(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    user_input = body["user_input"]

    messages.append({"role": "user", "content": user_input})
    output.append(f"User : {user_input}")
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages, 
        temperature=0.5
    )
    messages.append(res["choices"][0]["message"].to_dict())
    output.append(f"Assistant: {res['choices'][0]['message']['content']}")
    print(messages)
    print(output)
        
    chatbot_response = res["choices"][0]["message"]
    
    return HttpResponse(chatbot_response)


