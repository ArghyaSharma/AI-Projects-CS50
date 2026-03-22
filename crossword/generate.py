import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # raise NotImplementedError
        for variable in self.domains:
            self.domains[variable] = {x for x in self.domains[variable] if len(x) == variable.length}
            # here, x represents word!

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.
        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # raise NotImplementedError
        revised = False
        if self.crossword.overlaps[x, y]:
            overlap = self.crossword.overlaps[x, y]
            for word_x in self.domains[x].copy():
                satisfies = False
                for word_y in self.domains[y]:
                    if word_x[overlap[0]] == word_y[overlap[1]]:
                        satisfies = True
                        break

                if (satisfies == False):
                    self.domains[x].remove(word_x)
                    revised = True

        return revised
            
    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # raise NotImplementedError
        # first of all, I will initialise a queue
        queue = []
        # next up, will check all the variables in the domain, if they overlap
        for x in self.domains:
            for y in self.domains:
                if x != y and self.crossword.overlaps[x, y]:
                    queue.append((x, y))

        # now that, the queue of all the arcs have been initialised, will start checking
        # whether they are arc consistent or not, until the queue is empty
        while len(queue) != 0:
            (X, Y) = queue.pop(0)
            if self.revise(X, Y):
                if len(self.domains[X]) == 0:
                    return False
                
                neighbours = self.crossword.neighbors(X)
                for neighbour in neighbours:
                    if neighbour != Y :
                        queue.append((neighbour, X))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # raise NotImplementedError
        for variable in self.domains:
            if variable not in assignment:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # raise NotImplementedError
        for variable in assignment:
            word = assignment[variable]

            if len(word) != variable.length:
                return False
            
            neighbours = self.crossword.neighbors(variable)
            for neighbour in neighbours:
                overlap = self.crossword.overlaps[variable, neighbour]
                if neighbour in assignment and word[overlap[0]] != assignment[neighbour][overlap[1]]:
                    return False
                
            word_assigned = list(assignment.values())
            if len(word_assigned) != len(set(word_assigned)):
                return False
            
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # raise NotImplementedError
        values = [] # an empty list which is going to contain all the words in domain of var
        for words in self.domains[var]:
            values.append(words)

        result = []
        # initialising a dictionary which is gonna store the words with their respective 
        # elimination count
        word_with_elimination_count = {}

        # now, for each word in the values, we will find out, how many words they remove from rest 
        # of the nodes
        for words in values:
            elimination_count = 0
            neighbours = self.crossword.neighbors(var)
            for neighbour in neighbours:
                if neighbour not in assignment:
                    overlap = self.crossword.overlaps[var, neighbour]
                    word_neighbour = self.domains[neighbour]
                    for word_n in word_neighbour:
                        if words[overlap[0]] != word_n[overlap[1]]:
                            elimination_count += 1
            word_with_elimination_count[words] = elimination_count
            
        sorted_elimination_count = sorted(word_with_elimination_count.items(), key = lambda item: item[1])
        result = [k for k, v in sorted_elimination_count]

        return result

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # raise NotImplementedError
        # maintaining a dictionary which consists of variables with their corresponding numbers of
        # words in their domain in ascending order
        variable_domain_count = {}
        variable_list = []
        final_variable_list = []
        for variable in self.domains:
            if variable not in assignment:
                count = 0 # setting up a counter to count the number of words in its domain
                for words in self.domains[variable]:
                    count += 1
                
                variable_domain_count[variable] = count

        # now, sorting the dictionary according to number of domains in ascending order
        sorted_variable_domain_count = sorted(variable_domain_count.items(), key = lambda item: item[1])
        variable_list = [k for k, v in sorted_variable_domain_count]

        # list of variables with least number of words in its domains, we are gonna write code
        # for a tie-breaker between them
        variable_list_with_min_values = [k for k, v in variable_domain_count.items() if v == min(variable_domain_count.values())]
        variable_list_with_min_values_dict = {}
        # this dictionary will consist of all variables with same amount of domain corresponding to their
        # number of variables

        for v in variable_list_with_min_values:
            count = 0 # maintaining a counter to count number of neighbours
            for neighbour in self.crossword.neighbors(v):
                count += 1

            variable_list_with_min_values_dict[v] = count

        # all that is left, is sorting this dictionary consisting of degree heurestics, in descending order
        sorted_variable_list_with_min_values_dict_dec = sorted(variable_list_with_min_values_dict.items(), key = lambda item: item[1], reverse = True)
        final_variable_list = [k for k, v in sorted_variable_list_with_min_values_dict_dec]

        return final_variable_list[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # raise NotImplementedError
        # how to check if assignment is complete or not?
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for word in self.order_domain_values(var, assignment):
            assignment[var] = word
            if self.consistent(assignment):
               result = self.backtrack(assignment)
               if (result != None):
                   return result
            del assignment[var]

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
