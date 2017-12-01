import socket, time, types, select
from collections import namedtuple
from heapq import heappush, heappop

######### Reactor ####################################################################

ScheduledEvent = namedtuple('ScheduleEvent', ['event_time', 'task'])
Session = namedtuple('Session', ['address', 'file'])

events = []                   # heap with events prioritized by earliest time
sessions = {}                 # { csocket : Session(address, file)}
callback = {}                 # { csocket : callback(client, line) }
generators = {}               # { csocket : inline callback generator}

def reactor(host='localhost', port=9600):
    'Main event loop that triggers the appropriate business logic callbacks'
    s = socket.socket()
    s.bind((host, port))
    #calling listen puts the socket into sever mode
    # The integer argument is the number of connections the system should queue up
    #in the background before rejecting new clients
    s.listen(5)
    s.setblocking(0)          # Make asynchronous.  Never wait on a client socket.
    sessions[s] = None
    print('Server up, running, and waiting for call on {} {}'.format(host, port))
    try:
        while True:
            # Serve existing clients BUT only if they already have data ready
            ready_to_read, _, _ = select.select(sessions, [], [], 0.1)
            for c in ready_to_read:
                if c is s:
                    #accept() returns an open connection between the server and client,
                    #along with the address of the client.
                    #The connection is actually a different socket on another port
                    #(assigned by the kernel).
                    conection, client_address = c.accept()
                    connect(conection, client_address)
                    continue
                line = sessions[c].file.readline()
                if line:
                    callback[c](c, line.rstrip())
                else:
                    disconnect(c)

            # Run events scheduled at the appropriate event time
            while events and events[0].event_time <= time.monotonic():
                event = heappop(events)
                event.task()
    except KeyboardInterrupt:
        print('\nBye!')
    finally:
        s.close()

def connect(connection, client_address):
    '''Reactor logic for new connections
    connection - socket'''
    # c.makefile - Return a file object associated with the socket.
    sessions[connection] = Session(client_address, connection.makefile())
    on_connect(connection)         # call into user's business logic

def disconnect(c):
    'Reactor logic to end sessions'
    on_disconnect(c)                         # call into user's business logic
    sessions[c].file.close()
    c.close()
    del sessions[c]
    del callback[c]

def add_task(event_time, task):
    'Helper function to schedule one-time tasks at specific time'
    heappush(events, ScheduledEvent(event_time, task))

def call_later(delay, task):
    'Helper function to schedule one-time tasks after a given delay'
    add_task(time.time() + delay, task)

def call_periodic(delay, interval, task):
    'Helper function to schedule recurring tasks'
    def inner():
        task()
        call_later(interval, inner)
    call_later(delay, inner)


def on_connect(c):
        g = nbcaser(c)          # 'g' is a coroutine
        generators[c] = g       # generators -> awaitables
        callback[c] = g.send(None)  # we do this to advance `nbcaser` coroutine
                                    # to yield through the 'readline' coroutine
                                    # which will sleep on its 'yield' expression

def on_disconnect(c):
        g = generators.pop(c)
        g.close()

@types.coroutine
def readline(c):
    'A non-blocking readline to use with two-way generators'
    def inner(c, line):
        g = generators[c]
        try:
            callback[c] = g.send(line)  # `g.send(line)` will resume the `yield inner` point
        except StopIteration:
            disconnect(c)
    line = yield inner
    return line


######### User's Business Logic ######################################################

def announcement():
    print('The event loop is still running at:', time.ctime())

call_periodic(delay=1, interval=15, task=announcement)

async def nbcaser(c):
    upper, title = 'upper', 'title'
    mode = upper
    print("Received connection from", sessions[c].address)
    try:
        c.sendall(b'<welcome: starting in upper case mode>\n')
        while 1:
            line = await readline(c)
            if line == 'quit':
                c.sendall(b'quit\r\n')
                return
            if mode is upper and line == 'title':
                c.sendall(b'<switching to title case mode>\r\n')
                mode = title
                continue
            if mode is title and line == 'upper':
                line = c.sendall(b'<switching to upper case mode>\r\n')
                mode = upper
                continue
            print(sessions[c].address, '-->', line)
            if mode is upper:
                c.sendall(b'Upper-cased: %a\r\n' % line.upper())
            else:
                c.sendall(b'Title-cased: %a\r\n' % line.title())
    finally:
        print(sessions[c].address, 'quit')


if __name__ == '__main__':
    reactor('localhost', 9600)

