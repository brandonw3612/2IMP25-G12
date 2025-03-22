import numpy as np

def main():
    n = [30, 21, 137, 21, 2, 29, 4]
    mu = [0, 37, 660, 21, 0, 0, 0]
    a = np.divide(mu, np.power(n, 2))
    print("a = ")
    print(a)

    epsilon = [
        [0, 13, 71, 11, 0, 8, 2],
        [0, 0, 0, 2, 9, 23, 11],
        [0, 5, 0, 159, 0, 161, 3],
        [0, 0, 2, 0, 0, 14, 1],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ]
    ninj = np.multiply(n, np.transpose(np.atleast_2d(n)))
    e = np.divide(epsilon, 2 * ninj)
    print("e = ")
    print(e)

    mq = np.sum(a) / 7 - np.sum(e) / 21
    print("mq = ")
    print(mq)

if __name__ == "__main__":
    main()