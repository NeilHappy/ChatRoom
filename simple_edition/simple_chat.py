from asyncore import dispatcher
from asynchat import async_chat
import socket,asyncore

PORT=6005
NAME='TestChat'

class ChatSession(async_chat):

    def __init__(self,server,sock):
        async_chat.__init__(self,sock)
        self.server=server
        serl.set_terminator("\r\n")
        self.data=[]
        self.push('Welcome to %s\r\n' % self.server.name)

    def collect_incoming_data(self,data):
        self.data.append(data)

    def found_terminator(self):
        line=''.join(self.data)
        self.data=[]
        self.server.broadcast(line)

    def handler_close(self):
        async_chat.handler_close(self)
        self.server.disconnect(self)

class ChatServer(dispatcher):
    def __init__(self,port,name):
        dispatcher.__init__(self)
        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('',port))
        self.listen(5)
        self.name=name
        self.sessions=[]

    def disconnect(self,session):
        self.sessions.remove(session)

    def broadcast(self,line):
        for session in self.sessions:
            session.push(line+'\r\n')

    def handle_accept(self):
        conn,addr=self.accept()
        self.sessions.append(ChatSession(self,conn))

if __name__=='__main__':
    s=ChatServer(PORT,NAME)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        print 

