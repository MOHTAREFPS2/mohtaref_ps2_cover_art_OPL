import os
import zipfile
import tempfile
import shutil
from flask import Flask, request, jsonify, send_from_directory, abort

# --- الإعدادات ---
SOURCE_DIR = 'ps2_covers' 
OUTPUT_DIR = 'generated_files' 
# ------------------

app = Flask(__name__, static_folder=None)

os.makedirs(OUTPUT_DIR, exist_ok=True)
if not os.path.isdir(SOURCE_DIR):
    print(f"تحذير: مجلد المصدر '{SOURCE_DIR}' غير موجود.")

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if '..' in path or path.startswith('/'):
        abort(404)
    return send_from_directory('.', path)

@app.route('/rename-and-zip', methods=['POST'])
def rename_and_zip():
    if not request.is_json:
        return jsonify({"success": False, "error": "Request must be JSON"}), 400

    data = request.get_json()
    original_id = data.get('original_id')
    new_id = data.get('new_id')

    if not original_id or not new_id:
        return jsonify({"success": False, "error": "Original and new ID are required"}), 400

    original_zip_filename = f"{original_id}.zip"
    original_zip_path = os.path.join(SOURCE_DIR, original_zip_filename)

    if not os.path.exists(original_zip_path):
        return jsonify({"success": False, "error": f"Original file '{original_zip_filename}' not found"}), 404

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            with zipfile.ZipFile(original_zip_path, 'r') as zip_ref:
                zip_ref.extractall(tmpdir)

            for filename in os.listdir(tmpdir):
                if original_id in filename:
                    new_filename = filename.replace(original_id, new_id, 1)
                    os.rename(os.path.join(tmpdir, filename), os.path.join(tmpdir, new_filename))
            
            new_zip_basename = os.path.join(OUTPUT_DIR, new_id)
            shutil.make_archive(new_zip_basename, 'zip', tmpdir)
            new_zip_filename_with_ext = f"{new_id}.zip"

        return jsonify({
            "success": True, 
            "download_url": f"/download/{new_zip_filename_with_ext}",
            "filename": new_zip_filename_with_ext
        })
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"success": False, "error": "An internal error occurred while processing the file"}), 500

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
