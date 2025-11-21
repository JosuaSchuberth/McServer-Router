import argparse
import os
import socket
import threading


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Port",
    )
    return parser.parse_args()


def handle_client(conn, addr):
    print(f"Connected: {addr}")
    with conn:
        try:
            buffer = b""
            while True:
                data = conn.recv(1024)
                if not data:
                    print(f"Connection closed: {addr}")
                    break

                buffer += data
                while b"\n" in buffer:
                    line, buffer = buffer.split(b"\n", 1)
                    message = line.decode("utf-8", errors="ignore").strip()

                    if message.lower() == "ping":
                        response = "pong\n"
                    else:
                        response = f"echo:{message}\n"

                    conn.sendall(response.encode("utf-8"))
        except Exception as e:
            print(f"Error {addr}: {e}")


def main():
    args = parse_args()
    port = args.port

    host = "0.0.0.0"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print(f"Server up: {host}:{port}")

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(
                target=handle_client, args=(conn, addr), daemon=True
            )
            thread.start()


if __name__ == "__main__":
    main()
