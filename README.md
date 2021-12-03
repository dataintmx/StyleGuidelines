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
    - [3.1.5. Final de archivo](#315-final-de-archivo)
  - [3.2. Disposición del código](#32-disposición-del-código)
    - [3.2.1. Longitud máxima de línea](#321-longitud-máxima-de-línea)
    - [3.2.2. Líneas en blanco](#322-líneas-en-blanco)
    - [3.2.3. Sangrado (_indentation_) y tabulación](#323-sangrado-indentation-y-tabulación)
  - [3.3. Estilo de código](#33-estilo-de-código)
    - [3.3.1. Caracteres fuera de la especificación ASCII](#331-caracteres-fuera-de-la-especificación-ascii)
    - [3.3.2. Caracteres especiales](#332-caracteres-especiales)
    - [3.3.3. Comentarios y documentación en código](#333-comentarios-y-documentación-en-código)
      - [3.3.3.1. Comentarios](#3331-comentarios)
      - [3.3.3.2. Documentación en código (_docstring_)](#3332-documentación-en-código-docstring)
    - [3.3.4. Nomenclatura](#334-nomenclatura)
      - [3.3.4.1. Nomenclatura por tipo de identificador](#3341-nomenclatura-por-tipo-de-identificador)
        - [3.3.4.1.1. Paquetes y módulos](#33411-paquetes-y-módulos)
        - [3.3.4.1.2. Clases](#33412-clases)
        - [3.3.4.1.3. Métodos y funciones](#33413-métodos-y-funciones)
        - [3.3.4.1.4. Variables y constantes globales](#33414-variables-y-constantes-globales)
        - [3.3.4.1.5. Objetos privados](#33415-objetos-privados)
        - [3.3.4.1.6. Parámetros](#33416-parámetros)
        - [3.3.4.1.7. Variables y constantes locales](#33417-variables-y-constantes-locales)
    - [3.3.5. Uso de espacios en expresiones y declaraciones](#335-uso-de-espacios-en-expresiones-y-declaraciones)

# 1. Introducción

En esta guía se definen los lineamientos y convenciones que deberán seguirse al momento de escribir código en proyectos de DataInt. El principal objetivo de la guía es delinear un estándar de consistencia y coherencia en el código. Un proyecto con estilo consistente y coherente es más fácil de leer, entender y, por lo tanto, mantener.

Es importante recordar que esta guía sólo es eso: una guía, es decir, un punto arbitrario de referencia sobre cómo debe verse el código. Es imposible cubrir todos los casos y situaciones en un solo documento. Por esto, el programador siempre tiene la última palabra; con su experiencia y conocimientos, juzgará cómo aplicar la guía y en qué situaciones pueden hacerse excepciones a los lineamientos que en ella se presentan.

Esta guía esta divida en tres partes. En primer lugar, se define un grupo de guías auxiliares para lenguajes de programación en específico. Estas deberán usarse para complementar los lineamientos de esta guía y sólo deberán usarse en aquellos casos que no se encuentran contemplados en este documento. En segundo lugar, se presentan los lineamientos generales de la organización. Aquí se definen algunas reglas básicas para trabajar en los proyectos de DataInt. Estas reglas deberán seguirse, en la medida de lo posible, en todos los lenguajes de programación. En la tercera parte, se definen reglas específicas para cada lenguaje de programación. Si una regla específica para un lenguaje de programación entra en conflicto con un lineamiento general, la regla específica tendrá preferencia sobre el lineamiento general.

# 2. Guías auxiliares

A continuación se definen las guías auxiliares a la guía de estilo de DataInt. Las guías auxiliares son guías de estilo usadas por otras organizaciones (principalmente Google) y cuya función es complementar los lineamientos que se definen en este documento. Las guías auxiliares son específicas a cada lenguaje de programación.

Las guías auxiliares deberán usarse en aquellos casos que no son cubiertos por la guía de estilo de DataInt. Si una regla en una guía auxiliar entra en conflicto con una regla específica de lenguaje o un lineamiento general definidos en este documento, las reglas o lineamientos definidos aquí tendrán preferencia sobre aquellas definidas en una guía auxiliar. En resumen, la jerarquía de reglas es la siguiente:

1. Lineamientos generales (guía de estilo de DataInt).
2. Reglas específicas para lenguajes de programación (guía de estilo de DataInt).
3. Guía auxiliar de estilo.

Si en la guía de estilo de DataInt no hay reglas específicas para un lenguaje de programación, el programador deberá usar la guía de estilo definida por Google para dicho lenguaje de programación. Las guías de estilo de Google pueden encontrarse en [su respectivo repositorio](https://github.com/google/styleguide).

## 2.1. Listado de guías auxiliares

- **JavaScript**: [Guía de estilo para JavaScript de Google](https://google.github.io/styleguide/jsguide.html).
- **TypeScript**: [Guía de estilo para TypeScript de Google](https://google.github.io/styleguide/tsguide.html).
- **Python**: [Guía de estilo para Python definida en la PEP-0008](https://www.python.org/dev/peps/pep-0008/).
- **HTML y CSS**: [Guía de estilo para HTML/CSS de Google](https://google.github.io/styleguide/htmlcssguide.html).
- **PHP**: [Guía de estilo para PHP de WordPress](https://developer.wordpress.org/coding-standards/wordpress-coding-standards/php/).

# 3. Lineamientos generales

En esta sección se definen los lineamientos generales para escribir código en los proyectos de DataInt. Los lineamientos generales deberán seguirse, en la medida de lo posible, en todo los lenguajes de programación. Ante cualquier situación no cubierta en estos lineamientos generales, el programador deberá remitirse a los lineamientos específicos para su lenguaje de programación y, en su defecto, a una de las guías auxiliares.

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

```Markdown
Copyright (C) {year} DataInt Consultores S.A. de C.V. - All Rights Reserved.

This file and its contents are regarded as proprietary and confidential.
Unauthorized copying of this file, via any medium is strictly prohibited.

DataInt Consultores S.A. de C.V. is a company constituted under Mexican law with its principal place of business at Mexico City.
```

El programador deberá sustituir `{year}` con el año de la primer implementación (es decir, el año en el que se creo el archivo). 

En caso que la implementación sea propietaria y reutilice código abierto de terceros, la nota de copyright deberá ser la siguiente:

```Markdown
Copyright (C) {year} DataInt Consultores S.A. de C.V. - Some Rights Reserved.
Copyright (C) {os_code_year} {os_code_author} // {os_code_status}

This file and some of its contents are regarded as proprietary and confidential.
Unauthorized copying of this file, via any medium is strictly prohibited.

This implementation reuses the following works:
{os_code_author}, {os_code_name}, {os_code_author}, licensed under {os_code_license}

DataInt Consultores S.A. de C.V. is a company constituted under Mexican law with its principal place of business at Mexico City.
```

El programador deberá sustituir `{year}` con el año de la primer implementación. De igual forma, el programador deberá sustituir `{os_code_year}`, `{os_code_author}`, `{os_code_status}`, `{os_code_license}` y `{os_code_name}` por el año de publicación del código reutilizado, el nombre completo del autor del código reutilizado, el estado del código reutilizado (`modified` o `unchanged`), el nombre de a licencia bajo la cual se distribuyó el código y el nombre del programa o librería que se reutilizó, respectivamente. No está de más mencionar que, si en la implementación, se reutiliza código de más de un programa o librería de terceros, el programador deberá incluirlos en líneas separadas.

En caso de que la implementación en la que trabaja el programador sea distribuida bajo una licencia de código abierto, deberá incluirse la siguiente nota de copyright:

```Markdown
Copyright (C) {year} DataInt Consultores S.A. de C.V. - Some Rights Reserved.

This software is distributed under {license}. Please see the LICENSE file of the project.

DataInt Consultores S.A. de C.V. is a company constituted under Mexican law with its principal place of business at Mexico City.
```

El programador deberá sustituir `{year}` con el año de la primer implementación y `{license}` con el nombre de la licencia bajo la cual se distribuye el software.

**Es importante recordar que, en esta sección, cuando se habla de reutilización de código de terceros, se hace referencia a la redistribución de código.** Es decir, **si el programador importa librerías o paqueterías de terceros (sin importar la licencia bajo a cual se distribuyen), éste no está redistribuyendo código** y, por lo tanto, no es necesario hacer las respectivas atribuciones a sus autores originales y DataInt puede declarar que todos los derechos de propiedad intelectual le pertenecen. Sin embargo, si el programador copia código contenido en una librería distribuida por terceros (para hacerle modificaciones o mantenerlo íntegro), es necesario hacer las respectivas atribuciones y declarar que DataInt sólo mantiene algunos derechos de propiedad intelectual.

### 3.1.5. Final de archivo

Todos los archivos deberán terminar con un salto de línea (`\n`) o, en su defecto, un retorno de carro con nueva línea (`\rn`). 

## 3.2. Disposición del código

### 3.2.1. Longitud máxima de línea

Las líneas de código deberán limitarse a **120 caracteres**.

Las líneas de comentarios y documentación en código (_docstring_) deberán limitarse a **80 caracteres** para facilitar su legibilidad.

### 3.2.2. Líneas en blanco

Deberán colocarse una línea en blanco después de la nota de copyright al inicio del archivo.

Deberán colocarse dos líneas en blanco por encima de definiciones de clases.

Deberán colocarse una línea en blanco al rededor de definiciones de métodos o funciones.

El programador deberá separar con líneas en blanco grupos de declaraciones, métodos o funciones.

**Correcto** :white_check_mark:

```js
// Copyright (C) {year} DataInt Consultores S.A. de C.V. - All Rights Reserved.
//
// This file and its contents are regarded as proprietary and confidential.
// Unauthorized copying of this file, via any medium is strictly prohibited.
//
// DataInt Consultores S.A. de C.V. is a company constituted under Mexican law with its principal place of business
// at Mexico City.

// Personal info
const nombre = "Fulano";
const apellido = "Pérez";
const teléfono = "1010101010";

// Pet info
// Note the declaration is separated from the previous block of declarations by one space, 
// since it belongs to a different group
const mascotas = ["Negrito", "Panchito"];


// Before a class declaration, two blank lines
class Persona {
  constructor(nombre, apellido, teléfono, mascotas) {
    this.nombre = nombre;
    this.apellido = apellido;
    this.teléfono = teléfono;
    this.mascotas = mascotas
  }

  // Before and after functions and methods, one blank line
  get nombre_en_mayusculas() {
    return this.nombre.toUpperCase();
  }

}
```

**Incorrecto** :x:

```js
// Copyright (C) {year} DataInt Consultores S.A. de C.V. - All Rights Reserved.
//
// This file and its contents are regarded as proprietary and confidential.
// Unauthorized copying of this file, via any medium is strictly prohibited.
//
// DataInt Consultores S.A. de C.V. is a company constituted under Mexican law with its principal place of business
// at Mexico City.
const nombre = "Fulano";
const apellido = "Pérez";
const teléfono = "1010101010";

class Persona {
  constructor(nombre, apellido, teléfono, mascotas) {
    this.nombre = nombre;
    this.apellido = apellido;
    this.teléfono = teléfono;
    this.mascotas = mascotas
  }
  get nombre_en_mayusculas() {
    return this.nombre.toUpperCase();
  }
}
```

### 3.2.3. Sangrado (_indentation_) y tabulación

Cada vez que se abre un nuevo bloque de código, se incrementa el sangrado en 4 espacios en blanco (`\s`). El sangrado del código deberá hacerse con espacios en blanco y deberá evitarse el uso de tabuladores (`\t`).

## 3.3. Estilo de código

### 3.3.1. Caracteres fuera de la especificación ASCII

Si el programador requiere usar caracteres fuera de la especificación ascii (como caracteres pertenecientes a alfabetos distintos al latino), el programador deberá escribirlo explícitamente y deberá evitar el uso de secuencias hexadecimales o códigos unicode con escape de texto.

**Correcto** :white_check_mark:

```js
// Explicit use of the greek letter 'mu'
const unidades = "μm";
```

**Incorrecto** :x:

```js
// Don't use escaped hexadecimal or unicode
const unidades = "\u03bcm";
```

### 3.3.2. Caracteres especiales

Si el programador requiere usar caracteres especiales (como saltos de línea, tabulaciones, espacios en blanco, etc.), el programador deberá hacer uso de la secuencia de escape tradicional (`\"`, `\s`, `\t`, `\v`, etc.) en lugar de secuencias hexadecimales o códigos unicode con escape de texto.

**Correcto** :white_check_mark:

```js
// Always use the 'traditional' escaped character
const título = "Incidencia Delictiva\nMarzo de 2020";
```

**Incorrecto** :x:

```js
// Don't use the ascii escaped codes
const título = "Incidencia Delictiva\x0aMarzo de 2020";
```

### 3.3.3. Comentarios y documentación en código

#### 3.3.3.1. Comentarios

Todo el código debe comentarse. El programador siempre debe tener en mente que debe dejar una nota describiendo qué hacen sus funciones, declaraciones, clases, métodos e importaciones, siempre que éstas no sean explícitas y descriptivas. Estas notas deben ser suficientemente claras para que, otros colaboradores del proyecto (dentro y fuera de DataInt), puedan entender el código que están leyendo.

**Los comentarios en el código siempre deberán escribirse en inglés**. 

En idiomas de programación que permiten bloques de comentarios, se recomienda reservar la notación de bloque para comentarios que abarquen más de una línea. Si el comentario sólo abarca una línea, se recomienda usar exclusivamente la marca de línea comentada por default.

**Correcto** :white_check_mark:

```js
// This is a single line comment

/*
This is a multiline comment. Lorem ipsum dolor sit amet, 
consectetur adipiscing elit. Phasellus ante leo, auctor id dolor vel, rhoncus viverra massa. 
Cras in feugiat arcu. In vehicula est ligula, eu efficitur libero aliquam vel. 
*/


// This is a multiline comment. Lorem ipsum dolor sit amet, 
// consectetur adipiscing elit. Phasellus ante leo, auctor id dolor vel, rhoncus viverra massa. 
// Cras in feugiat arcu. In vehicula est ligula, eu efficitur libero aliquam vel. 
```

**Incorrecto** :x:

```js
// Este es un comentario en español

/* Don't use block comment notation for single line comments! */
```

#### 3.3.3.2. Documentación en código (_docstring_)

En idiomas de programación que permiten el uso de _docstrings_, o cadenas de documentación en código, el programador deberá hacer uso de esta herramienta. El uso de _docstrings_ no menoscabará, ni remplazará, el uso de comentarios para describir el código.

Toda documentación en código deberá contener, por lo menos, los siguientes elementos:

1. Descripción breve de la función, método o clase.
2. Nombre de los parámetros requeridos, su tipo y una breve descripción.
3. Tipo del objeto devuelto (_return_) y descripción.