import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/compile-run-java', methods=['POST'])
def compile_run_java():
    data = request.json
    code = data.get('code')
    input_data = data.get('input')

    if code:
        # Call the function to compile and run the provided Java code
        result = compile_and_run_java_code(code, input_data)
        return jsonify(result)
    else:
        return jsonify({'success': False, 'error': 'No code provided.'})

def compile_and_run_java_code(code, input_data=None):
    try:
        # Write the Java code to a temporary file
        with open('Main.java', 'w') as f:
            f.write(code)

        # Prepare input data if provided
        input_bytes = None
        if input_data:
            input_bytes = input_data.encode()

        # Compile the Java code using JDK
        compile_process = subprocess.run(['javac', 'Main.java'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if compile_process.returncode == 0:
            # If compilation is successful, execute the compiled program
            execution_command = ['java', 'Main']
            execution_process = subprocess.run(execution_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=input_bytes)
            output_text = execution_process.stdout.decode('utf-8')
            return {'success': True, 'output': output_text}
        else:
            # If compilation fails, return the compilation error
            compile_error = compile_process.stderr.decode('utf-8')
            return {'success': False, 'error': compile_error}
    except Exception as e:
        # If any error occurs during compilation or execution, return the error message
        return {'success': False, 'error': str(e)}
    finally:
        # Clean up temporary files
        subprocess.run(['rm', 'Main.java', 'Main.class'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
