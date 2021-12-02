# Guía de estilo <!-- omit in toc -->

- [1. Introducción](#1-introducción)
- [2. Guías auxiliares](#2-guías-auxiliares)
  - [2.1. Listado de guías auxiliares](#21-listado-de-guías-auxiliares)
- [3. Lineamientos generales](#3-lineamientos-generales)
  - [3.1. Archivos de código fuente (_source files_)](#31-archivos-de-código-fuente-source-files)
    - [3.1.1. Codificación](#311-codificación)
    - [3.1.2. Nombre](#312-nombre)
    - [3.1.3. Estructura](#313-estructura)
    - [3.1.4. Copyright](#314-copyright)
    - [3.1.5. Caracteres fuera de la especificación ASCII](#315-caracteres-fuera-de-la-especificación-ascii)
    - [3.1.6. Caracteres especiales](#316-caracteres-especiales)

# 1. Introducción

En esta guía se definen los lineamientos y convenciones que deberán seguirse al momento de escribir código en proyectos de DataInt. El principal objetivo de la guía es delinear un estándar de consistencia y coherencia en el código. Un proyecto con estilo consistente y coherente es más fácil de leer, entender y, por lo tanto, mantener.

Es importante recordar que esta guía sólo es eso: una guía, es decir, un punto arbitrario de referencia sobre cómo debe verse el código. Es imposible cubrir todos los casos y situaciones en un solo documento. Por esto, el programador siempre tiene la última palabra; con su experiencia y conocimientos, juzgará cómo aplicar la guía y en qué situaciones pueden hacerse excepciones a los lineamientos que en ella se presentan.

Esta guía esta divida en tres partes. En primer lugar, se define un grupo de guías auxiliares para lenguajes de programación en específico. Estas deberán usarse para complementar los lineamientos de esta guía y sólo deberán usarse en aquellos casos que no se encuentran contemplados en este documento. En segundo lugar, se presentan los lineamientos generales de la organización. Aquí se definen algunas reglas básicas para trabajar en los proyectos de DataInt. Estas reglas deberán seguirse, en la medida de lo posible, en todos los lenguajes de programación. En la tercera parte, se definen reglas específicas para cada lenguaje de programación. Si una regla específica para un lenguaje de programación entra en conflicto con un lineamiento general, la regla específica tendrá preferencia sobre el lineamiento general.

# 2. Guías auxiliares

A continuación se definen las guías auxiliares a la guía de estilo de DataInt. Las guías auxiliares son guías de estilo usadas por otras organizaciones (principalmente Google) y cuya función es complementar los lineamientos que se definen en este documento. Las guías auxiliares son específicas a cada lenguaje de programación.

Las guías auxiliares deberán usarse en aquellos casos que no son cubiertos por la guía de estilo de DataInt. Si una regla en una guía auxiliar entra en conflicto con una regla específica de lenguaje o un lineamiento general definidos en este documento, las reglas o lineamientos definidos aquí tendrán preferencia sobre aquellas definidas en una guía auxiliar. 

Si en la guía de estilo de DataInt no hay reglas específicas para un lenguaje de programación, el programador deberá usar la guía de estilo definida por Google para dicho lenguaje de programación. Las guías de estilo de Google pueden encontrarse en [su respectivo repositorio](https://github.com/google/styleguide).

## 2.1. Listado de guías auxiliares

- **JavaScript**: [Guía de estilo para JavaScript de Google](https://google.github.io/styleguide/jsguide.html).
- **TypeScript**: [Guía de estilo para TypeScript de Google](https://google.github.io/styleguide/tsguide.html).
- **Python**: [Guía de estilo para Python definida en la PEP-0008](https://www.python.org/dev/peps/pep-0008/).
- **HTML y CSS**: [Guía de estilo para HTML/CSS de Google](https://google.github.io/styleguide/htmlcssguide.html).
- **PHP**: [Guía de estilo para PHP de WordPress](https://developer.wordpress.org/coding-standards/wordpress-coding-standards/php/).

# 3. Lineamientos generales

En esta sección se definen los lineamientos generales para escribir código en los proyectos de DataInt. Los lineamientos generales deberán seguirse, en la medida de lo posible, en todo los lenguajes de programación. Ante cualquier situación no cubierta en estos lineamientos generales, el programador deberá remitirse a loos lineamientos específicos para su lenguaje de programación y, en su defecto, a una de las guías auxiliares.

## 3.1. Archivos de código fuente (_source files_)

### 3.1.1. Codificación

Todos los archivos deberán ser codificados en **UTF-8**.

### 3.1.2. Nombre

Los nombres de los archivos siempre deberán ser en minúsculas (_lowercase_) y podrán contener guiones medios ( `-` ) y bajos ( `_` ). 

Los nombres de archivo no podrán contener signos de puntuación adicionales a los requeridos para especificar la extensión del archivo (`.py`, `.js`, etc.). 

Los nombres de archivos no podrán contener espacios en blanco.

### 3.1.3. Estructura

Los archivos con código deberán tener, en la medida de lo posible, la siguiente estructura:

1. Shebang, si es requerido.
2. Información de copyright en comentarios.
3. Nombre completo y datos de contacto de la persona encargada de la primera implementación (es decir, de crear la primera versión del archivo) en comentarios.
4. Importación de dependencias escritas por terceros.
5. Importación de dependencias escritas por DataInt.
6. Implementación.

### 3.1.4. Copyright

El copyright incluido en los archivos de código dependerá, principalmente, de dos cosas: 1) si la implementación puede ser redistribuida o no (código abierto o código propietario) y 2) si la implementación utiliza código abierto proporcionado por terceros. 

El programador siempre deberá dirigirse al líder de proyecto para saber si la implementación que está produciendo será abierta o propietaria.

En caso que la implementación sea propietaria y no reutilice código abierto de terceros, la nota de copyright deberá ser la siguiente:

```
Copyright (C) {{year}} DataInt Consultores S.A. de C.V. - All Rights Reserved.

This file and its contents are regarded as proprietary and confidential.
Unauthorized copying of this file, via any medium is strictly prohibited.

DataInt Consultores S.A. de C.V. is a company constituted under Mexican law with its principal place of business at Mexico City.
```

El programador deberá sustituir `{{year}}` con el año de la primer implementación (es decir, el año en el que se creo el archivo). 

En caso que la implementación sea propietaria y reutilice código abierto de terceros, la nota de copyright deberá ser la siguiente:

```
Copyright (C) {{year}} DataInt Consultores S.A. de C.V. - Some Rights Reserved.
Copyright (C) {{os_code_year}} {{os_code_author}} // {{os_code_status}}

This file and some of its contents are regarded as proprietary and confidential.
Unauthorized copying of this file, via any medium is strictly prohibited.

This implementation reuses the following works:
{{os_code_author}}, {{os_code_name}}, {{os_code_author}}, licensed under {{os_code_license}}

DataInt Consultores S.A. de C.V. is a company constituted under Mexican law with its principal place of business at Mexico City.
```

El programador deberá sustituir `{{year}}` con el año de la primer implementación. De igual forma, el programador deberá sustituir `{{os_code_year}}`, `{{os_code_author}}`, `{{os_code_status}}`, `{{os_code_license}}` y `{{os_code_name}}` por el año de publicación del código reutilizado, el nombre completo del autor del código reutilizado, el estado del código reutilizado (`modified` o `unchanged`), el nombre de a licencia bajo la cual se distribuyó el código y el nombre del programa o librería que se reutilizó, respectivamente. No está de más mencionar que, si en la implementación, se reutiliza código de más de un programa o librería de terceros, el programador deberá incluirlos en líneas separadas.

En caso de que la implementación en la que trabaja el programador sea distribuida bajo una licencia de código abierto, deberá incluirse la siguiente nota de copyright:

```
Copyright (C) {{year}} DataInt Consultores S.A. de C.V. - Some Rights Reserved.

This software is distributed under {{license}}. Please see the LICENSE file of the project.

DataInt Consultores S.A. de C.V. is a company constituted under Mexican law with its principal place of business at Mexico City.
```

El programador deberá sustituir `{{year}}` con el año de la primer implementación y `{{license}}` con el nombre de la licencia bajo la cual se distribuye el software.

**Es importante recordar que, en esta sección, cuando se habla de reutilización de código de terceros, se hace referencia a la redistribución de código.** Es decir, **si el programador importa librerías o paqueterías de terceros (sin importar la licencia bajo a cual se distribuyen), éste no está redistribuyendo código** y, por lo tanto, no es necesario hacer las respectivas atribuciones a sus autores originales y DataInt puede declarar que todos los derechos de propiedad intelectual le pertenecen. Sin embargo, si el programador copia código contenido en una librería distribuida por terceros (para hacerle modificaciones o mantenerlo íntegro), es necesario hacer las respectivas atribuciones y declarar que DataInt sólo mantiene algunos derechos de propiedad intelectual.

### 3.1.5. Caracteres fuera de la especificación ASCII

Si en cualquier parte del archivo el programador requiere usar caracteres fuera de la especificación ascii (como caracteres pertenecientes a alfabetos distintos al latino), el programador deberá escribirlo explícitamente y deberá evitar el uso de secuencias hexadecimales o códigos unicode con escape de texto.

**Correcto** :white_check_mark:

```js
// Se recomienda usar la letra griega mu explícitamente
const unidades = "μm";
```

**Incorrecto** :x:

```js
// No se recomienda usar la secuencia hexadecimal o el código unicode con escape de texto
const unidades = "\u03bcm";
```

### 3.1.6. Caracteres especiales

Si en cualquier parte del archivo el programador requiere usar caracteres especiales (como saltos de línea, tabulaciones, espacios en blanco, etc.), el programador deberá hacer uso de la secuencia de escape tradicional (`\"`, `\s`, `\t`, `\v`, etc.) en lugar de secuencias hexadecimales o códigos unicode con escape de texto.

**Correcto** :white_check_mark:

```js
// Se recomienda usar la secuencia de escape tradicional
const título = "Incidencia Delictiva\nMarzo de 2020";
```

**Incorrecto** :x:

```js
// No se recomienda usar la secuencia hexadecimal o el código unicode con escape de texto
const título = "Incidencia Delictiva\x0aMarzo de 2020";
```