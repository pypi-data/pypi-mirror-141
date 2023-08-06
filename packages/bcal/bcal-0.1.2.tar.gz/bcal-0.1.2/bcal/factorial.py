def fact(n):
    f = 1
    while(n>=1):
        f = f * n
        n-= 1
    print(f)
def main():
    n = int(input("Enter a number: "))
    fact(n)
if __name__ == "__main__":
    main()