
cd lambda
uv sync


cd infra
cdk deploy --all

check event approval status for each attendee



UI instead of GForm

Pros
- Allows to create a dynamic drop down for the list of tasks/jobs, so there's no mismatch
- Allows employees not to fill in date/time, except if it didn't perfectly match their actual work

Cons
- Requires some sort of login
- More things to maintain
- Needs a DB otherwise it will be hard making any of the pros

---------

Questions:
- Can you describe your processes and what problems they have?
- How often do employees need to submit their timesheet? Current/Ideal
- Which info do they submit?
- How do they currently know their schedule?
- What are the timesheets used for?