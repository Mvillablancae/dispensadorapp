from websocket import create_connection
ws = create_connection("ws://localhost:8000/ws/scheduler/")
print("Sending 'Hello, World'...")
ws.send('{"message": "World" }')
print("Sent")
print("Receiving...")
result =  ws.recv()
print("Received '%s'" % result)
ws.close()