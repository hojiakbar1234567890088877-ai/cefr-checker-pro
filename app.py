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
        t11 = data.get('task11', '').strip()
        t12 = data.get('task12', '').strip()
        t2 = data.get('task2', '').strip()

        # Agar hamma joy bo'sh bo'lsa
        if len(t11) < 10 and len(t12) < 10 and len(t2) < 10:
            return jsonify({"total_score": 0, "feedback": "Hech qanday matn kiritilmadi yoki matn juda qisqa."})

        prompt = f"""
        You are a strict CEFR Examiner. Evaluate Hojiakbar's writing.
        Criteria:
        - If the text is gibberish, random letters, or unrelated to the topic, give a score of 0-5.
        - Evaluate Task 1.1: {t11}
        - Evaluate Task 1.2: {t12}
        - Evaluate Task 2: {t2}

        Return ONLY a JSON object:
        {{
            "total_score": (number from 0 to 50),
            "feedback": "Detailed explanation of the score"
        }}
        """
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "You are a precise CEFR grading bot. Output only JSON."},
                      {"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(completion.choices[0].message.content)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
