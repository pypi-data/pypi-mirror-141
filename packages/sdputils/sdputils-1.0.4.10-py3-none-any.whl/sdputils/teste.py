up_idx = 1

print(f'Uploading:    ', end='\r')
for i in range(100):
    if up_idx < 4:
        up_str = '.' * up_idx
        print(f'Uploading: {up_str}', end='\r')
        up_idx += 1
    else:
        print(f'Uploading:    ', end='\r')
        up_idx = 1
    