import os
from flask import Flask, render_template, request, jsonify
from groq import Groq
import json

app = Flask(__name__)

# YANGI VA TEKSHIRILGAN API KALITI:
# Bu kalitni hech qanday bo'shliqlarsiz (space) qo'ying
client = Groq(api_key="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") 
# DIQQAT: Agar bu kalit ham ishlamasa, o'zingizning Groq.com dagi 
# shaxsiy kalitingizni (gsk_...) ko'chirib (copy) kelib shu yerga qo'ying.

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    try:
        data = request.json
        t11 = data.get('task11', '').strip()
        t12 = data.get('task12', '').strip()
        t2 = data.get('task2', '').strip()
        name = data.get('fullName', 'Student')

        prompt = f"""Evaluate CEFR writing for {name}. 
        Task 1.1: {t11}
        Task 1.2: {t12}
        Task 2: {t2}
        Return ONLY JSON: {{"total_score": (number), "feedback": "string"}}"""
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        return completion.choices[0].message.content
    except Exception as e:
        # Xatolikni aniqroq ko'rish uchun:
        return jsonify({"total_score": 0, "feedback": f"Tizim xatosi: {str(e)}"}), 401
