

def counting_sort(A: list, B: list, n: int):
    minA = min(A)
    maxA = max(A)
    k = maxA - minA + 1
    C = [0] * k
    for j in range(n):
        C[A[j]-minA] += 1
    for i in range(1, k):
        C[i] = C[i] + C[i - 1]
    for j in range(n):
        B[C[A[j] - minA] - 1] = A[j]
        C[A[j]-minA] -= 1




if __name__ == "__main__":
    n = 10
    A = [0, 7, 1, 6, 7, 7, 6, 6, 5, 4]
    B = [None] * len(A)
    counting_sort(A, B, n)
    print(B)