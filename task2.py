def is_polindrome(number):
    if list(str(number)) == list(str(number))[::-1]:
        return True
    else:
        return False

print(is_polindrome(1221))