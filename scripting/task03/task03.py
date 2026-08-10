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