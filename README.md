# 💊 FarmaList Backend - TFG 🎓

Backend para la plataforma web para el Grado de Farmacia de la Facultad de Farmacia (UGR).

Backend para la gestión de **centros colaboradores** y **listados de prácticas externas** para el Grado de Farmacia de la Facultad de Farmacia de la **UGR**. Implementa la lógica de negocio a través de una API RESTful.

## Estado

Completado (versión 1.0.0)

## Cómo iniciar el proyecto

Se está utilizando el _task runner_ `taskipy`, que trabaja en conjunto con el gestor de dependencias `poetry`.

La primera vez ha de instalar todas las dependencias:

```
poetry install
```

-  Puede consultar las tareas que puede ejecutar con

```
poetry run task -l
task -l # si has ejecutado poetry shell previamente
```

-  Para poner en marcha los contenederes docker:

```
poetry run task docker
task docker # si has ejecutado poetry shell previamente
```

-  Para poner en marcha el servidor de desarrollo de flask en modo debug:

```
poetry run task flask
task flask # si has ejecutado poetry shell previamente
```

-  Para poner los contenedores docker y la aplicación de flask en marcha en modo debug:

```
poetry run task dev
task dev # si has ejecutado poetry shell previamente
```
