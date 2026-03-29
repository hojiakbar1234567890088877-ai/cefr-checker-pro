import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# Groq API kalitingiz
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

        # AI uchun batafsil instruksiya (Prompt)
        prompt = f"""
        You are an expert CEFR examiner. 
        Analyze these three writing tasks for a student named Hojiakbar:
        
        1. Task 1.1 (Letter/Graph): {t11}
        2. Task 1.2 (Report/Email): {t12}
        3. Task 2 (Essay): {t2}
        
        Please provide:
        - An overall CEFR Level (e.g., B2 or C1).
        - Specific feedback for each task.
        - Grammar and Vocabulary score (1-9 scale).
        - One key tip for improvement.
        
        Keep the feedback professional and encouraging.
        """
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful and precise CEFR writing tutor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        result = completion.choices[0].message.content
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
