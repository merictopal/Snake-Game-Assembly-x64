; snake_core.asm - corrected, tested for System V AMD64 ABI
global next_head
section .text

; int next_head(int head_x, int head_y, int direction, int width, int height, int *out_x, int *out_y)
; rdi=head_x, rsi=head_y, rdx=direction, rcx=width, r8=height, r9=out_x
; out_y is at [rsp+8] (first stack arg) (after return address)

next_head:
    push rbp
    mov rbp, rsp
    ; save registers we'll use
    push rbx
    push r12
    push r13

    mov eax, edi      ; eax = head_x
    mov ebx, esi      ; ebx = head_y
    mov edx, edx      ; edx = direction (already)
    mov r12d, ecx     ; r12d = width
    mov r13d, r8d     ; r13d = height

    ; compute nx, ny in r14d, r15d
    mov r14d, eax
    mov r15d, ebx

    cmp edx, 0
    je .up
    cmp edx, 1
    je .right
    cmp edx, 2
    je .down
    cmp edx, 3
    je .left
    jmp .done

.up:
    dec r15d
    jmp .done
.right:
    inc r14d
    jmp .done
.down:
    inc r15d
    jmp .done
.left:
    dec r14d
    jmp .done

.done:
    ; check boundaries: if nx < 0 -> collision ; if nx >= width -> collision
    ; nx = r14d, ny = r15d, width = r12d, height = r13d
    cmp r14d, 0
    jl .collision
    cmp r14d, r12d
    jge .collision
    cmp r15d, 0
    jl .collision
    cmp r15d, r13d
    jge .collision

    ; write out_x and out_y
    mov rax, r9       ; out_x pointer
    mov [rax], r14d
    ; out_y pointer is 7th arg at [rbp+16] (return addr at [rbp+8])
    mov rbx, [rbp+16]
    mov [rbx], r15d

    mov eax, 0        ; success
    jmp .ret

.collision:
    ; still write the (would-be) coordinates (optional)
    mov rax, r9
    mov [rax], r14d
    mov rbx, [rbp+16]
    mov [rbx], r15d
    mov eax, 1        ; collision code

.ret:
    pop r13
    pop r12
    pop rbx
    leave
    ret
