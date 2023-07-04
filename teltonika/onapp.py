import socket
import psycopg2
from datetime import datetime
import binascii
import struct

# Replace with the IP address of the EC2 instance and the port number to use for the TCP connection
server_address = ("0.0.0.0", 5010)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(server_address)

sock.listen(1)


while True:
    print('Waiting for a connection...')
    connection, client_address = sock.accept()

    try:
        print('Connection from', client_address)

        imei = connection.recv(1024).decode().strip()

        print('imei:', imei)

        connection.send(b'\x01')

        avl_data = connection.recv(1280)
        data = avl_data.hex()
        print("data received : ", data)
    
        

    except Exception as e:
        print("Error:", e)

    finally:
        connection.close()




# import socket

# HOST = '0.0.0.0'  # Your server's IP address
# PORT = 5010  # Port to listen on

# def decode_codec8(data):
#     imei = data[0:15].decode('ascii')  # Extract the IMEI (assuming ASCII encoding)
#     codec_id = struct.unpack('>H', data[15:17])[0]  # Extract the codec ID (2 bytes, big-endian)
#     gps_data = data[17:]  # Extract the GPS data portion

#     # Implement your codec8 decoding logic here based on the Teltonika protocol
#     # This is just a placeholder implementation

#     # Example decoding: Extract latitude, longitude, and speed
#     latitude = struct.unpack('>i', gps_data[0:4])[0] / 10000000
#     longitude = struct.unpack('>i', gps_data[4:8])[0] / 10000000
#     speed = struct.unpack('>H', gps_data[8:10])[0] / 10

#     decoded_data = {
#         'IMEI': imei,
#         'Codec ID': codec_id,
#         'Latitude': latitude,
#         'Longitude': longitude,
#         'Speed': speed
#     }

#     return decoded_data

# def handle_client(client_socket):
#     while True:
#         imei = client_socket.recv(1024).decode().strip()
#         if not imei:
#             break
        
#         client_socket.send(b'\x01')
#         data = client_socket.recv(8192)
#         decoded_data = decode_codec8(data)
#         print(decoded_data)

# def start_server():
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind((HOST, PORT))
#     server_socket.listen(1)
#     print(f"Server listening on {HOST}:{PORT}")

#     while True:
#         client_socket, client_address = server_socket.accept()
#         print(f"Client connected: {client_address[0]}:{client_address[1]}")
#         handle_client(client_socket)

# start_server()
