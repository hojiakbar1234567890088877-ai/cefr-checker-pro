import os
from flask import Flask, render_template, request, jsonify
from groq import Groq
import json

app = Flask(__name__)

# API kalitini to'g'ridan-to'g'ri shu yerga yozamiz
client = Groq(api_key="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")

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

        prompt = f"""
        You are an official CEFR Examiner.
        Student Name: {name}
        
        Evaluate these three tasks:
        Task 1.1: {t11}
        Task 1.2: {t12}
        Task 2: {t2}

        Return ONLY a JSON object:
        {{
            "total_score": (a number between 0 and 50),
            "feedback": "Write a helpful feedback in Uzbek language here."
        }}
        """
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "You are a CEFR grading expert. Always output valid JSON."},
                      {"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        # AI dan kelgan javobni qaytaramiz
        return completion.choices[0].message.content
    except Exception as e:
        return jsonify({"total_score": 0, "feedback": f"Server xatosi: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
