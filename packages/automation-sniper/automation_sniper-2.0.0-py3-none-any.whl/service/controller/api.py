import os
from flask import Flask, jsonify, request
from service.parser import parser_service
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "secret key"
UPLOAD_FOLDER = '/Users/pankaj.nayak/Desktop/swagger_output' #fixme-add cloud storage location
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'json', 'yml'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/transformation_tool', methods=['POST'])
def transform_api():
    if 'swagger_file' in request.files:
        file = request.files["swagger_file"]
        if "team_name" not in request.form:
            return jsonify({"error": "please provide team name"}), 400
        team_name = request.form.get("team_name")
        if file.filename == '':
            return jsonify({'message': 'No file selected for uploading'}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            payload = {
                'swagger_file_path': file_path,
                'team_name': team_name,
                'upload_path': UPLOAD_FOLDER
            }
        else:
            return jsonify({'message': 'Allowed file types are json or yml', 'status': 'Failed'}), 400
    else:
        if not request.json:
            return jsonify({"error": "please provide proper payload "}), 400
        if 'swagger_url' not in request.json:
            return jsonify({"error": "please provide proper swagger_api link"}), 400
        if 'team_name' not in request.json:
            return jsonify({"error": "please provide team name"}), 400
        if "version" not in request.json:
            return jsonify({"error": "please provide swagger version v1 or v2"}), 400
        payload = {
            'swagger_url': request.json['swagger_url'],
            'team_name': request.json['team_name'],
            'version': str(request.json['version']).lower(),
            'upload_path': UPLOAD_FOLDER
        }
    if bool(payload):
        # print(payload)
        res, error, storage_path = parser_service(**payload)
        if res:
            return jsonify({"status": "Success", "framework_location": storage_path}), 201
        else:
            return jsonify({"status": "Failed", "error": error}), 500


if __name__ == '__main__':
    app.run(debug=True)