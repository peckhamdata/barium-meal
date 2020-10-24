class BariumMeal():

    def __init__(self):
        collector_host_name = environ['COLLECTOR_HOST_NAME']
        trace.set_tracer_provider(TracerProvider())
        self.tracer = trace.get_tracer(__name__)

        # create a JaegerSpanExporter
        jaeger_exporter = jaeger.JaegerSpanExporter(
            service_name="airtable_ingest",
            collector_host_name=collector_host_name,
            collector_port=14268,
        )

        # create a BatchExportSpanProcessor and add the exporter to it
        span_processor = BatchExportSpanProcessor(jaeger_exporter)

        # add to the tracer factory
        trace.get_tracer_provider().add_span_processor(span_processor)


    def get_tracer(self):
        return self.tracer