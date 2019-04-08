import sys

def findGCD(a, b, step):
    a, b = max(a, b), min(a, b)

    # a = b * h + k
    h = a // b
    k = a % b
    record.append({'a': a, 'b': b, 'h': h, 'k': k})
    print('%d = %d * %d + %d ---- eq%d' % (a, b, h, k, step))

    if k == 1:
        return 1
    if k == 0:
        return b

    return findGCD(b, k, step+1)


'''
eq1: a = b * h + k
eq2: w * x + y * z = 1
'''
def substitute(eq1, eq2, step, extendedStep):
    # original eq1
    print('eq%d: %d = %d * %d + %d ---> ' % (step+1, eq1['a'], eq1['b'], eq1['h'], eq1['k']), end='')

    # transformed eq1
    eq1['h'] *= -1
    print('%d = %d + %d * %d' % (eq1['k'], eq1['a'], eq1['b'], eq1['h']))

    # original eq2
    print('Substitute eq%d into eq%d: %d * %d + %d * %d = 1' % (step+1, extendedStep, eq2['w'], eq2['x'], eq2['y'], eq2['z']))

    # substitute
    eq2['x'] = eq2['x'] + eq1['h'] * eq2['z']
    eq2['y'] = eq1['a']

    # swap
    eq2['w'], eq2['y'] = eq2['y'], eq2['w']
    eq2['x'], eq2['z'] = eq2['z'], eq2['x']

    # after substution
    print('---> %d * %d + %d * %d = 1 ---- eq%d' % (eq2['w'], eq2['x'], eq2['y'], eq2['z'], extendedStep+1), end='\n\n')

    if step == 0:
        return eq2['z']

    return substitute(record[step-1], eq2, step-1, extendedStep+1)


def modify(semiInverse, p):
    while semiInverse < 0:
        semiInverse += p
    return semiInverse


record = []
if __name__ == '__main__':
    a = int(input())
    p = 2 ** 1279 - 1

    # find gcd of a and p
    print('Calculating gcd(%d, %d)...' % (a, p))
    gcd = findGCD(a, p, 1)
    print('gcd(%d, %d) = %d' % (a, p, gcd), end='\n\n')

    if gcd != 1:
        print('The inverse of %d at mod %d does not exist.' % (a, p))
        sys.exit()
    if len(record) == 1:
        print('This problem cannot be solved by Extended Euclidean Algorithm, please check out the online modular calculator https://planetcalc.com/3311/')
        sys.exit()

    eq2 = {'w': record[-1]['a'], 'x': 1, 'y': record[-1]['b'], 'z': record[-1]['h']*(-1)}
    inverse = modify(substitute(record[-2], eq2, len(record)-2, len(record)), p)
    print('The inverse of %d at mod %d = %d' % (a, p, inverse))
