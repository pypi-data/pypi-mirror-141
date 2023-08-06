def fact(n):
    f = 1
    while(n>=1):
        f = f * n
        n-= 1
    print(f)
n = int(input("Enter a number: "))
fact(n)