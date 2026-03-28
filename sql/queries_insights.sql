--Conteo de logs por tipo (INFO/ERROR)--

fields @timestamp, @message
| filter @message like /INFO/ or @message like /ERROR/ or @message like /WARNING/
| stats count(*) by bin(5m)

-- Buscar errores específicos -- 
fields @timestamp, @message, @logStream
| filter @message like /ERROR/ or @message like /Exception/ or @message like /fail/
| sort @timestamp desc

-- Actividad por servidor --
stats count(*) by @logStream

-- Ver los últimos eventos de éxito --
fields @timestamp, @message
| filter @message like /SUCCESS/ or @message like /terminado/
| sort @timestamp desc

-- Widget 1: Volumen de Actividad (Gráfico de líneas) --
stats count(*) by bin(1m)

-- Widget 2: Últimos Errores (Tabla) --
fields @timestamp, @message, @logStream
| filter @message like /ERROR/ or @message like /Exception/
| sort @timestamp desc

-- Widget 3: Éxitos en el Pipeline (Número grande) --
filter @message like /SUCCESS/
| stats count(*)

