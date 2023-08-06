import canvaslms.cli.assignments as assignments
import canvaslms.cli.courses as courses
import canvaslms.hacks.canvasapi

import argparse
import csv
import re
import sys

def results_command(config, canvas, args):
  output = csv.writer(sys.stdout, delimiter=args.delimiter)

  assignments_list = assignments.process_assignment_option(canvas, args)

  if args.assignment_group != "":
    pass
  else:
    pass

  for result in results:
    output.writerow(result)

def add_command(subp):
  """Adds the results command to argparse parser subp"""
  results_parser = subp.add_parser("results",
      help="Lists results of a course",
      description="Lists results of a course for export, for instance "
      "to the `ladok report -f` command. Output format, CSV: "
        "<course code> <component code> <student ID> <grade> <grade date>.",
      epilog="If you specify an assignment group, the results of the "
        "assignments in that group will be summarized. That means that "
        "all assignments must have a passing grade. If there are assignments "
        "with A--F grading scales (in addition to P/F) the avergage of the "
        "A--F grades will be used as final grade for the entire group. If any "
        "assignment has an F, the whole group will evaluate to an F.")
  results_parser.set_defaults(func=results_command)
  assignments.add_assignment_option(results_parser, ungraded=False)
