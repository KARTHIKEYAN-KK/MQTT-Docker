import pyinotify
import time

log_file_path = '/root/MQTT-Docker/log/event.log'
last_position = 0

class LogEventHandler(pyinotify.ProcessEvent):
    def process_default(self, event):
        global last_position
        with open(log_file_path, 'r') as log_file:
            log_file.seek(last_position)  # Move to the last known position
            new_lines = log_file.readlines()
            
            for line in new_lines:
                if 'session has expired' in line or 'disconnected' in line:
                    continue

                timestamp, client_id = extract_client_id_and_time(line)
                if timestamp and client_id:
                    print(f"Timestamp: {timestamp}, Client ID: {client_id}")

            last_position = log_file.tell()  # Update the last known position

def extract_client_id_and_time(line):
    parts = line.strip().split(' - ')
    if len(parts) >= 2:
        timestamp = parts[0]
        rest = parts[1]
        client_id_start = rest.find('Client ID: ')
        if client_id_start != -1:
            client_id = rest[client_id_start + len('Client ID: '):].split(',')[0]
            return timestamp, client_id
    return None, None

wm = pyinotify.WatchManager()
mask = pyinotify.IN_MODIFY

handler = LogEventHandler()

notifier = pyinotify.Notifier(wm, handler)

wdd = wm.add_watch(log_file_path, mask, rec=False)

print(f"Monitoring changes in {log_file_path}...")

while True:
    try:
        notifier.process_events()
        if notifier.check_events():
            notifier.read_events()
    except KeyboardInterrupt:
        notifier.stop()
        break

print("Monitoring stopped.")
