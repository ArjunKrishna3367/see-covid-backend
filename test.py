def evaluate(expression):
    expression = expression.strip()
    if (len(expression) == 0):
        return ""
    if ("+" not in expression and "&" not in expression):
        return "(?=.*" + expression + ")"
    if ("(" in expression):
        lCount = -1
        lIndex = expression.find("(")
        for i in range(lIndex, len(expression)):
            if (expression[i] == "("):
                lCount += 1
            if (expression[i] == ")"):
                if (lCount == 0):
                    rIndex = i
                    break
                lCount -= 1
        return evaluate(expression[:lIndex]) + "(" + evaluate(expression[lIndex + 1:rIndex]) + ")" + evaluate(expression[rIndex + 1:]) 
    if ("+" in expression):
        orIndex = expression.find("+")
        return evaluate(expression[:orIndex]) + "|" + evaluate(expression[orIndex + 1:])
    if ("&" in expression):
        andIndex = expression.find("&")
        search1 = expression[:andIndex].strip()
        search2 = expression[andIndex + 1:].strip()
        return evaluate(search1) + evaluate(search2)

print(evaluate("(China + Russia) & Trump"))