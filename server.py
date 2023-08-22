import socket
from threading import Thread
import random


server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address="127.0.0.1"
port = 8000

server.bind((ip_address,port))
server.listen()

questions=[
"Who gifted the statue of liberty? /n a.france /n b.India /n c.UAE /n d.singapour",
"Which is the biggest planet of the solar system? /n a.neptune /n b.jupiter /n c.uranus /n d.pluto"
]
answers=["a","b"]
list_of_clients=[]
nicknames=[]
print("SERVER HAS BEEN STARTED")




def clientthread(conn,nicknmae):
    score = 0
    conn.send("Welcome to this quiz game!".encode('utf-8'))
    conn.send("You will recieve a question. The answer is from the below option a,b,c,d".encode('utf-8'))
    conn.send("Good Luck!\n\n".encode('utf-8'))
    index,question,answer = get_random_question_answer(conn)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.split(': ')[-1].lower()== answer:
                    score += 1
                    conn.send(f"Bravo! Your score is {score}\n\n".encode('utf-8'))
                else:
                    conn.send("Incorrect answer! Better luck next time!\n\n".encode('utf-8'))
                remove_question(index)
                index,question,answer = get_random_question_answer(conn)
            else:
                remove(conn)
                remove_nickname(nickname)
        
        except:
            continue

def broadcast(message,connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message.encode("utf-8"))
            except:
                remove(clients) 
def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)
def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)


def get_random_question_answer(conn):
    random_index = random.randint(0,len(questions)-1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

while True:
    conn,addr = server.accept()
    conn.send("NICKNAME".encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')
    list_of_clients.append(conn)
    nicknames.append(nickname)
    message = '{}joined'.format(nickname)
    print(message)
    # broadcast(message,conn)
    new_thread = Thread(target= clientthread,args=(conn,nickname))
    new_thread.start()

