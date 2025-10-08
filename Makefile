SHELL := /bin/bash

.PHONY: init demo_free5gc demo_nephio demo_prom demo_otel

init:
	bash scripts/bootstrap_git.sh

demo_free5gc:
	bash scripts/repro_free5gc_oauth2.sh

demo_nephio:
	bash scripts/repro_nephio_backstage.sh

demo_prom:
	bash scripts/demo_prometheus_multidoc.sh

demo_otel:
	bash scripts/demo_otlp_ruby_default.sh
