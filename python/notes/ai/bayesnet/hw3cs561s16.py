#!/usr/bin/env python
#
#  This file includes solutions for HW3 for CSCI 561 course offered at USC.edu in Spring 2016
#  Student Name  : ThammeGowda Narayanaswamy
#  Student ID    : 2074-6674-39
#  Student Email : tnarayan@usc.edu
#
# Keywords : Bayes Network, Expected utility, Maximum expected utility, decision under uncertainty
#

from copy import copy, deepcopy
from argparse import ArgumentParser
from decimal import Decimal
from pprint import pprint

# Tokens in input file
QRY_SEP = "******"
NODE_SEP = "***"
GIVEN = "|"
TRUE = "+"
FALSE = "-"
JOINT = ","
EQUALS = "="
PROBABILITY = "P"
EXP_UTILITY = "EU"
MAX_EXP_UTILITY = "MEU"
NORM_NODE = "normal"
DEC_NODE = "decision"
UTILITY_NODE = "utility"
UNDECIDED = "?"

# Global vars
debug = False


def key_of(value, var):
    """
    Key for index/dictionary
    :param value: assignment
    :param var:  variable
    :return:
    """
    return "%s%s" % (value, var)


def format_float(val, digits=2):
    """
    Formats float number to stated precision after rounding it up
    :param val: value
    :param digits:  digits, default = 2
    :return: string formatted from floating point value
    """
    # format = "%" + (".%d" % digits) + "f"
    # return format % val
    if digits == 0:
        return "%d" % round(val)
    rounder = ['0' for i in range(0, digits-1)]
    rounder.append("1")
    rounder.insert(0, ".")
    rounder = "".join(rounder)
    return str(Decimal(str(val)).quantize(Decimal(rounder)))


def complement_value(value):
    """
    gets complemented assignment for given value
    :param value: value who's complement shall be found
    :return: complemented value
    :raises Exception when complement is unknown
    """
    if value == TRUE:
        return FALSE
    elif value == FALSE:
        return TRUE
    else:
        raise Exception("Complement unknown for %s" % value)


class Node(object):
    """
    Node class in bayes network
    """

    def __init__(self, name, cpt, _type='normal'):
        """
        Creates a node
        :param name: name for this node
        :param cpt: Conditional probability table
        :param _type: node type {'normal', 'decision', 'utility'}
        :return:
        """
        self._type = _type
        self.name = name
        self.cpt = {}
        self.parents = {}
        self.ordered_parents = []

        # fist row in cpt is its header
        if len(cpt[0]) > 1:     # it got parents
            for p in cpt[0][1:]:
                self.ordered_parents.append(p)
        if name == UTILITY_NODE:
            pass
        if _type != DEC_NODE:
            for i in range(1, len(cpt)):
                val = float(cpt[i][0])
                key = []
                for j in range(1, len(cpt[i])):
                    key.append(cpt[i][j])

                if _type == NORM_NODE:
                    key.append(key_of(TRUE, name))
                    self.cpt[tuple(key)] = val          # Happened
                    del key[-1]
                    key.append(key_of(FALSE, name))
                    self.cpt[tuple(key)] = 1.0 - val    # Did not happen
                elif _type == UTILITY_NODE:
                    self.cpt[tuple(key)] = val          # Happened

    def probability(self, value, theta):
        """
        Computes probability of this node
        :param value: assignment/value for this node
        :param theta: dictionary having assignments for its parents
        :return: Conditional probability of this node
        """
        if self._type == NORM_NODE or (self._type == DEC_NODE and self.cpt):
            key = []
            for parent in self.ordered_parents:
                key.append(key_of(theta[parent][0], parent))
            key.append(key_of(value, self.name))
            return self.cpt[tuple(key)]
        else:
            if debug:
                print("ERROR: %s%s not known, %s" % (value, self.name, theta))
            return 1.0  # FIXME:

    def __repr__(self):
        return "(%s<%s>: %s :%s)" % (self.name, self._type, self.parents.keys(), self.cpt)


class DecisionNode(Node):
    """
    Decision node with functionality for making and undoing decisions
    """
    def decide(self, value):
        """
        Decides assignment for this node
        :param value: assignment for this node
        :return:
        """
        self.cpt = {
            tuple([key_of(value, self.name)]): 1.0,
            tuple([key_of(complement_value(value), self.name)]): 0.0
        }

    def undecide(self):
        """
        Clears any previous decisions made
        :return:
        """
        self.cpt = {}


class Query(object):
    """
    this class stores query model
    """

    def __init__(self, _type, query, given=None):
        """
        Creates query
        :param _type: query type = {P, EU, MEU}
        :param query: query variables
        :param given: evidence variables
        :return:
        """
        self._type = _type
        self.given = given
        self.query = query
        self.nodes = []
        self.nodes.extend(query)
        if given:
            self.nodes.extend(given)

    def __repr__(self):
        return "%s (%s | %s)" % (self._type, self.query, self.given)

    def decide(self, decisions):
        """
        Updates assignment of undecided variables in query
        :param decisions:
        :return: variables whose values affected this decision
        """
        changed = []
        node_sets = [self.query]
        if self.given:
            node_sets.append(self.given)
        for nodes in node_sets:
            for i in range(0, len(nodes)):
                if nodes[i][1:] in decisions:
                    chars = list(nodes[i])   # because strings cant be modified inplace
                    chars[0] = decisions[nodes[i][1:]]
                    nodes[i] = "".join(chars)
                    changed.append(nodes[i])
        return changed


class Parser(object):
    """
    This class hnows how to parse the input file. The implementation is specific to assignment instructions and format
    """

    def tokenize(self, statement):
        """
        tokenizes a statement
        :param statement: input statement
        :return: list of tokens
        """
        return statement.strip().split()

    def parse_cpt(self, cpt):
        """
        Parses conditional probability table and build bayesian Node
        :param cpt: conditional probability table
        :return: Node
        """
        name = cpt[0][0]
        _type = UTILITY_NODE if name == UTILITY_NODE else DEC_NODE if cpt[1][0] == DEC_NODE else NORM_NODE
        head = cpt[0]
        if GIVEN in head:      # take out '|' token from header
            head.remove(GIVEN)
        if _type in (NORM_NODE, UTILITY_NODE):
            for i in range(1, len(cpt)):
                cpt[i][0] = float(cpt[i][0])
                for j in range(1, len(cpt[i])):
                    cpt[i][j] = key_of(cpt[i][j], cpt[0][j])
            return Node(name, cpt, _type)
        elif _type == DEC_NODE:
            return DecisionNode(name, cpt, _type)
        else:
            print("Error: %s parsing not implemented" % _type)

    def parse_query(self, statement):
        """
        Parses query
        :param statement: query statement
        :return: Query
        """
        tokens = statement.replace("(", " ").replace(")", " ").replace(",", " , ").strip().split()
        name = tokens[0]
        if name in (PROBABILITY, EXP_UTILITY, MAX_EXP_UTILITY):
            query, given = [], []
            i, evidence = 1, False
            while i < len(tokens):
                token = tokens[i]
                if token == JOINT:
                    pass            # nothing needs to be done for this comma
                elif token == GIVEN:
                    evidence = True   # what follows is evidence
                else:
                    tmp = given if evidence else query
                    if (i+1) < len(tokens) and tokens[i+1] == EQUALS:
                        assignment = tokens[i+2]   # ['Node', '=', 'Assignment']
                        i += 2   # equals and the assignment are consumed
                    else:
                        assignment = UNDECIDED     # ['Decision']
                    tmp.append(key_of(assignment, token))
                i += 1              # move ahead for next iteration
            return Query(name, query, given)
        else:
            raise Exception("Not implemented yet! %s" % name)

    def parse(self, in_file):
        """
        Parses input file
        :param in_file: path to input file
        :return: list of Query objects, BayesNet object
        """
        queries = []
        net = BayesNet()
        with open(in_file) as reader:
            for line in reader:         # queries first
                line = line.strip()
                if line == QRY_SEP:
                    break              # Done parsing queries
                elif line:
                    queries.append(self.parse_query(line))
            cpt = []
            for line in reader:         # parse nodes
                tokens = self.tokenize(line)
                if not tokens:    # skip empty lines if there are any
                    continue
                if tokens[0] == NODE_SEP or tokens[0] == QRY_SEP:   # end of current Node
                    if cpt:
                        net.add_node(self.parse_cpt(cpt))
                    cpt = []
                else:
                    cpt.append(tokens)
            if cpt:
                net.add_node(self.parse_cpt(cpt))
        return queries, net


class BayesNet(object):
    """
    This class models a simple Bayes Network
    """

    def __init__(self):
        """
        Creates Bayes Network
        :return: instance of Bayes network
        """
        self.index = {}
        self.topo_sort = []
        self.decision_nodes = []
        self.utility_node = None

    def add_node(self, node):
        """
        Adds a node to this bayes network
        :param node: Node instance
        :return:
        """
        self.index[node.name] = node
        if node._type != UTILITY_NODE:
            self.topo_sort.append(node)
        for parent in node.ordered_parents:
            node.parents[parent] = self.index[parent]

        if node._type == DEC_NODE:
            self.decision_nodes.append(node)
        elif node._type == UTILITY_NODE:
            self.utility_node = node

    def __repr__(self):
        return str(self.topo_sort)

    def compute(self, state):
        """
        Computes probability of a state
        :param state: state
        :return: probability of state
        """
        res = 1.0
        theta = {}
        for state_val in state:
            val, name = state_val[0], state_val[1:]
            node = self.index[name]
            jpd = node.probability(val, theta)
            res *= jpd
            theta[name] = (val, jpd)
        return res

    def build_jpd_table(self):
        """
        Build joint probability table by enumerating all states
        :return: table (i.e. dictionary of state_key:probability)
        """
        nodes = map(lambda x: x.name, self.topo_sort)
        table = {}

        for i in range(0, 2**len(nodes)):
            state = "{0:0{1}b}".format(i, len(nodes))
            key = []
            for j in range(0, len(state)):
                key.append("{0}{1}".format(FALSE if state[j] == '0' else TRUE, nodes[j]))
            table[tuple(key)] = self.compute(key)
        return table

    def compute_utility(self, q, table):
        """
        Computes utility of given state
        :param q: query
        :param table: JPT
        :return: utility value
        """
        total_util = 0.0
        for key, util in self.utility_node.cpt.items():
            query = list(key)
            given = copy(q.query)
            if q.given:
                given.extend(q.given)
            new_q = Query(PROBABILITY, query, given)
            p = self.compute_by_enumerate(new_q, table)
            if debug:
                print("%s = %s" % (new_q, p))
            total_util += p * util
        return total_util

    def compute_max_utility(self, q):
        """
        Searches for maximum utility states
        :param q: query
        :return: (\maximum utility value, decision choices)
        """
        max_util = 0.0
        q_undecided = map(lambda y: y[1:], filter(lambda x: x[0] == UNDECIDED, q.nodes))        # query undecided
        n_undecided = map(lambda y: y.name, filter(lambda x: not x.cpt, self.decision_nodes))   # network Undecided
        h_undecided = set(n_undecided).difference(q_undecided)         # hidden undecided
        undecided = []
        undecided.extend(q_undecided)   # query vars first
        undecided.extend(h_undecided)   # hidden vars last

        rational_decisions = []
        if undecided:
            last_state = ""
            for i in range(0, 2**len(undecided)):
                state = "{0:0{1}b}".format(i, len(undecided))
                decisions = {}
                for j in range(0, len(state)):
                    assign = FALSE if state[j] == '0' else TRUE
                    self.index[undecided[j]].decide(assign)
                    decisions[undecided[j]] = assign
                table = self.build_jpd_table()
                new_q = deepcopy(q)
                choices = new_q.decide(decisions)
                util = self.compute_utility(new_q, table)
                if debug:
                    print("Choices %s = %s " % (choices, util))
                if util > max_util:
                    max_util = util
                    rational_decisions = choices
                last_state = state
            for j in range(0, len(last_state)):
                self.index[undecided[j]].undecide()
        else:
            max_util = self.compute_utility(q, self.build_jpd_table())
        return max_util, rational_decisions

    def compute_by_enumerate(self, q, table):
        """
        Computes probability of a query state by enumerating over JPT table
        :param q: query state
        :param table: joint probability table
        :return:  probability of query state
        """
        res = 0.0
        for key, val in table.items():
            select = True
            for n in q.nodes:
                if n not in key:
                    select = False
                    break
            if select:
                res += val

        if q.given and res > 0.0:   # Conditional probability given evidence
            denominator = self.compute_by_enumerate(Query(q._type, q.given), table)
            if debug:
                print("Joint : %f  / Evidence : %f" % (res, denominator))
            res /= denominator

        undecided_count = self.count_undecided_nodes(q)  # undecided variables mess up
        if undecided_count >= 1:  # if there are undecided nides
            if debug:
                print("%s Undecided Node count = %d" % (q, undecided_count))
            res /= 2 * undecided_count  # reduce to half
        return res

    def make_decisions(self, decisions):
        """
        Makes decisions for decisions nodes
        :param decisions: dictionary of decision assignments
        :return:
        """
        for name, value in decisions.items():
            self.index[name].decide(value)

    def undo_decisions(self, decisions):
        """
        Clears previously made decisions
        :param decisions: dictionary of decisions
        :return:
        """
        for name in decisions.keys():
            self.index[name].undecide()

    def count_undecided_nodes(self, query):
        assignments = dict(map(lambda x: (x[1:], x[0]), query.nodes))
        num_assignments = 0
        for k in assignments.keys():
            if self.index[k]._type == DEC_NODE:
                num_assignments += 1
        return len(self.decision_nodes) - num_assignments

    def query(self, q):
        """
        Queries this bayes net for given query state's probability or utility or maximum expected utility
        :param q: instance of Query
        :return: result as per grading instructions of assignment
        """
        decisions = {}
        if self.decision_nodes:     # assign decisions as per Query
            assignments = dict(map(lambda x: (x[1:], x[0]), q.nodes))
            for dn in self.decision_nodes:
                # print("Assign %s to %s" % (assignments[dn.name], dn.name))
                if dn.name in assignments and assignments[dn.name] != UNDECIDED:
                    decisions[dn.name] = assignments[dn.name]
        self.make_decisions(decisions)
        if q._type == MAX_EXP_UTILITY:
            res, choices = self.compute_max_utility(q)
            choices = map(lambda x: x[0], choices)
            if debug:
                print("%s = %s, %f" % (q, choices, res))
            res = "%s %s" % (" ".join(choices), format_float(res, 0))
        else:
            table = self.build_jpd_table()
            res = None
            if q._type == PROBABILITY:
                res = self.compute_by_enumerate(q, table)
                if debug:
                    pprint(table)
                    sum = 0.0
                    for v in table.values():
                        sum += v
                    print("Sum = %f" % sum)
                    print("%s = %f" % (q, res))
                res = format_float(res, 2)
            elif q._type == EXP_UTILITY:
                res = self.compute_utility(q, table)
                if debug:
                    print("%s = %f" % (q, res))
                res = format_float(res, 0)
        self.undo_decisions(decisions)
        return res

if __name__ == '__main__':
    parser = ArgumentParser(description="CSCI561 Spring2016 HW3 Solution for Deciding under uncertainty" \
                                        + " by Thamme Gowda (2074-669439)", version='1.0')
    parser.add_argument("-i", "--input", help="Path to input file", required=True)
    parser.add_argument("-o", "--output", help="Path to output file", required=False, default="output.txt")
    args = vars(parser.parse_args())
    qs, net = Parser().parse(args['input'])

    with open(args['output'], 'w') as out:
        for i in range(0, len(qs)):
            res = deepcopy(net).query(qs[i])
            out.write("%s" % res)
            if i < len(qs) - 1:         # except last one, graders you !!
                out.write("\n")
# END #
