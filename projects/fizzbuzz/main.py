from typing import Generator

def fizzbuzz(define: dict, reps: range) -> Generator[int | str, None, None]:
    define = tuple(define.items())
    for i in reps:
        e = tuple(a for a, b in define if i % b == 0)
        yield i if e == () else ''.join(e)

def main():
    context = {'Fizz': 3, 'Buzz': 5}
    for i in fizzbuzz(context, range(100)):
        print(i)

if __name__ == '__main__':
    main()

