#!/usr/bin/env python3
import sys
import time
from socket import *

def main():
    server = '127.0.0.1'
    port = 12000
    if len(sys.argv) >= 2:
        server = sys.argv[1]
    if len(sys.argv) >= 3:
        port = int(sys.argv[2])

    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(1)

    rtts = []
    received = 0

    for seq in range(1, 11):
        send_time = time.time()
        message = f"Ping {seq} {send_time}"
        try:
            clientSocket.sendto(message.encode(), (server, port))
            recv_message, addr = clientSocket.recvfrom(1024)
            recv_time = time.time()
            rtt = recv_time - send_time
            print(recv_message.decode())
            print(f"RTT: {rtt:.6f} seconds")
            rtts.append(rtt)
            received += 1
        except timeout:
            print("Request timed out")

        # small pause so output is readable
        time.sleep(0.1)

    print("\n--- Ping statistics ---")
    lost = 10 - received
    loss_rate = (lost / 10.0) * 100
    print(f"Packets: Sent = 10, Received = {received}, Lost = {lost} ({loss_rate:.0f}% loss)")
    if rtts:
        print(f"Minimum RTT = {min(rtts):.6f} s")
        print(f"Maximum RTT = {max(rtts):.6f} s")
        print(f"Average RTT = {sum(rtts)/len(rtts):.6f} s")

if __name__ == '__main__':
    main()
