import socket, sys, os, ssl, time

server_cert = 'server_cert.pem'
client_cert = 'client_cert.pem'
client_key = 'client_key.pem'

server_sni_hostname = 'server' # the 'common name' when making server cert

def send_file(server_ip, server_port, file_path):
    """Send a file to the server.
    
    Args:
        server_ip (str): IP address of the server.
        server_port (int): Port number of the server.
        file_path (str): Path of the file to be sent.
    """

    # Ensure that the given file exists
    assert os.path.exists(file_path), "File not found."
    
    # Create a client socket using IPv4 and TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Create the TLS context to wrap the socket.
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
    context.load_cert_chain(certfile=client_cert, keyfile=client_key)
    secureConnection = context.wrap_socket(client_socket, server_side=False, server_hostname=server_sni_hostname)
    
    try:
        secureConnection.connect((server_ip, server_port))
        print(f"Connected to server at {server_ip}:{server_port}")

        # Extract file name from path
        file_name = file_path.split('/')[-1]
        
        # Send the length of the file name to the server
        secureConnection.send(len(file_name.encode()).to_bytes(4, byteorder='big'))
        
        # Send the actual file name
        secureConnection.send(file_name.encode())
        
        # Open and send file
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                secureConnection.send(data)
                time.sleep(0.01)

        print("File sent successfully.")

    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        client_socket.close()
        print(f"Connection to {server_ip}:{server_port} closed.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: client.py <SERVER_IP> <SERVER_PORT> <FILE_PATH>")
        sys.exit(1)

    server_ip = sys.argv[1]
    
    try:
        server_port = int(sys.argv[2])
        assert 1024 <= server_port <= 65535, "Port number should be between 1024 and 65535."

        file_path = sys.argv[3]
        send_file(server_ip, server_port, file_path)
    except ValueError:
        print("Port should be a number.")

