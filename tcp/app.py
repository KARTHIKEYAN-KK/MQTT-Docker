import socket
import psycopg2
from datetime import datetime

# Replace with the IP address of the EC2 instance and the port number to use for the TCP connection
server_address = ("0.0.0.0", 5010)

# Create a TCP socket and bind it to the server address
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

conn = psycopg2.connect(host="13.232.49.108", port=5001, database="iot", user="postgres", password="postgres")
cur = conn.cursor()

while True:
    print('Waiting for a connection...')
    connection, client_address = sock.accept()

    try:
        print('Connection from', client_address)

        # Receive data from the client
        data = connection.recv(1024)
        hexData = data.hex()
        bytes_object = bytes.fromhex(hexData)
        regular_string = bytes_object.decode('utf-8')

        asciiData = bytes.fromhex(hexData).decode('ascii')

        bytes_object = bytes.fromhex(asciiData)
        regular_string = bytes_object.decode('utf-8')

        print('Hex data:', asciiData)
        print('Received data:', regular_string)

        split_data = regular_string.split("#")

        device_id = split_data[0]
        mac_address = split_data[1]
        gsm_signal = split_data[2]
        flood_status = split_data[3]
        time = datetime.utcnow()

        print('device_id', device_id)
        print('mac_address', mac_address)
        print('gsm_signal', gsm_signal)
        print('flood_status', flood_status)

        cur.execute("INSERT INTO devicedata (device_id, mac_address, gsm_signal, flood_status, timestamp) VALUES (%s, %s, %s, %s, %s)", (device_id, mac_address, gsm_signal, flood_status, time))
        conn.commit()

    except Exception as e:
        print("Error:", e)

    finally:
        # Close the connection
        connection.close()
