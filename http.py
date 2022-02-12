import socket
import subprocess
import os

def handle_request(request):
    headers = request.split('\n')
    
    try:
        filename = headers[0].split()[1]
    except IndexError as e:
        print(e)
        
    
    if filename == '/':
        filename = '/index.html'

    try:
        filename = './app' + filename
        print(filename)
        content = ''
        if '.php' in filename:
            content = dynamic_handler(filename, 'php')  
        elif '.py' in filename:
            content = dynamic_handler(filename, 'python')
        elif '.js' in filename:
            content = dynamic_handler(filename, 'node')
        else:
            fin = open(filename)
            content = fin.read()
            fin.close()

        response = 'HTTP/1.0 200 OK\ncontent-type: text/html; charset=utf-8\n\n' + content
    except FileNotFoundError:
        response = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'

    return response


def dynamic_handler(filename, command):
    filename = os.getcwd() + '/' + filename
    proc = subprocess.Popen(f"{command} {filename}", shell=True, stdout=subprocess.PIPE)
    return proc.stdout.read().decode("utf-8")


# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)
print('Listening on port %s ...' % SERVER_PORT)

try:
    while True:
        # Wait for client connections
        client_connection, client_address = server_socket.accept()
        # Get the client request
        request = client_connection.recv(1024).decode()
        print(request, client_address, "\n\n")

        # Return an HTTP response
        response = handle_request(request)
        client_connection.sendall(response.encode())

        # Close connection
        client_connection.close()
except (Exception,KeyboardInterrupt) as e:
    print('\nClosing connection gracefully!! ')
    print(e.with_traceback(), e)
    # Close socket
    server_socket.close()
