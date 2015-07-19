import sys
import fileinput
import os
import re
import fnmatch

from subprocess import check_call

NUM_EXPECTED_ARGS = 3
MATCHING_PATTERN = r'(?P<front>"(amount|budgeted)": "?)(?P<amount>-?\d+\.?\d*)(?P<back>"?)'

class YnabConverter():
    """Converts the currency of a ynab budget """
    def __init__(self, budget_location, amount_multiplier = 1, new_budget_location_suffix = "_converted"):
        self.budget_location = budget_location
        self.amount_multiplier = amount_multiplier
        self.create_budget_copy(new_budget_location_suffix)

    def create_budget_copy(self, new_budget_suffix):
        budget_location_components = self.budget_location.split(".")
        original_name = budget_location_components[0]
        extension = budget_location_components[1]
        self.new_budget_location = original_name + new_budget_suffix + "." + extension

        command = "cp -r " + self.budget_location + " " + self.new_budget_location
        print "Executing: '%s'" % (command)
        check_call(command.split(" "))

    def convert_budget_amounts(self):
        matching_filenames = []
        for root, dirnames, filenames in os.walk(self.new_budget_location):
            for filename in fnmatch.filter(filenames, '*.ydiff'):
                matching_filenames.append(os.path.join(root, filename))
            for filename in fnmatch.filter(filenames, '*.yfull'):
                matching_filenames.append(os.path.join(root, filename))

        for filename in matching_filenames:
            self.convert_file(filename)

    def convert_file(self, filename):
        # file_to_convert = open(filename, 'r+')

        for line in fileinput.input(filename, inplace = True):
            match = re.search(MATCHING_PATTERN, line)
            if match is not None:
                # print "Line before replace: '%s'" % line
                current_amount = float(match.group('amount'))
                new_amount = current_amount * self.amount_multiplier
                # print "New amount is: %s" % (new_amount)

                line = re.sub(MATCHING_PATTERN, r'\g<front>' + str(new_amount) + r'\g<back>', line)
                # print "Line after replace: '%s'" % line
                print line
            else:
                print line

        # file_to_convert.close()


def main():
    if len(sys.argv) != NUM_EXPECTED_ARGS:
        raise Exception("Expected " + str(NUM_EXPECTED_ARGS - 1) + " arguments, got " + str(len(sys.argv) - 1))

    budget_location = sys.argv[1]
    amount_multiplier = float(sys.argv[2])
    converter = YnabConverter(budget_location, amount_multiplier)
    converter.convert_budget_amounts()

if __name__ == '__main__':
    main()