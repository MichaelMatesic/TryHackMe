# [TryHackMe | Scripting](https://tryhackme.com/room/scripting) Challenge Room Solution Writeup

## Task 1 \[Easy\] Base64

- Read input from file.
- Decode n=50 times.
- Use a loop.

### Python3 Solution

```python3
import base64

with open("b64_1550406728131.txt", "r") as f:
    b64_encoded = f.read().strip()

for i in range(50):
    b64_encoded = base64.b64decode(b64_encoded)

b64_decoded = b64_encoded if isinstance(b64_encoded, str) else b64_encoded.decode("utf-8")

print(f"Decoded: {b64_decoded}")
```

### Bash Solution

```bash
#!/bin/bash

b64_encoded=$(< "b64_1550406728131.txt")

for i in $(seq 1 50); do
    b64_encoded=$(base64 --decode <<< "$b64_encoded")
done

b64_decoded=$b64_encoded

echo "Decoded: $b64_decoded"
```

## Task 2 \[Medium\] Gotta Catch Em All

- Move through a sequence of ports, performing operations at each stop on a running number (starting at 0).
- Each port reports instructions of the form ```operation_type operation_value next_port```.
- Monitor port 3010 for its report on the currently live port in the sequence.
- Wait for the first port (1337) to become live.
- Traverse the sequence until reaching the last port (9765).
- Report the final running number.

```python3
import argparse
import re
import socket
import time
from typing import Union
from typing_extensions import Self

class PortHopper():
    """
    A class to handle port hopping on a target machine. It connects to a specified IP address and hops across ports based on 
    the responses received, performing arithmetic operations on a number until a STOP signal at the end port is reached.
    """

    def __init__(self: Self):
        """
        Initialize the PortHopper class by parsing command-line arguments and determining the address family of the provided IP address.

        :param self: Class self
        :type self: Self
        """
        # Parse command-line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument("ip", type = str, help = "Target machine IP address")
        parser.add_argument("-ph", "--port_home", type = int, default = 3010, help = "Target machine home port")
        parser.add_argument("-ps", "--port_start", type = int, default = 1337, help = "Target machine start port")
        parser.add_argument("-pe", "--port_end", type = int, default = 9765, help = "Target machine end port")
        parser.add_argument("-n", "--number", type = float, default = 0.0, help = "Starting number")
        parser.add_argument("-l", "--lifespan", type = float, default = 4.0, help = "Maximum time a port remains live")
        args = parser.parse_args()
        self.ip = args.ip
        self.port_home = args.port_home
        self.port_start = args.port_start
        self.port_end = args.port_end
        self.lifespan = args.lifespan
        self.number = args.number
        self._set_address_family()

        print(f"Starting.\nIP: {self.ip} | Home port: {self.port_home} | Start port: {self.port_start} | " \
              f"End port: {self.port_end} | Start number: {self.number:.2f} | Lifespan: {self.lifespan}")

    def _set_address_family(self: Self) -> None:
        """
        Determine the address family between IPv4 and IPv6.

        :param self: Class self
        :type self: Self
        :return: None
        :rtype: None
        """

        try:
            socket.inet_pton(socket.AF_INET, self.ip)
            self.address_family = socket.AF_INET
            return
        except OSError:
            pass

        try:
            socket.inet_pton(socket.AF_INET6, self.ip)
            self.address_family = socket.AF_INET6
            return
        except OSError:
            raise ValueError(f"Invalid IP address: {self.ip}")

    def _get_response(self: Self, port: int, timeout: float = 0.0) -> Union[str, None]:
        """
        Attempt to connect to a given IP and port to retrieve a response.

        :param self: Class self
        :type self: Self
        :param port: Port number
        :type port: int
        :param timeout: Connection timeout
        :type timeout: float
        :return: Response data if successful, None otherwise
        :rtype: str or None
        """

        try:
            with socket.socket(self.address_family, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                sock.connect((self.ip, port))
                request = f"GET / HTTP/1.1\r\nHost: {self.ip}\r\n\r\n"
                sock.send(request.encode("utf-8"))
                chunks: list[bytes] = []
                while True:
                    chunk = sock.recv(1024)
                    if not chunk:
                        break
                    chunks.append(chunk)
                response = b"".join(chunks).decode("utf-8").split("\r\n\r\n", 1)[1]
                return response
        except (socket.timeout, ConnectionRefusedError, OSError):
            return None

    def _get_live_port(self: Self) -> int:
        """
        Attempt to retrieve the live port from the target machine. If no response is received, retry after a short delay.

        :param self: Class self
        :type self: Self
        :return: Live port if successful, fallback to home port otherwise
        :rtype: int
        """

        port_live = self._get_response(self.port_home, self.lifespan / 2)
        if port_live is None:
            port_live = self.port_home
            print(f"No response from {self.ip}:{self.port_home}, retrying in {self.lifespan / 4} seconds.")
            time.sleep(self.lifespan / 4)
        else:
            port_live = int(re.search(r'id="onPort">(\d+)</a>', port_live).group(1))  # pyright: ignore[reportOptionalMemberAccess]
            print(
                f"\r\033[K"
                f"Start port: {self.port_start} | Live port: {port_live} | End port: {self.port_end}",
                end="",
                flush=True
            )
            time.sleep(self.lifespan / 10)
        return port_live
        
    def run(self: Self) -> None:
        """
        Main function to run the script. Jumps across ports on a target machine based on the response received, 
        performing arithmetic operations on a number until a STOP signal is received or port 9765 is reached.

        :param self: Class self
        :type self: Self
        :return: None
        :rtype: None
        """

        # Track the live port until it matches the start port.
        port_live = self.port_home
        while port_live != self.port_start:
            port_live = self._get_live_port()

        # Once the live port matches the start port, begin hopping across ports.
        port_last = self.port_home
        while True:
            port_live = self._get_live_port()

            if port_last == port_live:
                continue
            else:
                # Attempt to get a response from the new live port
                response = self._get_response(port_live, self.lifespan / 2)
                print(f"\r\nResponse from {self.ip}:{port_live}: {response}\r\n")

                # Peform checks on the response
                if response is None:
                    print(f"No response from {self.ip}:{port_live}, retrying in {self.lifespan / 4} seconds.")
                    time.sleep(self.lifespan / 4)
                    continue

                if response == "STOP":
                    print(f"Received STOP signal. Finished at:\nIP: {self.ip} | Port: {port_live} | Number: {self.number:.2f}")
                    break

                # Parse the response and perform the operation
                operation, value, _ = response.split()
                operation, value = operation.lower(), float(value)

                if operation == "add":
                    self.number += value
                    print(f"IP: {self.ip} | Port: {port_live} | Number: {self.number:.2f}")
                elif operation == "minus":
                    self.number -= value
                    print(f"IP: {self.ip} | Port: {port_live} | Number: {self.number:.2f}")
                elif operation == "multiply":
                    self.number *= value
                    print(f"IP: {self.ip} | Port: {port_live} | Number: {self.number:.2f}")
                elif operation == "divide":
                    self.number /= value
                    print(f"IP: {self.ip} | Port: {port_live} | Number: {self.number:.2f}")
                else:
                    raise ValueError(f"Unknown operation: {operation}")

                # Update the last port for the next iteration
                port_last = port_live

if __name__ == "__main__":
    port_hopper = PortHopper()
    port_hopper.run()
```

## Task 3 \[Hard\] Encrypted Server Chit Chat

- Connect to UDP server at port 4000.
- Initialize communications with ```b"hello"```.
- Request instructions with ```b"ready"```.
- Log the returned key, iv (initialization vector), and target SHA256 checksum. 
- Obtain ciphertext-tag pairs via two sequential ```b"final"``` requests.
- Decode pair using AES GCM and the [PyCA cyrptography](https://cryptography.io/en/latest/#) library.
- Compute the candidate SHA256 checksum (ensure same format between checksums such as hex).
- Iterate through these pairs until the candidate checksum matches the target.
- Report the corresponding decoded flag.

```python3
import argparse
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import hashlib
import re
import socket
from typing import Union
from typing_extensions import Self

class DecryptionSearch():
    """
    A class to handle decryption search on a target machine. It connects to a specified IP address and port, retrieves encryption parameters, 
    and decrypts data until a matching checksum is found.
    """

    def __init__(self: Self):
        """
        Initialize the DecryptionSearch class by parsing command-line arguments and determining the address family of the provided IP address.

        :param self: Class self
        :type self: Self
        """
        # Parse command-line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument("ip", type = str, help = "Target machine IP address")
        parser.add_argument("-p", "--port", type = int, default = 4000, help = "Target machine server port")
        args = parser.parse_args()
        self.ip = args.ip
        self.port = args.port
        self._set_address_family()
        self.host_ip = socket.gethostname().strip("ip-").replace("-", ".")

        print(f"Starting.\nHost IP: {self.host_ip} | Target IP: {self.ip} | Target port: {self.port}")

    def _set_address_family(self: Self) -> None:
        """
        Determine the address family between IPv4 and IPv6.

        :param self: Class self
        :type self: Self
        :return: None
        :rtype: None
        """

        try:
            socket.inet_pton(socket.AF_INET, self.ip)
            self.address_family = socket.AF_INET
            return
        except OSError:
            pass

        try:
            socket.inet_pton(socket.AF_INET6, self.ip)
            self.address_family = socket.AF_INET6
            return
        except OSError:
            raise ValueError(f"Invalid IP address: {self.ip}")

    def _request_response(self: Self, request: bytes, sock: socket.socket, verbose: bool = True) -> Union[bytes, None]:
        """
        Send a request to the target IP and port, and receive a response.

        :param self: Class self
        :type self: Self
        :param request: Request data to send
        :type request: bytes
        :param sock: Socket object for communication
        :type sock: socket.socket
        :return: Response data if successful, None otherwise
        :rtype: bytes or None
        """
        if verbose:
            print(f"{self.host_ip} ... {request}")
        sock.sendto(request, (self.ip, self.port))
        response = sock.recv(1024)
        if verbose:
            print(f"{self.ip}:{self.port} ... {response}")
        return response

    def run(self: Self, timeout: float = 60.0) -> None:
        """
        Run the decryption search process by connecting to the target IP and port, retrieving encryption parameters, 
        and decrypting data until a matching checksum is found.

        :param self: Class self
        :type self: Self
        :param timeout: Connection timeout
        :type timeout: float
        :return: None
        :rtype: None
        """

        try:
            with socket.socket(self.address_family, socket.SOCK_DGRAM) as sock:
                sock.settimeout(timeout)

                response = self._request_response(b"hello", sock)

                response = self._request_response(b"ready", sock)
                response = re.search(rb"key:(.*?) iv:(.*?) to decrypt and find the flag that has a SHA256 checksum of (.{32})", response) # pyright: ignore[reportArgumentType, reportUnknownVariableType, reportCallIssue]
                key, iv, checksum_target = response.group(1), response.group(2), response.group(3).hex() # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
                print(f"Key = {key} | IV = {iv} | Checksum = {checksum_target}")

                aesgcm = AESGCM(key) # pyright: ignore[reportUnknownArgumentType]
                checksum_candidate = b""
                print(f"Decrypting ...")
                while checksum_candidate != checksum_target:
                    ciphertext = self._request_response(b"final", sock, verbose = False)
                    tag = self._request_response(b"final", sock, verbose = False)
                    plaintext = aesgcm.decrypt(iv, ciphertext + tag, None) # pyright: ignore[reportOperatorIssue, reportUnknownArgumentType]
                    checksum_candidate = hashlib.sha256(plaintext).hexdigest()
                    print(f"Decrypted = {plaintext} | Checksum match = {checksum_candidate == checksum_target}")
                print(f"Checksum matched ... Flag: {plaintext.decode('utf-8')}") # pyright: ignore[reportPossiblyUnboundVariable]

        except (socket.timeout, ConnectionRefusedError, OSError):
            raise ValueError("Failed to retrieve response from the target.")

if __name__ == "__main__":
    decryptionsearch = DecryptionSearch()
    decryptionsearch.run()
```