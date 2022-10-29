chars = '123456가7812나0123'

def tt():
    if len(chars) == 7:
        if chars[0].isdigit() and \
                chars[1].isdigit() and \
                ord('가') <= ord(chars[2]) <= ord('힣') and \
                chars[3].isdigit() and \
                chars[4].isdigit() and \
                chars[5].isdigit() and \
                chars[6].isdigit():
            has_digit = True
            result_chars = chars
            print(result_chars)

    elif len(chars) == 8:
        if chars[0].isdigit() and \
                chars[1].isdigit() and \
                chars[2].isdigit() and \
                ord('가') <= ord(chars[3]) <= ord('힣') and \
                chars[4].isdigit() and \
                chars[5].isdigit() and \
                chars[6].isdigit() and \
                chars[7].isdigit():
            has_digit = True
            result_chars = chars
            print(result_chars)
    elif len(chars) <= 30:
        for i in range(0, len(chars)-6):
            if chars[i].isdigit() and \
                    chars[i+1].isdigit() and \
                    ord('가') <= ord(chars[i+2]) <= ord('힣') and \
                    chars[i+3].isdigit() and \
                    chars[i+4].isdigit() and \
                    chars[i+5].isdigit() and \
                    chars[i+6].isdigit():
                print(chars[i+6])
                has_digit = True
                result_chars = chars[i:i+7]
                print(result_chars)
                break

        # for i in range(0, len(chars) - 7):
        #     if chars[i].isdigit() and \
        #             chars[i + 1].isdigit() and \
        #             chars[i + 2].isdigit() and \
        #             ord('가') <= ord(chars[i + 3]) <= ord('힣') and \
        #             chars[i + 4].isdigit() and \
        #             chars[i + 5].isdigit() and \
        #             chars[i + 6].isdigit() and \
        #             chars[i + 7].isdigit():
        #         print(chars[i + 7])
        #         has_digit = True
        #         result_chars = chars[i:i + 8]
        #         print(result_chars)
        #         return









tt()