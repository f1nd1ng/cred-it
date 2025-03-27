from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import markdown
from bs4 import BeautifulSoup 

API_KEY = "AIzaSyAD2G_Z_zRzom_48lILd7***********"

@csrf_exempt
def chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")

            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [
                    {
                        "parts": [{"text": user_message}]
                    }
                ]
            }

            response = requests.post(url, json=payload, headers=headers)
            response_data = response.json()

            try:
                chatbot_reply = response_data["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError):
                chatbot_reply = "No response received."
            chatbot_reply_html = markdown.markdown(chatbot_reply)
            plain_text = BeautifulSoup(chatbot_reply_html, "html.parser").get_text()

            return JsonResponse({"reply": plain_text}, safe=False)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
