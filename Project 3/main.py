import sys

class CSP:
    
    def __init__(self, variables, constraints, forwardCheck):
        self.variables = variables
        self.constraints = constraints
        self.forwardCheck = forwardCheck
        self.unassign = variables.keys()

def complete(assignment, csp):
    complete = False
    if len(assignment.keys()) == len(csp.variables.keys()): # If there still unassigned variable
       complete = True
    return complete

def consistent(assignment, csp):
    complete = True
    # for each constraints, check if assignment is consistent
    for constraint in csp.constraints: 
        if constraint[5] == "==" and constraint[2] in assignment.keys() and constraint[6] in assignment.keys():
            if not (int(constraint[0]) * int(assignment[constraint[2]]) + int(constraint[4]) == int(assignment[constraint[6]])):
                complete = False
        if constraint[5] == "!=" and constraint[2] in assignment.keys() and constraint[6] in assignment.keys():
            if not (int(constraint[0]) * int(assignment[constraint[2]]) + int(constraint[4]) != int(assignment[constraint[6]])):
                complete = False
        if constraint[5] == "<=" and constraint[2] in assignment.keys() and constraint[6] in assignment.keys():
            if not (int(constraint[0]) * int(assignment[constraint[2]]) + int(constraint[4]) <= int(assignment[constraint[6]])):
                complete = False
        if constraint[5] == ">=" and constraint[2] in assignment.keys() and constraint[6] in assignment.keys():
            if not (int(constraint[0]) * int(assignment[constraint[2]]) + int(constraint[4]) >= int(assignment[constraint[6]])):
                complete = False
        if constraint[5] == "<" and constraint[2] in assignment.keys() and constraint[6] in assignment.keys():
            if not (int(constraint[0]) * int(assignment[constraint[2]]) + int(constraint[4]) < int(assignment[constraint[6]])):
                complete = False
        if constraint[5] == ">" and constraint[2] in assignment.keys() and constraint[6] in assignment.keys():
            if not (int(constraint[0]) * int(assignment[constraint[2]]) + int(constraint[4]) > int(assignment[constraint[6]])):
                complete = False

    return complete

def selectUnassignVariable(csp):
    
    if len(csp.unassign) == 1: # if only 1 unassign variable left
        temp = csp.unassign[0]
        csp.unassign.remove(temp) # remove from unassign list
        return temp # return the variable

    # MRV (Minimum-Remaining-Value) - select variable with smallest domain
    least = csp.unassign[0] # variable with smallest domain
    secondLeast = csp.unassign[1] # variable with second smallest domain
    for var in csp.unassign: # for each unssigned variable
        # if size of domain is less than least's domain, replace it
        if len(csp.variables[var]) < len(csp.variables[least]):
            secondLeast = least
            least = var
        # if size of domain is less than secondLeast's domain, replace it
        elif len(csp.variables[var]) < len.csp.variables[secondLeast]:
            secondLeast = var
        
    if least == secondLeast: # if tie
        # degree heuristic selects the variable involved in the highest number of constraints
        leastCounter = 0
        secondLeastCounter = 0
        # for each constraints count the number of appearences of the variables
        for c in csp.constraints: 
            if c[2] == least or c[6] == least:
                leastCounter = leastCounter + 1
            if c[2] == secondLeast or c[6] == secondLeast:
                secondLeastCounter = secondLeastCounter + 1
        
        if leastCounter > secondLeastCounter:
            return least
        else:
            return secondLeast
    
    return least

def orderDomainValue(var, csp):
    return {}

def backtrackingSearch(csp):
    return backtrack({}, csp)

def backtrack(assignment, csp):
    if complete(assignment, csp):
        return assignment

    var = selectUnassignVariable(csp)
    
    for value in orderDomainValue(var, csp):
        if csp.consistent(assignment):
            assignment[var].append(value)
    
    return False

def main():
    forwardCheck = False # flag to use forward checking (AC-3)
    variable = dict() # list of variables and its domain
    constraints = list() # list of binary constraints
    uConstraints = list() # list of unary constraints
    
    # Check if there are 3 arguments in the command line
    if len(sys.argv) != 3:
        print("Invalid missing or no arguments")
        sys.exit(1)
    
    # check for forward checking flag
    if sys.argv[2] == 1:
        forwardCheck = True
        
    try:
        # reads in lines of text file
        with open(sys.argv[1], "r") as file:
            data = file.readlines()
        # stores each line as an element of an array and remove any \n character
        for i in range(len(data)):
            data[i] = data[i].replace("\n", "")
            
    except FileNotFoundError: # file not found
        print("File Not Found")
        sys.exit(1)

    # parse the first line to get variables and domain
    temp = data[0].split(":")
    nameCount = 0
    for i in temp:
        varName = "X" + str(nameCount)
        nameCount = nameCount + 1
        domains = list() # temp list of domain for variable
        for j in range(int(i)):
            domains.append(j)
        variable[varName] = domains # add domain of variable into dictionary of variables

    print("Variables and domain:")
    for v in variable.keys():
        print(v, variable[v])
    print("\nConstraints:")
    
    # parse all contstraints
    for i in data[1:]:
        temp = i.split(" ")
        if "X" in temp[len(temp) - 1]: # if there is a second varibale
            print(temp)
            constraints.append(temp)
        else: # if there is only one variable
            print(temp)
            uConstraints.append(temp)

    removeUnary(variable, uConstraints) # remove all unary constraints
    
    csp = CSP(variable, constraints, forwardCheck)
    print(backtrackingSearch(csp))

def removeUnary(variable, uConstraints): # satisfy all unary constraints
    for u in uConstraints: # for each unary constraints
        for var in variable.keys(): # for each variable
            if var == u[2]: # if var is in the constraint
                for value in variable[var].copy(): # for each value in domain of variable
                    if u[5] == "==":
                        if not (int(u[0]) * int(value) + int(u[4]) == int(u[6])):
                            variable[var].remove(value)
                    elif u[5] == "!=":
                        if not (int(u[0]) * int(value) + int(u[4]) != int(u[6])):
                            variable[var].remove(value)
                    elif u[5] == "<=":
                        if not (int(u[0]) * int(value) + int(u[4]) <= int(u[6])):
                            variable[var].remove(value)
                    elif u[5] == ">=":
                        if not (int(u[0]) * int(value) + int(u[4]) >= int(u[6])):
                            variable[var].remove(value)
                    elif u[5] == "<":
                        if not (int(u[0]) * int(value) + int(u[4]) < int(u[6])):
                            variable[var].remove(value)
                    elif u[5] == ">":
                        if not (int(u[0]) * int(value) + int(u[4]) > int(u[6])):
                            variable[var].remove(value)      

main()
