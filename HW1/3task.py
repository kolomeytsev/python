
import sys


def make_poliz(expression):
    stack = []
    res = []
    operators = ['+', '-', '*', '/', '(', ')', '**']
    tokens = input.strip().split()
    for elem in tokens:
        if elem not in operators:
            res.append(float(elem))
        elif elem == '(':
            stack.append('(')
        elif elem == ')':
            top = stack.pop()
            while top != '(':
                res.append(top)
                top = stack.pop()
        elif elem in ['+', '-']:
            while len(stack) > 0:
                if stack[-1] in ['+', '-', '*', '/', '^']:
                    res.append(stack.pop())
                else:
                    break
            stack.append(elem)
        elif elem in ['*', '/']:
            while len(stack) > 0:
                if stack[-1] in ['*', '/', '^']:
                    res.append(stack.pop())
                else:
                    break
            stack.append(elem)
        else:
            stack.append('^')
    while len(stack) > 0:
        res.append(stack.pop())
    return res


def interpret(expression):
    poliz = make_poliz(expression)
    stack = []
    for i in range(len(poliz)):
        elem = poliz[i]
        if elem not in ['+', '-', '*', '/', '^']:
            stack.append(elem)
        else:
            operand1 = stack.pop()
            operand2 = stack.pop()
            if elem == '+':
                res = operand1 + operand2
            if elem == '-':
                res = operand2 - operand1
            if elem == '*':
                res = operand1 * operand2
            if elem == '/':
                res = float(operand2) / operand1
            if elem == '^':
                res = operand2**operand1
            stack.append(res)
    return stack[-1]


input = sys.stdin.readline()
if len(input) > 0:
    x = interpret(input)
    print x
