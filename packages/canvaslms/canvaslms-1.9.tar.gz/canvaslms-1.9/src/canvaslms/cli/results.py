import canvaslms.cli.assignments as assignments
import canvaslms.cli.courses as courses
import canvaslms.cli.submissions as submissions
import canvaslms.hacks.canvasapi

import argparse
import csv
import datetime as dt
import importlib
import re
import sys

def results_command(config, canvas, args):
  output = csv.writer(sys.stdout, delimiter=args.delimiter)

  assignments_list = assignments.process_assignment_option(canvas, args)

  if args.assignment_group != "":
    results = summarize_assignment_groups(canvas, args)
  else:
    results = summarize_assignments(canvas, args)

  for result in results:
    if not args.include_Fs and result[3][0] == "F":
      continue
    output.writerow(result)
def summarize_assignments(canvas, args):
  """Turn submissions into results,
  canvas is a Canvas object,
  args is the command-line arguments"""

  courses_list = courses.process_course_option(canvas, args)

  users_list = []
  for course in courses_list:
    for user in course.get_users(enrollment_type=["student"]):
      users_list.append(user)

  assignments_list = assignments.process_assignment_option(canvas, args)
  submissions_list = submissions.filter_submissions(
    submissions.list_submissions(assignments_list, include=[]),
    users_list)

  for submission in submissions_list:
    if submission.grade is not None:
      yield (
        submission.assignment.course.course_code,
        submission.assignment.name,
        submission.user.integration_id,
        submission.grade,
        submission.submitted_at or submission.graded_at
        )
def summarize_assignment_groups(canvas, args):
  """Summarize assignment groups into a single grade,
  canvas is a Canvas object,
  args is the command-line arguments"""

  summary = importlib.import_module(args.summary_module)

  courses_list = courses.process_course_option(canvas, args)
  all_assignments = list(assignments.process_assignment_option(canvas, args))

  for course in courses_list:
    users_list = list(course.get_users(enrollment_type=["student"]))
    ag_list = assignments.filter_assignment_groups(
      course, args.assignment_group)

    for assignment_group in ag_list:
      assignments_list = list(assignments.filter_assignments_by_group(
        assignment_group, all_assignments))
      for user, grade, grade_date in summary.summarize_group(
        assignments_list, users_list):
          yield (
            course.course_code,
            assignment_group.name,
            user.integration_id,
            grade,
            grade_date
          )

def add_command(subp):
  """Adds the results command to argparse parser subp"""
  results_parser = subp.add_parser("results",
      help="Lists results of a course",
      description="Lists results of a course for export, for instance "
      "to the `ladok report -f` command. Output format, CSV: "
        "<course code> <component code> <student ID> <grade> <grade date>.",
      epilog="If you specify an assignment group, the results of the "
        "assignments in that group will be summarized. You can supply your "
        "own function for summarizing grades through the -S option. The "
        "default works as follows: "
        "All assignments must have a passing grade. If there are assignments "
        "with A--F grading scales (in addition to P/F) the avergage of the "
        "A--F grades will be used as final grade for the entire group. If any "
        "assignment has an F, the whole group will evaluate to an F.")
  results_parser.set_defaults(func=results_command)
  assignments.add_assignment_option(results_parser, ungraded=False)
  results_parser.add_argument("-S", "--summary-module",
    required=False, default="canvaslms.cli.summary",
    help="Name of Python module to load with a custom summarization function "
      "to summarize assignment groups. The default module is part of the "
      "`canvaslms` package: `canvaslms.cli.summary`. This module must contain "
      "a function `summarize_group(assignments, users)`, where `assignments` "
      "is a list of assignment `canvasapi.assignment.Assignment` objects and "
      "`users` is a list of `canvasapi.user.User` objects. The return value "
      "must be a tuple "
      "`(user object, grade, grade date)`.")
  results_parser.add_argument("-F", "--include-Fs",
    required=False, default=False, action="store_true",
    help="Include failing grades (Fs) in output. By default we only output "
      "A--Es and Ps.")
