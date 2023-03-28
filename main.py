from logging import log
from os import path, mkdir
from os.path import join, dirname
import datetime as dt
from utils.webcam import webcamera # Custom Function to handle webcam.
import multiprocessing
import socketserver
import websockets
import asyncio
import uuid
import cv2
import time


def socket(packet):
    async def handler(web_socket, path):
        print("Attempting to connect to socket...")
        try:
            print("Web socket connected successfully")
            while True:
                await asyncio.sleep(0.033) # Is what establishes it as 30 FPS
                await web_socket.send(packet[0].tobytes())
        except websockets.exceptions.ConnectionClosed:
            print("Web socket connection terminated...")
    # Create the awaitable object
    start_server = websockets.serve(ws_handler=handler, host="localhost", port=8080)
    # Start the server, add it to the event loop
    asyncio.get_event_loop().run_until_complete(start_server)
    # Registered our websocket connection handler, thus run event loop forever
    asyncio.get_event_loop().run_forever()

def main():
    run_program = True
    manager = multiprocessing.Manager()
    manager_list = manager.list()
    manager_list.append(None)
    # Initialize processes
    socket_connection_handler = multiprocessing.Process(target=socket, args=(manager_list,))
    camera_connection_handler = multiprocessing.Process(target=webcamera, args=(manager_list,))
    # Collect Processes 
    PROCESSES = [ socket_connection_handler, camera_connection_handler ]
    # Start processes
    for process in PROCESSES:
        print("starting processes")
        process.start()
    # Loop forever
    while run_program is True:
        pass
    # terminate processes
    for process in PROCESSES:
        process.terminate()
        log("Terminated processes.", "Standard", "Standard", "logs")    
    run_program = False
        

if __name__ == '__main__':
    print("launching application...")
    run_program = True
    try:
        main()
    except:
        print("Error...")
    print("Program terminated...")

