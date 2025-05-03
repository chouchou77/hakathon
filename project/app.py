from flask import Flask, request, jsonify
from flask_cors import CORS
from agent import analyze_and_create_pdf_tool, search_jobs_tool
import PyPDF2
import io

app = Flask(__name__)
CORS(app)  # هذا يسمح بالوصول من أي مصدر (يمكنك تقييده لاحقاً)

@app.route('/api/analyze-resume-pdf', methods=['POST'])
def analyze_resume_pdf():
    """
    API endpoint لتحليل السيرة الذاتية من ملف PDF وإنشاء PDF محسن
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'الرجاء إرفاق ملف PDF'}), 400
        
        file = request.files['file']
        if not file.filename.endswith('.pdf'):
            return jsonify({'error': 'الرجاء إرفاق ملف PDF صالح'}), 400
        
        # قراءة محتوى PDF
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        result = analyze_and_create_pdf_tool(text)
        return jsonify({'message': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-resume-text', methods=['POST'])
def analyze_resume_text():
    """
    API endpoint لتحليل السيرة الذاتية من نص وإنشاء PDF محسن
    """
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'الرجاء تقديم نص السيرة الذاتية'}), 400
        
        result = analyze_and_create_pdf_tool(data['text'])
        return jsonify({'message': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search-jobs', methods=['POST'])
def search_jobs():
    """
    API endpoint للبحث عن وظائف
    """
    try:
        data = request.get_json()
        if not data or 'skills' not in data or 'interests' not in data:
            return jsonify({'error': 'الرجاء تقديم المهارات والاهتمامات'}), 400
        
        result = search_jobs_tool(
            skills=data['skills'],
            interests=data['interests'],
            location=data.get('location', '')
        )
        return jsonify({'message': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 