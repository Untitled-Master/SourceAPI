from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search():
    url = "https://shamela.ws/ajax/search"
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
        "Referer": "https://shamela.ws/search",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    
    term = request.form.get('term')
    if not term:
        return jsonify({"error": "No search term provided"}), 400
    
    data = {
        "term": term
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from Shamela"}), response.status_code
    
    codeh = response.text
    soup = BeautifulSoup(codeh, 'html.parser')

    # Find all <a> elements for links
    links = soup.find_all('a')

    # Find all <p> elements for paragraphs
    paragraphs = soup.find_all('p')

    results = []
    for link, paragraph in zip(links, paragraphs):
        href = link.get('href')
        text = link.text.strip()
        if href and text:
            result = {
                "paragraph": paragraph.text.strip(),
                "link_text": text,
                "link_href": href
            }
            results.append(result)
    
    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
