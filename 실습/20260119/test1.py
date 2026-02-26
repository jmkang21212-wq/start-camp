a = 'jaemin kang'
print(f'Hello, {a}!')
print(f'a[:2] = {a[:2]}')
print(f'a[2:] = {a[2:]}')
print(f'a[8:2:-1] = {a[8:2:-1]}')
print(f'a[::-1] = {a[::-1]}')
print(f'a[-1:-2:-1] = {a[-1:-2:-1]}')
print(a)
print(len(a))
print(len(a.replace(' ', '')))

def split_name(full_name):
    first_name = full_name.split(' ')[0]
    last_name = full_name.split(' ')[1]
    return first_name, last_name

print(split_name(a))

    # a = input()
    # print('===>', a + 1
    #     )

a = int(input(a))
print('===>', a + 10)