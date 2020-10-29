"""
Test barium meal trace
"""
import re
import opentelemetry
from barium_meal import BariumMeal


def test_setup_tracer():
    """Set up OpenTelemetry tracer"""

    bm = BariumMeal(jaeger_config={'collector_host_name': 'jaegerbomb',
                            'service_name': 'ja-ja-ja'})

    tracer = bm.get_tracer()
    assert isinstance(tracer, opentelemetry.sdk.trace.Tracer)


def test_with_requests():

    bm = BariumMeal(requests=True)
    tracer = bm.get_tracer()
    assert isinstance(tracer, opentelemetry.sdk.trace.Tracer)


def test_publish_span_state_pubsub():
    """Persist correlation data to Pub/Sub"""

    bm = BariumMeal()
    tracer = bm.get_tracer()

    with tracer.start_as_current_span("my_span") as my_span:
        message = {'payload': 'value'}
        traceable_message = bm.add_trace(message, my_span)

        assert traceable_message['trace']['trace_id'] == my_span.get_span_context().trace_id


def test_resume_span_from_message():
    """Resume trace from data in Pub/Sub"""
    bm = BariumMeal()
    tracer = bm.get_tracer()
    traced_message = {'trace': {'trace_id': 1,
                                'span_id': 2,
                                'trace_state': {},
                                'trace_flags': 1}}
    bm.get_context_from_event_data(traced_message)
    with tracer.start_as_current_span("my_span") as my_span:
        assert my_span.get_span_context().trace_id == 1


def test_instrument_boto():
    """Confiugure to include boto"""

    bm = BariumMeal(boto=True)

    tracer = bm.get_tracer()
    assert isinstance(tracer, opentelemetry.sdk.trace.Tracer)


def test_traceparent_header_from_span_state():
    """
    Get W3C traceparent header:
    https://www.w3.org/TR/trace-context/#trace-context-http-headers-format
    """

    bm = BariumMeal()
    tracer = bm.get_tracer()

    with tracer.start_as_current_span("my_span") as my_span:
        header = bm.get_traceparent_header(my_span)
        assert isinstance(header['traceparent'], str)

        matches = re.findall('00-[a-f0-9]{32}-[a-f0-9]{16}-[a-f0-9]{2}',
                             header['traceparent'])
        assert len(matches) == 1


def test_resume_span_from_headers():
    """
    Just going to do traceparent to get started
    """
    bm = BariumMeal()
    tracer = bm.get_tracer()
    traceparent_header = {'traceparent': '00-0000000000000000000000000000000f-000000000000000a-00'}
    bm.get_context_from_headers(traceparent_header)
    with tracer.start_as_current_span("my_span") as my_span:
        assert my_span.get_span_context().trace_id == 15
        assert my_span.get_span_context().trace_flags == 0
