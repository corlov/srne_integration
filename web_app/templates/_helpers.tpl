{{/*
Генерирует стандартные метки для всех ресурсов.
*/}}
{{- define "solar-system.labels" -}}
helm.sh/chart: {{ include "solar-system.name" . }}
{{ include "solar-system.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{/*
Генерирует метки селектора для сервиса.
*/}}
{{- define "solar-system.selectorLabels" -}}
app.kubernetes.io/name: {{ include "solar-system.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{/*
Возвращает полное имя чарта.
*/}}
{{- define "solar-system.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}
