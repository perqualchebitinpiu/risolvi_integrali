#Description: Programma che risolve integrali step by step

from lark import Lark, Transformer
import sympy as sym
import copy


grammar = """start: expr
             expr: add  | sub | term
             term: mul  | div |  term2
             term2: pow  | fact | fnt
             fact: xvar |value | round_paren_expr 
             round_paren_expr: "(" expr ")"     
             pow:  term2 "^" fact
             mul:  term "*" term2
             div:  term "/" term2
             add:  term "+" expr
             sub:  term "-" expr
             fnt: sin_f | cos_f |sinh_f |cosh_f | tanh_f | coth_f 
                | tg_f | cotg_f | arcsin_f 
                | arccos_f | arctg_f | arccotg_f | ln_f | exp_f

             sinh_f: "sinh" "(" expr ")"
             cosh_f: "cosh" "(" expr ")"
             tanh_f: "tanh" "(" expr ")"
             coth_f: "coth" "(" expr ")"
             sin_f: "sin" "(" expr ")" 
             cos_f: "cos" "(" expr ")"
             tg_f: "tan" "(" expr ")"
             cotg_f: "cot" "(" expr ")"
             arcsin_f: "asin" "(" expr ")"
             arccos_f: "acos" "(" expr ")"
             arctg_f: "atan" "(" expr ")"
             arccotg_f: "acot" "(" expr ")"

             ln_f: "ln" "(" expr ")"
             exp_f: "exp" "(" expr ")"
            
             value : SIGNED_NUMBER            
             xvar  : "x"
             %import common.SIGNED_NUMBER             
             %import common.WS
             %ignore WS
            
              """



class toOp_transformer(Transformer):
    def expr(self, terms): 
        return (terms[0])
    def term2(self, terms): 
        return (terms[0])
    def term(self, terms): 
        return (terms[0])
    def fact(self, terms): 
        return (terms[0])
    def round_paren_expr(self, terms): 
        return terms[0]
    def mul(self, terms):                
        return ["N","*", terms[0], terms[1]]
    def add(self, terms):                
        return ["N","+", terms[0], terms[1]]
    def sub(self, terms):                
        return ["N","-", terms[0], terms[1]]
    def div(self, terms):                
        return ["N","/", terms[0], terms[1]]
    def pow(self, terms):                
        return ["N","^", terms[0], terms[1]]
    def fnt(self, terms):                
        return (terms[0])
    def sin_f(self, terms): 
        return ["N","SIN", terms[0],None]

    def tg_f(self, terms): 
        return ["N","TG", terms[0],None]
    def cotg_f(self, terms): 
        return ["N","COTG", terms[0],None]
    def arcsin_f(self, terms): 
        return ["N","ARCSIN", terms[0],None]
    def arccos_f(self, terms): 
        return ["N","ARCCOS", terms[0],None]
    def arctg_f(self, terms): 
        return ["N","ARCTG", terms[0],None]
    def arccotg_f(self, terms): 
        return ["N","ARCCOTG", terms[0],None]
    def sinh_f(self, terms): 
        return ["N","SINH", terms[0],None]
    def cosh_f(self, terms): 
        return ["N","COSH", terms[0],None]
    def tanh_f(self, terms): 
        return ["N","TANH", terms[0],None]

    def coth_f(self, terms): 
        return ["N","COTH", terms[0],None]
    def ln_f(self, terms): 
        return ["N","LN", terms[0],None]
    def exp_f(self, terms): 
        return ["N","EXP", terms[0],None]
    def cos_f(self, terms): 
        return ["N","COS", terms[0],None]
    def xvar(self,terms):
        return ["N","VAR","x"]
    def value(self, val):
        val  = float(val[0])
        if val.is_integer():
            return ["N","CONST",int(val)]
        else:
            return ["N","CONST",val]



parser = Lark(grammar)




def get_expr(node):
    if node != None:
        expr = ""
        if node[0] == "D":
            expr += "D[" 

        if node[1] == "COS":
            expr += "cos(" +  get_expr(node[2]) + ")"
        elif node[1] == "SIN":
            expr += "sin("+  get_expr(node[2]) + ")"

        elif node[1] == "TG":
            expr += "tan("+  get_expr(node[2]) + ")"
        elif node[1] == "COTG":
            expr += "cot("+  get_expr(node[2]) + ")"
        elif node[1] == "ARCSIN":
            expr += "asin("+  get_expr(node[2]) + ")"
        elif node[1] == "ARCCOS":
            expr += "acos("+  get_expr(node[2]) + ")"
        elif node[1] == "ARCTG":
            expr += "atan("+  get_expr(node[2]) + ")"
        elif node[1] == "ARCCOTG":
            expr += "acot("+  get_expr(node[2]) + ")"
        elif node[1] == "SINH":
            expr += "sinh("+  get_expr(node[2]) + ")"
        elif node[1] == "COSH":
            expr += "cosh("+  get_expr(node[2]) + ")"
        elif node[1] == "TANH":
            expr += "tanh("+  get_expr(node[2]) + ")"
        elif node[1] == "COTH":
            expr += "coth("+  get_expr(node[2]) + ")"
        elif node[1] == "LN":
            expr += "ln("+  get_expr(node[2]) + ")"
        elif node[1] == "EXP":
            expr += "exp("+  get_expr(node[2]) + ")"
        elif node[1] == "-U":
            expr1 = get_expr(node[2]) 
            if node[2][1] in ["+","-"]:
                expr1 = "(" + expr1 + ")"
            expr += "-" + expr1 
        elif node[1] == "+":
            expr += get_expr(node[2]) +"+" +get_expr(node[3])
        elif node[1] == "-":
            expr += get_expr(node[2]) +"-" +get_expr(node[3])

        elif node[1] == "^":
            expr1 = get_expr(node[2])
            if node[2][1] in [["+","-","*","/"]]:
                expr1 = "(" + expr1 + ")"
            expr2 = get_expr(node[3])
            if node[3][1] in ["+","-","*","/"]:
                expr2 = "(" + expr2 + ")"
            expr +=  expr1+"^" +expr2

        elif node[1] == "*":
            expr1 = get_expr(node[2])
            if node[2][1] in ["+","-"]:
                expr1 = "(" + expr1 + ")"
            expr2 = get_expr(node[3])
            if node[3][1] in ["+","-"]:
                expr2 = "(" + expr2 + ")"
            expr +=  expr1+"*" +expr2
        elif node[1] == "/":
            expr1 = get_expr(node[2])
            if node[2][1] in ["+","-"]:
                expr1 = "(" + expr1 + ")"
            expr2 = get_expr(node[3])
            if node[3][1] in ["+","-"]:
                expr2 = "(" + expr2 + ")"
            expr +=  expr1+"/" +expr2

        if node[1] == "CONST":
            expr += str(node[2])
        if node[1] == "VAR":
            expr += "x"
        if node[0] == "D":
            expr += "]"

        return expr
    else:
        return ""    

def compute_diff(node):
    node[0]= "N"
    if node[1] == "+" or node[1] == "-":  #deriva entrambi i termini
        node[2][0] = "D"
        node[3][0] = "D"
    elif node[1] == "*": 
        #copia tutte le sotto espressioni
        #fattori non derivati
        fact_a_n  = copy.deepcopy(node[2])
        fact_b_n  = copy.deepcopy(node[3])
        #fattori derivati
        fact_a_d = node[2]
        fact_b_d  = node[3]
        fact_a_d[0]= "D"        
        fact_b_d[0]= "D"

        node[1] = "+"

        node[2] = ["N","*",fact_a_d,fact_b_n]
        node[3] = ["N","*",fact_a_n,fact_b_d]
    elif node[1] == "^": 
        #copia tutte le sotto espressioni
        #fattori non derivati
        fact_f_n  = copy.deepcopy(node[2])
        fact_g_n  = copy.deepcopy(node[3])
        #fattori derivati
        fact_f_d = node[2]
        fact_g_d  = node[3]
        fact_f_d[0]= "D"        
        fact_g_d[0]= "D"

        node[1] = "*"

        node[2] = ["N","^",fact_f_n,["N","-",fact_g_n,["N","CONST",1]]]
        node_log = ["N", "*", fact_f_n,["N","*",fact_g_d,["N","LN",fact_f_n,None]]]
        node[3] = ["N","+",["N","*",fact_g_n,fact_f_d],node_log]
    elif node[1] == "/": 
        #copia tutte le sotto espressioni
        #fattori non derivati
        fact_a_n  = copy.deepcopy(node[2])
        fact_b_n  = copy.deepcopy(node[3])
        #fattori derivati
        fact_a_d = node[2]
        fact_b_d  = node[3]
        fact_a_d[0]= "D"        
        fact_b_d[0]= "D"

        node[1] = "/"

        node[2] = ["N","-",["N","*",fact_a_d,fact_b_n], ["N","*",fact_a_n,fact_b_d] ]
        node[3] = ["N","^",fact_b_n,["N","CONST",2]]

    elif node[1] == "COS": #la derivata di cos(f(x)) = -sin(f(x))*D[f(x)]
        #funzione interna non derivata
        f_n  = copy.deepcopy(node[2])
        #funzione interna da derivare
        f_d  = node[2]
        f_d[0] = "D"
        
        node[1] = "-U"
        node[2] = ["N","*",["N","SIN",f_n,None],f_d]
###########################
    elif node[1] == "TG": #la derivata di cos(f(x)) = -sin(f(x))*D[f(x)]
        #funzione interna non derivata
        f_n  = copy.deepcopy(node[2])
        #funzione interna da derivare
        f_d  = node[2]
        f_d[0] = "D"
               
        node = ["N","*",["N","/",["N","CONST",1],["N","^",["N","COS",f_n,None],["N","CONST",2]]],f_d]
    elif node[1] == "COTG": #la derivata di cos(f(x)) = -sin(f(x))*D[f(x)]
        #funzione interna non derivata
        f_n  = copy.deepcopy(node[2])
        #funzione interna da derivare
        f_d  = node[2]
        f_d[0] = "D"
               
        node = ["N","*",["N","/",["N","CONST",-1],["N","^",["N","SIN",f_n,None],["N","CONST",2]]],f_d]
    elif node[1] == "ARCTG": #la derivata di cos(f(x)) = -sin(f(x))*D[f(x)]
        #funzione interna non derivata
        f_n  = copy.deepcopy(node[2])
        #funzione interna da derivare
        f_d  = node[2]
        f_d[0] = "D"
               
        node = ["N","*",["N","/",["N","CONST",1],["N","+",["N","^",f_n,["N","CONST",2]],["N","CONST",1]]],f_d]
    elif node[1] == "ARCCOTG": #la derivata di cos(f(x)) = -sin(f(x))*D[f(x)]
        #funzione interna non derivata
        f_n  = copy.deepcopy(node[2])
        #funzione interna da derivare
        f_d  = node[2]
        f_d[0] = "D"
               
        node = ["N","*",["N","/",["N","CONST",-1],["N","+",["N","^",f_n,["N","CONST",2]],["N","CONST",1]]],f_d]
    elif node[1] == "LN": #la derivata di cos(f(x)) = -sin(f(x))*D[f(x)]
        #funzione interna non derivata
        f_n  = copy.deepcopy(node[2])
        #funzione interna da derivare
        f_d  = node[2]
        f_d[0] = "D"
               
        node = ["N","*",["N","/",["N","CONST",1],f_n],f_d]
    elif node[1] == "SINH": #la derivata di cos(f(x)) = -sin(f(x))*D[f(x)]
        #funzione interna non derivata
        f_n  = copy.deepcopy(node[2])
        #funzione interna da derivare
        f_d  = node[2]
        f_d[0] = "D"
               
        node = ["N","*",["N","COSH",f_n,None],f_d]

    elif node[1] == "COSH": #la derivata di cos(f(x)) = -sin(f(x))*D[f(x)]
        #funzione interna non derivata
        f_n  = copy.deepcopy(node[2])
        #funzione interna da derivare
        f_d  = node[2]
        f_d[0] = "D"
               
        node = ["N","*",["N","SINH",f_n,None],f_d]
    elif node[1] == "EXP": #la derivata di cos(f(x)) = -sin(f(x))*D[f(x)]
        #funzione interna non derivata
        f_n  = copy.deepcopy(node[2])
        #funzione interna da derivare
        f_d  = node[2]
        f_d[0] = "D"
               
        node = ["N","*",["N","EXP",f_n,None],f_d]
    elif node[1] == "TANH": #la derivata di cos(f(x)) = -sin(f(x))*D[f(x)]
        #funzione interna non derivata
        f_n  = copy.deepcopy(node[2])
        #funzione interna da derivare
        f_d  = node[2]
        f_d[0] = "D"
               
        node = ["N","*",["N","/",["N","CONST",1],["N","^",["N","COSH",f_n,None],["N","CONST",2]]],f_d]

    elif node[1] == "COTH": #la derivata di cos(f(x)) = -sin(f(x))*D[f(x)]
        #funzione interna non derivata
        f_n  = copy.deepcopy(node[2])
        #funzione interna da derivare
        f_d  = node[2]
        f_d[0] = "D"
               
        node = ["N","*",["N","/",["N","CONST",-1],["N","^",["N","SINH",f_n,None],["N","CONST",2]]],f_d]
    elif node[1] == "SIN": #la derivata di cos(f(x)) = -sin(f(x))*D[f(x)]
        #funzione interna non derivata
        f_n  = copy.deepcopy(node[2])
        #funzione interna da derivare
        f_d  = node[2]
        f_d[0] = "D"
               
        node = ["N","*",["N","COS",f_n,None],f_d]
    elif node[1] == "CONST": #la derivata della costante diventa zero
        node[2] = 0
    elif node[1] == "VAR": #la derivata della varibile X è 1
        node[1] = "CONST"
        node[2] = 1

    return node

def diff_step(node):
    if node != None:
        if node[0] == "D":
            return compute_diff(node)
        else:
            if not(node [1] in ["CONST","VAR"]):
                node[2] = diff_step(node[2])
                node[3] = diff_step(node[3])
                return node
            else:
                return node
    else:
        return None

if  __name__ == "__main__":
    line = "x^2"
    print(line)
    tree = parser.parse(line)
    print(tree.pretty())
    op_tree = toOp_transformer().transform(tree)

    root = op_tree.children[0]  
    root[0] = "D"
    #print(root)
    print(get_expr(root))
    root = diff_step(root)
    #print(root)
    print(get_expr(root))
    root = diff_step(root)
    #print(root)
    print(get_expr(root))
    root = diff_step(root)
    #print(root)
    print(get_expr(root))
    root = diff_step(root)
    print(get_expr(root))
    root = diff_step(root)

    #print(root)
    print("my_diff: \t\t\t" + get_expr(root))    
    vers1 = sym.simplify(get_expr(root))
    vers2 = sym.diff(line)
    print("my_diff simply:\t"+ str(vers1))
    print("sympy simply:\t"+ str(vers2))

    print((sym.simplify(vers1-vers2) == 0))

    #print("sympy integrate:\t"+ str(sym.integrate(sym.simplify(get_expr(root)))))

