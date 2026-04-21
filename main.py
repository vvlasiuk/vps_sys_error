import time
from rabbitmq import RabbitMQClient, OUTPUT_QUEUES
from logger import log_message
from dispatcher import Dispatcher
from config import get_env

RETRY_DELAY = int(get_env('RETRY_DELAY', 60))

def main():
    dispatcher = Dispatcher()
    while True:
        try:
            client = RabbitMQClient()
            client.connect()
            print("[Main] Connected to RabbitMQ")
            while True:
                msg = client.get_message()
                if not msg:
                    time.sleep(1)
                    continue
                print(f"[Main] Received: {msg}")
                logged = log_message(msg)
                out_msgs = dispatcher.dispatch(msg)
                if not logged:
                    print("[Main] Log failed, sending to all channels")
                    # Якщо логування неуспішне — форсовано у всі канали
                    for ch, _ in OUTPUT_QUEUES.items():
                        for _, out_msg in out_msgs:
                            if ch == out_msg['destination']['system']:
                                client.send_message(ch, out_msg)
                else:
                    for ch, out_msg in out_msgs:
                        if ch in OUTPUT_QUEUES:
                            client.send_message(ch, out_msg)
            client.close()
        except Exception as e:
            print(f"[Main] RabbitMQ error: {e}. Retry in {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)

if __name__ == '__main__':
    main()
