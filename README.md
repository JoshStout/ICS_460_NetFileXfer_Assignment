The program is made from two files provided for the assignment, NetFileXferClient.py and a NetFileXferServer.py. Both have been modifed to provide TLS encryption. The program is designed to transfer files from the client to the server. 

To generate self signed certificates, run the following command and use 'server' as the Common Name when making the certificate for the server and 'client' for the client certificate. Keep copies of both certificates in both the client and server folders. Store the server's key in the server folder, and store the client's key in the client folder.

>> openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout key.pem -out cert.pem

To run the NetFileXferServer.py program, go to the file location in a bash terminal and type the following:
>> python3 NetFileXferServer.py 12000

Next, go to the folder containing NetFileXferClient.py program and type in the following, with <FILE_PATH> being the path and file name you want sent to the server:
>> python3 NetFileXferClient.py localhost 12000 <FILE_PATH>
