from flask import Flask, request, jsonify

app = Flask(__name__)

def scrape_web_content(query):
    import requests
    from bs4 import BeautifulSoup
    
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = [h3.text for h3 in soup.find_all('h3')]
    
    return titles

def generate_summary(text):
    import spacy
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    summary = [sentence.text for sentence in doc.sents]
    return ' '.join(summary)

def create_script(title, summary):
    script = f"Title: {title}\n\n"
    script += f"Introduction:\n{summary[:150]}\n\n"
    script += "Main Content:\n"
    for i, content in enumerate(summary.split('.')):
        script += f"{i+1}. {content.strip()}\n"
    script += "\nConclusion:\n" + " ".join(summary[-150:])
    return script

@app.route('/generate-script', methods=['POST'])
def generate_script_route():
    data = request.get_json()
    title = data.get('title', 'No Title')
    results = scrape_web_content(title)
    summary = generate_summary(" ".join(results))
    script = create_script(title, summary)
    return jsonify({"script": script})

if __name__ == '__main__':
    app.run(debug=True)
