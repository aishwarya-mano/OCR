from flask import Flask, request, jsonify
from flask_cors import CORS
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import io

app = Flask(__name__)
CORS(app)


@app.route('/api/analyze', methods=['POST'])
def analyze_image():
    image_file = request.files['image']
    image_stream = io.BytesIO()
    image_file.save(image_stream)
    image_stream.seek(0)

    subscription_key = '462cd837573949d5a34ccbbc063c1bc4'
    endpoint = 'https://aishwarya-demo.cognitiveservices.azure.com/'
    computervision_client = ComputerVisionClient(
        endpoint, CognitiveServicesCredentials(subscription_key))

    image_analysis = computervision_client.read_in_stream(
        image_stream, raw=True)
    read_operation_location = image_analysis.headers["Operation-Location"]
    operation_id = read_operation_location.split("/")[-1]

    import time
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    text = ""
    if read_result.status == 'succeeded':
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                text += line.text + "\n"

    return jsonify({'text': text})


if __name__ == '__main__':
    app.run(debug=True)
