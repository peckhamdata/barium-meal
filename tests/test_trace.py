"""
Test barium meal trace
"""


def test_setup_tracer():
    """Set up OpenTelemetry tracer"""

    bm = BariumMeal(jaeger={'collector_host_name': 'jaegerbomb',
                            'service_name': 'ja-ja-ja')

    tracer = bm.get_tracer()



def test_publish_span_state():
    """Persist correlation data to Pub/Sub"""


def test_resume_span_from_message():
    """Resume trace from data in Pub/Sub"""
