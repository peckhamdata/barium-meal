from base64 import b32encode

from opentelemetry import trace
from opentelemetry.exporter import jaeger
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.boto import BotoInstrumentor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry import context
from opentelemetry.context.context import Context


class BariumMeal():

    def __init__(self,
                 jaeger_config=None,
                 requests=False,
                 boto=False,
                 flask_app=None):
        trace.set_tracer_provider(TracerProvider())
        self.tracer = trace.get_tracer(__name__)

        # create a JaegerSpanExporter
        if jaeger_config is not None:
            jaeger_exporter = jaeger.JaegerSpanExporter(
                service_name=jaeger_config['service_name'],
                collector_endpoint=jaeger_config['collector_endpoint']
            )

            # create a BatchExportSpanProcessor and add the exporter to it
            span_processor = BatchExportSpanProcessor(jaeger_exporter)

            # add to the tracer factory
            trace.get_tracer_provider().add_span_processor(span_processor)

        if requests:
            RequestsInstrumentor().instrument(tracer_provider=trace.get_tracer_provider())

        if boto:
            BotoInstrumentor().instrument(tracer_provider=trace.get_tracer_provider())

        if flask_app:
            FlaskInstrumentor().instrument_app(flask_app)

    def get_tracer(self):
        return self.tracer

    def add_trace(self, message, span):
        traced_message = message.copy()
        traced_message['trace'] = {'trace_id': span.get_span_context().trace_id,
                                   'span_id': span.get_span_context().span_id,
                                   'trace_state': span.get_span_context().trace_state,
                                   'trace_flags': span.get_span_context().trace_flags}
        return traced_message


    def get_context_from_event_data(self, event_data):

        incoming_context = trace.SpanContext(trace_id=event_data['trace']['trace_id'],
                                             span_id=event_data['trace']['span_id'],
                                             trace_flags=trace.TraceFlags(event_data['trace']['trace_flags']),
                                             trace_state=trace.TraceState(event_data['trace']['trace_state']),
                                             is_remote=True)
        base_span = trace.DefaultSpan(context=incoming_context)
        our_context = Context({'current-span': base_span})
        context.attach(our_context)


    def get_traceparent_header(self, span):
        trace_id = str(hex(span.get_span_context().trace_id)[2:]).zfill(32)
        parent_id = str(hex(span.get_span_context().span_id)[2:]).zfill(16)
        trace_flags = str(span.get_span_context().trace_flags).zfill(2)
        header = f'00-{trace_id}-{parent_id}-{trace_flags}'
        return {'traceparent': header}


    def get_context_from_headers(self, traceparent_header):
        trace_id = int(traceparent_header['traceparent'][3:35], 16)
        span_id = int(traceparent_header['traceparent'][37:52], 16)
        trace_flags = int(traceparent_header['traceparent'][53:], 16)
        incoming_context = trace.SpanContext(trace_id=trace_id,
                                             span_id=span_id,
                                             trace_flags=trace.TraceFlags(trace_flags),
                                             is_remote=True)
        base_span = trace.DefaultSpan(context=incoming_context)
        our_context = Context({'current-span': base_span})
        context.attach(our_context)
