from flask import Flask, jsonify
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os
import json
from typing import List, Dict, Any, Tuple


def execute_notebook(notebook_path: str, timeout: int = 1200) -> Tuple[nbformat.NotebookNode, str]:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)

    executor = ExecutePreprocessor(timeout=timeout, kernel_name='python3')
    resources = {'metadata': {'path': os.path.dirname(notebook_path) or '.'}}

    executor.preprocess(notebook, resources)

    collected_text: List[str] = []
    for cell in notebook.cells:
        if cell.cell_type == 'code':
            for output in cell.get('outputs', []):
                if output.get('output_type') == 'stream' and output.get('name') == 'stdout':
                    collected_text.append(output.get('text', ''))
                elif output.get('output_type') in ('execute_result', 'display_data'):
                    data = output.get('data', {})
                    if 'text/plain' in data:
                        collected_text.append(str(data['text/plain']))

    return notebook, ''.join(collected_text)


def extract_json_objects(text: str) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    brace_level: int = 0
    current_chars: List[str] = []

    for ch in text:
        if ch == '{':
            brace_level += 1
        if brace_level > 0:
            current_chars.append(ch)
        if ch == '}':
            brace_level -= 1
            if brace_level == 0 and current_chars:
                candidate = ''.join(current_chars)
                try:
                    obj = json.loads(candidate)
                    results.append(obj)
                except Exception:
                    pass
                current_chars = []

    return results


app = Flask(__name__)


@app.get('/api/match-infos')
def api_match_infos():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    nb_save = os.path.join(root_dir, 'save_match_link_to_xlsx.ipynb')
    nb_infos = os.path.join(root_dir, 'get_match_infos.ipynb')

    try:
        _, _ = execute_notebook(nb_save)
    except Exception as e:
        return jsonify({'error': 'Failed to run save_match_link_to_xlsx.ipynb', 'details': str(e)}), 500

    try:
        _, out_text = execute_notebook(nb_infos)
        items = extract_json_objects(out_text)
        return jsonify({'count': len(items), 'items': items})
    except Exception as e:
        return jsonify({'error': 'Failed to run get_match_infos.ipynb', 'details': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


