# functions
def regex_check(regex, string):
    """checks if the regex and the string of same length match"""
    if regex and string:  # if both of them are not empty
        if len(regex) > 1 and regex[0] == "\\":  # there is an escape sequence
            return bool(regex[1] == string[0]) and regex_check(regex[2:], string[1:])  # comparing the escaped character
        elif len(regex) > 1 and regex[1] in metacharacters2:  # we have a metacharacter of repetition to handle
            if regex[1] == "?":
                if regex[0] == ".":  # very special case, we can remove a char from string or not
                    return regex_check(regex[2:], string[1:]) or regex_check(regex[2:], string)
                elif regex[0] == string[0]:  # the character exists so we remove it
                    return regex_check(regex[2:], string[1:])
                else:  # the char doesn't exist so we don't remove
                    return regex_check(regex[2:], string)
            elif regex[1] == "*":
                if regex[0] == ".":  # very special case, here we don't care about anything but the fact that the rest of the regex matches the end of the string
                    return regex_check(regex[2:], string[- len(regex[2:])])
                while regex[0] == string[0]:  # remove all the matching part
                    string = string[1:]
                return regex_check(regex[2:], string)
            elif regex[1] == "+":  # "+"
                if regex[0] == ".":  # very special case, here we remove at least a char then only care about the fact that the rest of the regex matches the end of the string
                    string = string[1:]  # remove one char
                    return regex_check(regex[2:], string[- len(regex[2:]):])
                elif regex[0] != string[0]:  # char doesn't exist
                    return False
                while regex[0] == string[0]:  # remove all the matching part
                    string = string[1:]
                return regex_check(regex[2:], string)
        elif regex[0] == "." or regex[0] == string[0]:  # comparing the [0] of them: wild card "." or they match
            return regex_check(regex[1:], string[1:])
        else:  # [0] doesn't match
            return False
    else:  # one/both are empty
        return bool(not regex or string)


def compare(regex_str, string_str):
    if string_str and any(char in metacharacters1 for char in regex_str):
        if "$" == regex_str[len(regex_str) - 1]:  # regex has metacharacter "$"
            if "^" == regex_str[0]:
                regex_str = regex_str[1:len(regex_str) - 1]  # remove the metacharacters from regex_str
            else:
                regex_str = regex_str[:len(regex_str) - 1]  # remove the metacharacter from regex_str
                if "\\" in regex_str:
                    string_str = string_str[- len(regex_str) + 1:] + " "  # capture the ending of string_str of equal length to regex_str
                else:
                    string_str = string_str[- len(regex_str):]  # capture the ending of string_str of equal length to regex_str
            if all(char not in metacharacters2 for char in regex_str):  # no repetition metacharacters
                return len(regex_str) == len(string_str) and regex_check(regex_str, string_str.strip())  # make sure the regex isn't longer then the string then match
            else:
                return regex_check(regex_str, string_str)  # make sure the regex isn't longer then the string then match
        elif "^" == regex_str[0]:  # regex has metacharacter "^"
            return regex_check(regex_str[1:], string_str)  # remove the metacharacter and match the beginnings
    elif regex_check(regex_str, string_str):  # if they match (no metacharacters)
        return True
    elif string_str[1:]:  # if the next string_str isn't empty
        return compare(regex_str, string_str[1:])
    else:  # the sting_str is empty
        return False


# write your code here
metacharacters1 = "^$"
metacharacters2 = "?+*"
input_str = input().strip()  # the input
input_list = input_str.split("|")  # contains the regex_str on [0] and the string_str on [1]
print(compare(input_list[0], input_list[1]))  # print result
