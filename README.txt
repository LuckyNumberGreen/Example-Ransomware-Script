Ransomware Simulation (ransomware.py)

Prerequisites:
Python 3 with OpenSSL installed on the system path (Kali Linux)
A dummy file named 'my_secrets.txt' in the working directory (automatically created if missing)

How to Run:
python3 ransomware.py

Behavior:
Automatically generates symmetric/asymmetric keys.
Encrypts 'my_secrets.txt' into 'data_cipher.txt' and deletes originals.
Displays the ransom note, pauses for 5 seconds simulating payment, and then automatically decrypts the files back to normal
