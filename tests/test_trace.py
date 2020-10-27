"""
Test barium meal trace
"""
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

def test_publish_span_state():
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
