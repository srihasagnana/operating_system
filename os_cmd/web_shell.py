from flask import Flask, request, jsonify, Response, render_template
import subprocess

app = Flask(__name__)

os_commands = {
    "Windows": [
        "dir", "echo Hello World", "whoami", "ping 127.0.0.1 -n 2", "tasklist", "type README.txt", "cls"
    ],
    "Linux": [
        "ls", "echo Hello World", "whoami", "ping -c 2 127.0.0.1", "ps aux", "cat README.txt", "clear"
    ]
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/commands')
def get_commands():
    return jsonify(os_commands)

@app.route('/run', methods=['POST'])
def run():
    data = request.json
    cmd = data.get('command', '')
    os_type = data.get('os', 'Windows')

    if not cmd:
        return jsonify({'stderr': 'No command provided.'})

    try:
        if os_type == "Windows":
            shell_cmd = ['cmd.exe', '/c', cmd]
        else:
            shell_cmd = ['bash', '-c', cmd]

        result = subprocess.run(shell_cmd, capture_output=True, text=True, timeout=10)
        return jsonify({
            'stdout': result.stdout.strip(),
            'stderr': result.stderr.strip()
        })
    except Exception as e:
        return jsonify({'stderr': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
