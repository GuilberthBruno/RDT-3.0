import socket
import random
import time
import threading
encerrarPrograma = False

class Network:
    def __init__(self):
        self.port = 9999
        self.connected_nodes = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("0.0.0.0", self.port))
        self.time_limit = 5
        self.problem = "4"


    def receive_message(self):
        while encerrarPrograma == False:
            data, addr = self.socket.recvfrom(1024)
            sender_ip = addr[0]
            receveid_data = data.decode()
            print(f"\n{data}\n")


            if sender_ip not in self.connected_nodes:
                print(f"Nova conexão - {sender_ip}")
                self.connected_nodes.append(sender_ip)
                connected_message = f"CONNECTION | {True} | {sender_ip}"
                self.send_message(connected_message.encode(), sender_ip)

            elif self.problem == "1":
                destip = receveid_data.split(' | ')[3]
                if receveid_data.split(" | ")[2] == "MESSAGE":
                    data = self.corrupted_data(receveid_data.split(' | ')[5], data)
                else:
                    data = self.corrupted_data(receveid_data.split(' | ')[3], data)
                self.send_message(data, destip)
                self.problem = "4"

            elif self.problem == "2":
                self.timer_limit()
                self.problem = "4"

            elif self.problem == "3":
                if receveid_data.split(" | ")[2] == "ACK":
                    self.send_message(data, receveid_data.split(" | ")[3])
                    self.send_message(data, receveid_data.split(" | ")[3])
                else:
                    self.send_message(data, receveid_data.split(" | ")[3])

                self.problem = "4"

            elif self.problem == "4":
                self.send_message(data, receveid_data.split(" | ")[3])

    
    
    def send_message(self, data, destip):
        self.socket.sendto(data, (destip, self.port))



    

    def change_problem(self, new_problem):
        self.problem = new_problem

    def corrupted_data(self, data_to_corrupt, data):
        corrupted_data = data_to_corrupt.encode()
        # Copiar os dados originais para evitar modificá-los diretamente
        corrupted_data = bytearray(corrupted_data)

        # Escolha de um índice aleatório que será o byte a ser corrompido
        index_to_corrupt = random.randint(0, len(corrupted_data) - 1)

        # Alterar o byte escolhido
        corrupted_data[index_to_corrupt] ^= 0xFF  #aplicação da operação de OU exclusivo no byte selecionado - 0xFF representa um byte de 1s

        corrupted_data = bytes(corrupted_data[1:])

        data = data.decode()
        data_list = data.split(" | ")
        data_list[5] = corrupted_data.decode('utf-8', errors='replace')

        data = ' | '.join(data_list)

        corrupted_data = data.encode()

        return corrupted_data

    def timer_limit(self):
        timer = time.time()
        while time.time() - timer <= self.time_limit:
            pass

        self.problem = "3"




if __name__ == "__main__":
    net = Network()
    thread = threading.Thread(target=net.receive_message)
    thread.start()
    while encerrarPrograma == False:
        opcao = input("-------------------MENU-------------------------- \n 1 - Alterar problema a ser testado\n 2 - Encerrar programa\n")
        problem = ""
        if opcao == "1":
            while(True) :
                problem = input("Qual problema você quer testar?\n1 - dados corrompidos\n2 - Estouro de temporizador\n3 - Enviar ack duplicado\n4 - Enviar mensagem normalmente")

                if problem == "1" or problem == "2" or problem == "3" or problem == "4":
                    break

            net.problem = problem

        elif opcao == "2":
            encerrarPrograma = True
            thread.join()
