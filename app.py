import os
from flask import Flask, render_template, request, jsonify
from groq import Groq
import json

app = Flask(__name__)
client = Groq(api_key="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")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    try:
        data = request.json
        t11 = data.get('task11', '')
        t12 = data.get('task12', '')
        t2 = data.get('task2', '')

        prompt = f"""
        Analyze these CEFR writing tasks for Hojiakbar. 
        Task 1.1: {t11}
        Task 1.2: {t12}
        Task 2: {t2}

        IMPORTANT: You must return ONLY a JSON object with exactly these keys:
        "total_score": (a number between 10 and 50),
        "feedback": "your detailed feedback here"
        """
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "You are a CEFR examiner that only outputs JSON."},
                      {"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        # AI javobini qabul qilamiz
        ai_response = json.loads(completion.choices[0].message.content)
        return jsonify(ai_response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
