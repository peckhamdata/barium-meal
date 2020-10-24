# barium-meal

Python Wrapper for [OpenTelemetry](https://opentelemetry.io/) written to scratch the itch
of needing to use the same / similar code across several [Google Cloud Functions](https://cloud.google.com/functions)
and wanting to abstract away from tracing / logging so I can mix and match the two.

Some of these cloud functions are invoked via HTTP, others from [Pub/Sub](https://cloud.google.com/pubsub) messages.

For Pub/Sub I have jury-rigged persisting
[the state of a Span to propagate between processes](https://opentelemetry-python.readthedocs.io/en/stable/api/trace.html#opentelemetry.trace.SpanContext).
To ensure that a trace that goes from function to function via pub/sub remains contiguous.

I'm *sure* there is a better way of doing this but this is good enough for my purposes and by putting my solution
out in the wild I'm hoping to get feedback to help improve it.

