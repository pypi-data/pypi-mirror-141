import asyncio, socket
from sys import argv


async def handle_client(client):
    loop = asyncio.get_event_loop()
    request = None
    while request != 'quit':
        request = (await loop.sock_recv(client, 255)).decode('utf8')
        response = str(eval(request)) + '\n'
        await loop.sock_sendall(client, response.encode('utf8'))
    client.close()


async def run_server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(8)
    sock.setblocking(False)

    loop = asyncio.get_event_loop()

    while True:
        client, _ = await loop.sock_accept(sock)
        loop.create_task(handle_client(client))


if __name__ == '__main__':
    if len(argv) != 3:
        print(f'Usage: {argv[0]} <listen_addr> <listen_port>')
        exit()
    asyncio.run(run_server(argv[1], argv[2]))
