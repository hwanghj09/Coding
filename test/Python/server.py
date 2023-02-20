import socketserver

class MyHandler(socketserver.BaseRequestHandler):
    users = {}
    def send_all_message(self, msg):
        for sock, _ in self.users.values():
            sock.send(msg.encode())


    def handle(self):
        ##client_address는 BaseRequestHandler에 있음
        print(self.client_address)

        while True:
            self.request.send("채팅 닉네임을 입력하세요:".encode)  ##접속되어 있는 소켓을 의미함. BaseRequestHandler 여기에 있음
            nickname = self.request.recv(1024).decode()

            if nickname in self.users:
                self.request.send("이미 등록된 닉네임 입니다. \n".encode())
            else:
                self.users[nickname] = (self.request, self.client_adrress)
                print("현재 {}명 참여중".format(len(self.users)))
                self.send_all_message("[{}]님이 입장 했습니다.".format(nickname))
                break
        ##실제 채팅구현
        while True:
            msg = self.request.recv(1204)
            if msg.decode() =="/bye":
                self.request.close()
                break
            self.send_all_message("[{}] {}".format(nickname, msg.decode()))
        
        if nickname in self.users:
            del self.users[nickname]
            self.send_all_message("[{}]님이 퇴장하셨습니다.".format(nickname))
            print("현재 {}명 참여중".format(len(self.users)))
            
class ChatServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

server = ChatServer(("", 8080), MyHandler ) ##BaseRequestHandler
server.serve_forever()
server.shutdown
server.server_close()