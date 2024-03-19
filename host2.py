import socket
import time
import threading

encerrarPrograma = False

class Host:
    def __init__(self):
        self.port = 9999
        self.ip = ""
        self.network_address = "192.168.1.11"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("0.0.0.0", self.port))
        self.num_seq = True
        self.timer_limit = 5
        self.wait_ack = False

    def send_message(self, receiver_ip , message):
        data = f"{self.num_seq} | MESSAGE | {receiver_ip} | {self.ip} | {message}" 
        checksum = self.checksum(data.split(" | ")[4].encode())
        data = f"{checksum} | " + data
        self.socket.sendto(data.encode(), (self.network_address, self.port))
        num_seq_actual = self.num_seq
        self.wait_ack == True
        inicio = time.time()

        while self.num_seq == num_seq_actual:
            if time.time() > inicio + self.timer_limit:
                self.send_message(receiver_ip , message)
        
        
        

    
    def receive_message(self):

        while encerrarPrograma == False:
            data, addr = self.socket.recvfrom(1024)
            receveid_data = data.decode().split(" | ")
            
            if receveid_data[0] == "CONNECTION":
                self.ip = receveid_data[2]
            
            elif self.wait_ack == False:
                if self.not_corrupted(receveid_data[5].encode(), receveid_data[0]) and receveid_data[1] == self.num_seq:
                    self.send_ack(receveid_data[4], self.num_seq)
                    self.num_seq = not self.num_seq
                    print(f"\nReceveid message from {receveid_data[4]} - {receveid_data[5]}\n")
                
                else:
                    self.send_ack(receveid_data[4], not self.num_seq)

            else:
                if self.not_corrupted(receveid_data[4].encode(), receveid_data[0]) and receveid_data[1] == self.num_seq:
                    self.num_seq = not self.num_seq
                    self.wait_ack = False
                

                
                     
                    
    
            
    


    def checksum(self, data):
        checksum_value = sum(data) & 0xFF
        return checksum_value

    def not_corrupted(self, data, receveid_checksum):
        calculated_checksum = self.checksum(data)
        if int(receveid_checksum) == int(calculated_checksum):
            return True
        else:
            return False
        

    def send_ack(self, sender_ip, num_seq):
        message = f"{num_seq}  | ACK | {sender_ip}"
        checksum = self.checksum(message.split(" | ").encode())
        ack = f"{checksum} | " + message
        self.socket.sendto(ack.encode(), (self.network_address, self.port))





if __name__ == "__main__": 
    host = Host()
    thread = threading.Thread(target=host.receive_message)
    thread.start()
    time.sleep(1)
    connect_message = "CONNECTION"
    host.socket.sendto(connect_message.encode(), (host.network_address, host.port))



    while encerrarPrograma == False:
        opcao = input("-------------------MENU-------------------------- \n 1 - Enviar mensagem\n 2 - Encerrar programa")
        if opcao == "1":
            ip = str(input("Digite o ip do destinatário:\n\n"))
            host.wait_ack = True
            message = input("Digite a mensagem a ser enviada:\n\n")
            host.send_message(ip, message )

        elif opcao == "2":
            encerrarPrograma = True
            thread.join()