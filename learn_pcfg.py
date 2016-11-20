__author__ = 'TuWei'

import sys

def main():

    # 1.read file from config_train
    input = open(sys.argv[1],'r')
    lines = input.readlines()
    input.close()

    # 2.
    s = []
    current = []
    results = {}
    buf = ''
    for line in lines:
        for char in line:
            if char == '(':
                if len(buf):
                    current.append(buf)
                    buf = ''
                s.append(current)
                current = []
            elif char == ')':
                if len(buf):
                    current.append(buf)
                    buf = ''
                left = current[0]
                if len(current) == 2:
                    right = current[1].lower()
                else:
                    right = ' '.join(current[1:])
                if not left in results:
                    results[left] = {}
                if not right in results[left]:
                    results[left][right] = 0
                results[left][right] += 1
                tmp = current[0]
                current = s.pop()
                current.append(tmp)
            elif char == ' ':
                if len(buf):
                    current.append(buf)
                    buf = ''
            else:
                buf += char

    # 3. write the result into output
    output = open(sys.argv[2], 'w')
    for result in results:
        total = 0
        rights = results[result]
        for right in rights:
            total += rights[right]
        for right in rights:
            output.write(result+" # " + right + " # " + str(float(rights[right])/total) + '\n')
    output.close()

if __name__ == '__main__':
    main()

