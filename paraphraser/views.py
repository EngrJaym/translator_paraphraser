from django.shortcuts import render
from django.http import JsonResponse
from transformers import pipeline
import json
import re

paraphraser = pipeline("text2text-generation", model="google/flan-t5-large")

def showParaphraser(request):
    return render(request, 'index.html')


def paraphrase_text(text, min_length):
    paraphrased = paraphraser(text, min_length = min_length, max_length=1000, do_sample=True, repetition_penalty=2.0, temperature=0.8)
    print(paraphrased)
    return paraphrased[0]['generated_text']


def paraphrase_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            input_text = data.get("text", "").strip()
            summary_length = data.get("summary_length", "medium")
            word_count = len(input_text.split())

            if word_count < 30:
                return JsonResponse({"summary": "Minimum number of input text to be summarized is 30."})
            
            else:
                length_map = {"short": round(word_count/6), "medium": round(word_count/2), "detailed": round(word_count/0.8)}
                desired_word_count = length_map.get(summary_length, 100)
                print(word_count, desired_word_count)
                if not input_text:
                    return JsonResponse({"error": "Please enter some text to summarize."}, status=400)

                stripped_input_text = re.sub(r'\s+', ' ', input_text).strip()

                paraphrased_text = paraphrase_text(stripped_input_text, desired_word_count)

                return JsonResponse({"summary": paraphrased_text})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON request"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

def translate_text(text, translation):
    translator = pipeline("translation", model=f"Helsinki-NLP/opus-mt-{translation}")
    return translator(text)[0]['translation_text']
    

def translate_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            input_text = data.get("text", "").strip()
            translation = data.get("translation", "")
            print(input_text, translation)
            translated_text = translate_text(input_text, translation)

            return JsonResponse({"translation": translated_text})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON request"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)   
