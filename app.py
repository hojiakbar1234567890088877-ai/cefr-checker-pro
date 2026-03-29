import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# Sizning Groq API kalitingiz
client = Groq(api_key="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")

@app.route('/')
def home():
    # Bu funksiya templates papkasidagi index.html ni ochadi
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    try:
        data = request.json
        t1 = data.get('task1', '')
        t2 = data.get('task2', '')

        prompt = f"""
        You are a professional CEFR examiner. 
        Evaluate the following writing tasks:
        Task 1: {t1}
        Task 2: {t2}
        
        Provide a detailed CEFR band score and feedback for each.
        """
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify({'result': completion.choices[0].message.content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
