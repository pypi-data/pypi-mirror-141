class VD:
    def __init__(self, vector = {}):
        self.vector = vector
    
    def dicc(self):
        print(self.vector)

    def __add__(self, P2):
        p1 = self.vector
        p2 = P2.vector
        result = {}
        m1 = list(p1.keys())[-1]
        m2 = list(p2.keys())[-1]
        m = max(m1, m2)
        for i in range(m + 1):
            if(i in p1.keys() and i in p2.keys()):
                result[i] = p1[i] + p2[i]
            elif(i in p1.keys()):
                result[i] = p1[i]
            elif(i in p2.keys()):
                result[i] = p2[i]
        return VD(result)


    def __str__(self):
        string = "."
        for x in self.vector:
            if(self.vector[x] > 0):
                string += " + "
            else:
                string += " - "
            string += "%dx^%d" % (abs(self.vector[x]), x)
        if(string[1:4] == " + "):
            subString = ". + "
            string = string.replace(subString, "")
        else:
            subString = ". - "
            string = string.replace(subString, "-")

        return string
    
def example():
    V = VD({2:5,3:-3,5:2})
    W = VD({2:3,3:5})

    V.dicc()
    print(V)
    print(W)
    print(V + W)