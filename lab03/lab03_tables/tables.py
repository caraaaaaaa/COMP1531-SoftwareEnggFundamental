import random
num1 = random.randint(2, 12)
num2 = random.randint(2, 12)


answer = int(input(f'What is {num1} x {num2}? '))

while answer != (num1 * num2):
    print('Incorrect - try again.')
    answer = int(input(f'What is {num1} x {num2}? '))

print('Correct!')