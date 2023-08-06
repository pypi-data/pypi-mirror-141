import canvaslms.cli.assignments as assignments
import canvaslms.cli.courses as courses
import canvaslms.hacks.canvasapi

import argparse
import csv
import re
import sys

def results_command(config, canvas, args):
  if args.ungraded:
    submissions = list_ungraded_submissions(assignment_list)
  else:
    submissions = list_submissions(assignment_list)

  if args.user or args.category or args.group:
    user_list = users.process_user_or_group_option(canvas, args)
    submissions = filter_submissions(submissions, user_list)

  output = csv.writer(sys.stdout, delimiter=args.delimiter)

  for submission in submissions:
    output.writerow(format_submission_short(submission))

def add_command(subp):
  """Adds the results command to argparse parser subp"""
  results_parser = subp.add_parser("results",
      help="Lists results of a course",
      description="Lists results of a course for export. Output format: "
        "<course code> <component code> <student ID> <grade> <grade date>")
  results_parser.set_defaults(func=results_command)
  assignments.add_assignment_option(results_parser)
