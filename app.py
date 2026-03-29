import os
from flask import Flask, render_template, request, jsonify
from groq import Groq
import json

app = Flask(__name__)

# DIQQAT: Bu yerga Groq Cloud-dan olgan o'zingizning API kalitingizni qo'yishingiz SHART!
# Hozircha men misol tariqasida bitta kalit qo'ydim, lekin u bloklanishi mumkin.
# O'zingiznikini qo'ysangiz, 401 xatosi yo'qoladi.
API_KEY = "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" 
client = Groq(api_key=API_KEY)

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

        # AI-ga aniq topshiriq va so'zlar soni bo'yicha ko'rsatma beramiz
        prompt = f"""
        Evaluate the CEFR Writing performance for: {name}.
        
        STRICT LIMITS & RULES:
        1. Task 1.1 (Informal Letter): Target is ~50 words. Tone must be friendly.
        2. Task 1.2 (Formal Letter): Target is 120-150 words. Tone must be professional.
        3. Task 2 (Essay): Target is 180-200 words. Must have academic structure.
        
        STUDENT WORK:
        - Task 1.1: {t11}
        - Task 1.2: {t12}
        - Task 2: {t2}
        
        OUTPUT FORMAT:
        Return ONLY a JSON object:
        {{
            "total_score": (A number from 0 to 50 based on task achievement and word limits),
            "feedback": "Write detailed feedback in Uzbek. Mention if they hit the word counts."
        }}
        """
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a professional CEFR examiner. Always return valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        # AI-dan kelgan JSON javobni qaytaradi
        return completion.choices[0].message.content

    except Exception as e:
        # Xatolik bo'lsa, foydalanuvchiga aniq ko'rsatadi
        return jsonify({"total_score": 0, "feedback": f"API Xatosi: {str(e)}"}), 401

if __name__ == '__main__':
    app.run(debug=True)
