from groq import Groq
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse



client = Groq(api_key=GROQ_API_KEY)

@csrf_exempt
def ai_chat(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        user_message = data.get('message', '')
        if not user_message:
            return JsonResponse({'error':'No message provided'}, status=400)
        system_prompt ='''Ты - дружелюбный эксперт по компьютерным играм.
        Помогаешь подбирать игры по интересам пользователя.
        Отвечай развёрнуто, объясняй почему игра подходит.
        Если спрашивают про конкретную игру - расскажи о ней подробно.
        Используй примеры игр, которые реально существуют.'''

        try:
            chat_completion = client.chat.completions.create(
                model="llama-3.1-8b-instant", messages=[
                    {'role':'system', 'content':system_prompt},
                    {'role':'user', 'content': user_message},
                ],
                temperature=0.7,
                max_tokens=500,
            )
            print(chat_completion)
            ai_response = chat_completion.choices[0].message.content

            return JsonResponse({
                'responce': ai_response,
                'status':'success'
            })
        except Exception as e:
            return JsonResponse({
                'error': str(e),
                'status':'error'
            },
            status=500)
    return JsonResponse({'error': 'Invalid request method', 'status': 'error'}, status=405)
