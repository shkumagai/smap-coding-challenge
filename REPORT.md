# Report

## Done

- Implement and execute `import` command
- Implement `summary` view
- Implement `detail` view
- Implement tests for `summary` and `detail` views
- Add flake8 and its extensions to tidy up codes automatically

## Technical decisions

Use Class based view, not View functions
- I'm used to using Class based view
- Easy to split implementation into sub classes or mixins (in my opinion)

Use Chartjs to draw charts
- js file loaded from CDN directly
- Using Django template view, not implement as SPA

Use bootstrap CSS framework
- I'm not CSS professional
- To minimize the cost for edit CSS files

Show consumption data by day
- It can be specified via query parameter which formatted as `?date=yyyy-mm-dd`
- If not specified, use the oldest date which has consumption data

Use pytest as a test runner
- Easy to detect where an error has occurred on, why an error occurred
- Finding tests automatically
- Listing tests which took too long durations

Use flake8 to check syntax, keep tidy codes
- de facto standard in Python
- Well-maintained by PyCQA
- East to use

## Trade-offs

Use magic number to get the oldest date when a date doesn't specified in the query parameter
- In general, create 'summary' table separately, and insert pre-calculated data into there to get summarized data easily
- In this challenge, I didn't do that because it seems overkill

Implement with Django template view
- To change page contents, need to modify each template

## Others

- Add Makefile to aggregate commands that used frequently in development and to make it easier to use them

## Additional packages

Added these packages explicitly:
- pytest
- pytest-django
- flake8
- flake8-coding
- flake8-commas
- flake8-comprehensions
- flake8-debugger
- flake8-import-order
- flake8-print
- flake8-string-format

and added some other packages which above packages depend.
