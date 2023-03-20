package utils

import (
	"go.opentelemetry.io/otel"
)

var Tracer = otel.Tracer("compose-tracer")
