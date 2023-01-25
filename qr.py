from flask import Flask, request, jsonify, send_file, render_template
import qrcode
from PIL import Image
from urllib.parse import urlparse

app = Flask(__name__, template_folder='templates')
path = 'qr_code.png'

@app.route('/generate_qr', methods=['GET'])
def generate_qr():
    url = request.args.get("url")
    parsed_url = urlparse(url)
    if parsed_url.scheme and parsed_url.netloc:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img = img.convert("RGB")
        img.save(path)
        return render_template("qr_code.html",url=url)
    else:
        return jsonify({"error": "Invalid URL provided"}), 400

@app.route('/download')
def download():
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
