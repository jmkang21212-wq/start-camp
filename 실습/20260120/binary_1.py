t = input()
for i in range(t):
    num, hex_num = input().split()
    
    ten_num = int(hex_num, 16)       # 10진수로 변환
    bin_num = bin(ten_num)[2:]       # 2진수 문자열로 변환 ('0b' 제거)
    
    # 16진수 글자 수 * 4 만큼의 자릿수를 맞추고, 앞을 0으로 채움
    total_len = int(num) * 4
    result = bin_num.zfill(total_len) 
    
    print(f'#{i+1} {result}')