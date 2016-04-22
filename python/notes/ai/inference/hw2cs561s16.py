# Author : Thamme Gowda N
# Topic  : CSCI561 Spring 2016, Homework 2
# Email  : tnarayan@usc.edu
#
# Some of the code is taken from AIMA textbook http://aima.cs.berkeley.edu/python/logic.html
from argparse import ArgumentParser
import copy


class Statement(object): # just a parent class
    pass

class AtomicStatement(Statement):

    def __init__(self, name, args):
        self.args = args
        self.name = name

    def substitute(self, vals):
        for idx, arg in enumerate(self.args):
            if arg in vals:
                self.args[idx] = vals[arg]

    def format(self, theta):
        argf = lambda arg: "_" if arg[0].islower() and arg not in theta else arg
        return "%s(%s)" % (self.name, ", ".join(map(argf, self.args)))

    def __repr__(self):
        return str({"name": self.name, "args": self.args})

class ImplicationStatement(AtomicStatement):

    def __init__(self, name, args, lhs=None):
        super(ImplicationStatement, self).__init__(name, args)
        self.lhs = lhs

    def __repr__(self):
        data = eval(AtomicStatement.__repr__(self))
        data['lhs'] = self.lhs
        return str(data)

class KnowledgeBase(object):

    def __init__(self):
        self.rules = []
        self.counter = 0

    def tell(self, rule):
        self.rules.append(rule)

    def fetch_rules_for_goal(self, query):
        for rule in self.rules:
            if rule.name == query.name:
                yield copy.deepcopy(rule)

    def ask(self, query, outfile, debug=False):
        with open(outfile, 'w') as outfile:
            ie = InferenceEngine(self, outfile, debug)
            qs = query if type(query) == list else [query]
            res = False
            for q in qs:
                for res in ie.fol_bc_or(q, {}):
                    if res: # One poof is sufficient
                        break
                if not res: # if one part of AND compound fails, stop
                    break

            lastline = "True" if res else "False"
            outfile.write(lastline)
            if debug:
                print(lastline)
            return res

    def __repr__(self):
        return str({"n": len(self.rules), "rules": self.rules })

class InferenceEngine(object):

    def __init__(self, kb, logfile=None, debug=False):
        self.kb = kb
        self.used_vars = set()   # set of all used vars
        self.counter = 1         # for generating new vars
        self.logfile = logfile
        self.debug = debug

    def log(self, message):
        if self.debug or not self.logfile:
            print(message)
        if self.logfile:
            self.logfile.write(message)
            self.logfile.write("\r\n")

    def fol_bc_or(self, goal, theta):
        self.log("Ask: " + goal.format(theta))
        self.used_vars.update(goal.args)
        found = False
        truenum = 0
        for rule in self.kb.fetch_rules_for_goal(goal):
            rule = self.standardize_variables(rule)
            unified = self.unify(goal, rule, copy.deepcopy(theta))
            if unified:
                truenum += 1
                if truenum > 1:
                    self.log("Ask: "+ goal.format(theta))
                newthetas = [unified]
                if isinstance(rule, ImplicationStatement):
                    newthetas = self.fol_bc_and(rule.lhs, unified)
                for newtheta in newthetas:
                    self.log("True: " + self.substitute(newtheta, goal).format(theta))
                    found = True
                    yield newtheta
        if not found:
            self.log("False: " + goal.format(theta))
            yield None


    def fol_bc_and(self, goal, theta):
        if theta == None:
            return
        elif len(goal) == 0: yield theta
        else:
            first,rest = goal[0],goal[1:]
            for x in self.fol_bc_or(self.substitute(theta,first), copy.deepcopy(theta)):
                for y in self.fol_bc_and(copy.deepcopy(rest), copy.deepcopy(x)):
                    yield y

    def substitute(self, theta, rule):
        rule = copy.deepcopy(rule)
        for idx,arg in enumerate(rule.args):
            while arg in theta:
                rule.args[idx] = theta[arg]
                arg = theta[arg]
        return rule

    def unify(self, x, y, theta):
        if theta is None:
            return None #Failure
        elif x == y:
            return theta
        elif type(x) is str and x[0].islower():
            return self.unify_var(x, y, theta)
        elif type(y) is str and y[0].islower():
            return self.unify_var(y, x, theta)
        elif isinstance(x, Statement) and isinstance(y, Statement):
            return self.unify(x.args, y.args, self.unify(x.name, y.name,theta))
        elif type(x) is list  and type(y) is list:
            return self.unify(x[1:], y[1:], self.unify(x[0], y[0], theta))
        else:
            return None

    def unify_var(self, var, x, theta):
        if  var in theta:
            return self.unify(theta[var],x,theta)
        elif x in theta:
            return self.unify(var,theta[x],theta)
        else :
            theta[var]=x
            return theta

    def standardize_variables(self, rule):
        change={}
        tempvar=set()
        for i, arg in enumerate(rule.args):
            if arg in self.used_vars and arg[0].islower() :
                change[arg]=self.new_var()
                rule.args[i]=change[arg]
            else:
                tempvar.add(arg)

        if type(rule) == ImplicationStatement:
            for subrule in rule.lhs:
                for idx, arg in enumerate(subrule.args):
                    if arg in change:
                        subrule.args[idx] = change[arg]
                    elif arg not in tempvar and arg in self.used_vars and arg[0].islower():
                        newvar = self.new_var()
                        change[arg]= newvar
                        subrule.args[idx] = newvar
        self.used_vars.update(tempvar)
        return (rule)

    def new_var(self):
        self.counter += 1
        newvar = "x%d" % self.counter
        self.used_vars.add(newvar)
        return newvar

class QueryParser(object):

    def parse(self, line):
        line = line.strip()
        if " => " in line:   # implication statement
            return self.parse_implication(line)
        elif " && " in line:  # found in query
            return map(lambda x:self.parse_atomic(x), line.split(" && "))
        else:                  # Atomic statement
            return self.parse_atomic(line)

    def parse_implication(self, sentence, statement=None):
        if not statement:
            statement = ImplicationStatement(None, None)
        parts = sentence.split(" => ")
        self.parse_atomic(parts[1], statement) # rhs is atomic
        statement.lhs = map(lambda x: self.parse_atomic(x),
                            parts[0].split(" && "))
        return statement

    def parse_atomic(self, sentence, statement=None):
        if not statement:
            statement = AtomicStatement(None, None)
        statement.name = sentence[:sentence.index("(")]
        statement.args = map(lambda x: x.strip(),
                             sentence[sentence.index("(")+1 : sentence.index(")")].split(", "))
        return statement

    def parse_input(self, in_file):
        with open(in_file) as in_file:
            lines = in_file.readlines()
            #line 0 is query
            kb = KnowledgeBase()
            qry = self.parse(lines[0])
            nrules = int(lines[1].strip())
            for l in lines[2: 2 + nrules]:
                kb.tell(self.parse(l))
            return (qry, kb)

if __name__ == "__main__":
    parser = ArgumentParser(usage="CSCI561-2016-1 HW2 Solutions by Thamme Gowda N.")
    parser.add_argument("-i", "--input", help="Path to input file", required=True)
    parser.add_argument("-o", "--output", help="Path to output/log file", required=False, default="output.txt")
    args = vars(parser.parse_args())
    qry, kb = QueryParser().parse_input(args["input"])
    kb.ask(qry, args["output"], debug=True)






