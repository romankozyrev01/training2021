nums = iter([1, 2, 3, 4, 5])
while True:
    try:
        print(next(nums))
    except StopIteration:
        break
