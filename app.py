from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key="AIzaSyA9Ht_ec5N0wQPDxSWkN8eh1LpeJWL9KfE")
model = genai.GenerativeModel("gemini-1.0-pro")

JSON_FILE_REFERENCE = "https://drive.google.com/file/d/1ft3u6xIPt4rd6gM-0XnMrSbqDyniXPHu/view?usp=sharing"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        major = data.get('major')
        if not major:
            return jsonify({"error": "Major name is required."}), 400

        prompt = (
            f"The data for majors is hosted at {JSON_FILE_REFERENCE}. Based on this data, "
            f"generate a 2-year meta-major plan based on these majors list '{major}'. Provide a structured list "
            f"of suggested courses or pathways."
        )

        response = model.generate_content(prompt)
        suggestion = response.text.strip()
        return jsonify({"suggestion": suggestion})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
