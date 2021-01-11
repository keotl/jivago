from jivago.templating.template_filter import TemplateFilter
from jivago.wsgi.filter.system_filters.banner_filter import BannerFilter
from jivago.wsgi.filter.system_filters.body_serialization_filter import BodySerializationFilter
from jivago.wsgi.filter.system_filters.error_handling.application_exception_filter import ApplicationExceptionFilter
from jivago.wsgi.filter.system_filters.error_handling.unknown_exception_filter import UnknownExceptionFilter
from jivago.wsgi.filter.system_filters.request_scope_filter import RequestScopeFilter
from jivago.wsgi.filter.system_filters.streaming_response_header_filter import StreamingResponseHeaderFilter
from jivago.wsgi.request.http_form_deserialization_filter import HttpFormDeserializationFilter
from jivago.wsgi.request.json_serialization_filter import JsonSerializationFilter
from jivago.wsgi.routing.cors.cors_headers_injection_filter import CorsHeadersInjectionFilter

JIVAGO_DEFAULT_FILTERS = [BannerFilter,
                          CorsHeadersInjectionFilter,
                          UnknownExceptionFilter,
                          TemplateFilter,
                          JsonSerializationFilter,
                          HttpFormDeserializationFilter,
                          StreamingResponseHeaderFilter,
                          BodySerializationFilter,
                          ApplicationExceptionFilter,
                          RequestScopeFilter]

# Required filters for HTTP OPTIONS requests.
JIVAGO_DEFAULT_OPTIONS_FILTERS = [BannerFilter,
                                  CorsHeadersInjectionFilter,
                                  UnknownExceptionFilter,
                                  JsonSerializationFilter,
                                  BodySerializationFilter,
                                  ApplicationExceptionFilter,
                                  RequestScopeFilter]
