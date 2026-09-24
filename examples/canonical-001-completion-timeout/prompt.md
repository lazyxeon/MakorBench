# Operator Report

We have an intermittent problem with the render-job pipeline.

A small number of jobs end up marked `TIMED_OUT` by the scheduler even though the rendered object exists in artifact storage. In the cases we've manually checked, the billing ledger also shows the job as completed.

What we know so far:

- it is rare enough that we have not found a reliable manual reproduction;
- it seems more likely after a worker has been running for several hours;
- restarting an affected worker appears to make the problem disappear for a while;
- CPU, memory, database latency, and queue depth look normal during incidents;
- increasing the scheduler timeout from 45 seconds to 90 seconds reduced the visible timeout rate but did not eliminate the issue;
- there is no obvious user-facing exception besides the timeout state.

Please determine the actual cause, make the smallest safe fix, and verify that the fix addresses the underlying problem rather than only hiding the timeout symptom.
