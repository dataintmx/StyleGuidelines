# Guía de estilo <!-- omit in toc -->

- [1. Introducción](#1-introducción)
- [2. Guías auxiliares](#2-guías-auxiliares)
  - [2.1. Listado de guías auxiliares](#21-listado-de-guías-auxiliares)
- [3. Lineamientos generales](#3-lineamientos-generales)
  - [3.1. Estructura de proyecto](#31-estructura-de-proyecto)
  - [3.2. Flujo de trabajo con sistema de control de versiones](#32-flujo-de-trabajo-con-sistema-de-control-de-versiones)
    - [3.2.1. Nomenclatura](#321-nomenclatura)
    - [3.2.2. Convención de versionado](#322-convención-de-versionado)
  - [3.3. Archivos de código fuente (_source files_)](#33-archivos-de-código-fuente-source-files)
    - [3.3.1. Codificación](#331-codificación)
    - [3.3.2. Nombre](#332-nombre)
    - [3.3.3. Estructura](#333-estructura)
    - [3.3.4. Copyright](#334-copyright)
    - [3.3.5. Final de archivo](#335-final-de-archivo)
  - [3.4. Disposición del código](#34-disposición-del-código)
    - [3.4.1. Longitud máxima de línea](#341-longitud-máxima-de-línea)
    - [3.4.2. Líneas en blanco](#342-líneas-en-blanco)
    - [3.4.3. Sangrado (_indentation_) y tabulación](#343-sangrado-indentation-y-tabulación)
  - [3.5. Estilo de código](#35-estilo-de-código)
    - [3.5.1. Caracteres fuera de la especificación ASCII](#351-caracteres-fuera-de-la-especificación-ascii)
    - [3.5.2. Caracteres especiales](#352-caracteres-especiales)
    - [3.5.3. Comentarios y documentación en código](#353-comentarios-y-documentación-en-código)
      - [3.5.3.1. Comentarios](#3531-comentarios)
      - [3.5.3.2. Documentación en código (_docstring_)](#3532-documentación-en-código-docstring)
    - [3.5.4. Nomenclatura](#354-nomenclatura)
      - [3.5.4.1. Nomenclatura por tipo de identificador](#3541-nomenclatura-por-tipo-de-identificador)
        - [3.5.4.1.1. Paquetes y módulos](#35411-paquetes-y-módulos)
        - [3.5.4.1.2. Clases](#35412-clases)
        - [3.5.4.1.3. Métodos y funciones](#35413-métodos-y-funciones)
        - [3.5.4.1.4. Variables y constantes globales](#35414-variables-y-constantes-globales)
        - [3.5.4.1.5. Objetos privados](#35415-objetos-privados)
        - [3.5.4.1.6. Parámetros](#35416-parámetros)
        - [3.5.4.1.7. Variables y constantes locales](#35417-variables-y-constantes-locales)
    - [3.5.5. Uso de espacios en expresiones y declaraciones](#355-uso-de-espacios-en-expresiones-y-declaraciones)

# 1. Introducción

En esta guía se definen los lineamientos y convenciones que deberán seguirse al momento de escribir código en proyectos de DataInt. El principal objetivo de la guía es delinear un estándar de consistencia y coherencia en el código. Un proyecto con estilo consistente y coherente es más fácil de leer, entender y, por lo tanto, mantener.

Es importante recordar que esta guía sólo es eso: una guía, es decir, un punto arbitrario de referencia sobre cómo debe verse el código. Es imposible cubrir todos los casos y situaciones en un solo documento. Por esto, el programador siempre tiene la última palabra; con su experiencia y conocimientos, juzgará cómo aplicar la guía y en qué situaciones pueden hacerse excepciones a los lineamientos que en ella se presentan.

Esta guía esta divida en tres partes. En primer lugar, se define un grupo de guías auxiliares para lenguajes de programación en específico. Estas deberán usarse para complementar los lineamientos de esta guía y sólo deberán usarse en aquellos casos que no se encuentran contemplados en este documento. En segundo lugar, se presentan los lineamientos generales de la organización. Aquí se definen algunas reglas básicas para trabajar en los proyectos de DataInt. Estas reglas deberán seguirse, en la medida de lo posible, en todos los lenguajes de programación. En la tercera parte, se definen reglas específicas para cada lenguaje de programación. Si una regla específica para un lenguaje de programación entra en conflicto con un lineamiento general, la regla específica tendrá preferencia sobre el lineamiento general.

# 2. Guías auxiliares

A continuación se definen las guías auxiliares a la guía de estilo de DataInt. Las guías auxiliares son guías de estilo usadas por otras organizaciones (principalmente Google) y cuya función es complementar los lineamientos que se definen en este documento. Las guías auxiliares son específicas a cada lenguaje de programación.

Las guías auxiliares deberán usarse en aquellos casos que no son cubiertos por la guía de estilo de DataInt. Si una regla en una guía auxiliar entra en conflicto con una regla específica de lenguaje o un lineamiento general definidos en este documento, las reglas o lineamientos definidos aquí tendrán preferencia sobre aquellas definidas en una guía auxiliar. En resumen, la jerarquía de reglas es la siguiente:

1. Reglas específicas para lenguajes de programación (guía de estilo de DataInt).
2. Lineamientos generales (guía de estilo de DataInt).
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
const name = "Fulano";
const last_name = "Pérez";
const phone = "1010101010";

// Pet info
// Note the declaration is separated from the previous block of declarations by one space, 
// since it belongs to a different group
const phone = ["Negrito", "Panchito"];


// Before a class declaration, two blank lines
class Persona {
  constructor(name, last_name, phone, pets) {
    this.name = name;
    this.last_name = last_name;
    this.phone = phone;
    this.pets = pets
  }

  // Before and after functions and methods, one blank line
  get name_to_upper() {
    return this.name.toUpperCase();
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
const name = "Fulano";
const last_name = "Pérez";
const phone = "1010101010";
const phone = ["Negrito", "Panchito"];

class Persona {
  constructor(name, last_name, phone, pets) {
    this.name = name;
    this.last_name = last_name;
    this.phone = phone;
    this.pets = pets
  }
  get name_to_upper() {
    return this.name.toUpperCase();
  }
}
```

### 3.2.3. Sangrado (_indentation_) y tabulación

Cada vez que se abre un nuevo bloque de código, se incrementa el **sangrado en 4 espacios en blanco** (`\s`). El sangrado del código deberá hacerse con espacios en blanco y deberá evitarse el uso de tabuladores (`\t`).

## 3.3. Estilo de código

### 3.3.1. Caracteres fuera de la especificación ASCII

Si el programador requiere usar caracteres fuera de la especificación ascii (como caracteres pertenecientes a alfabetos distintos al latino), el programador deberá escribirlo explícitamente y deberá evitar el uso de secuencias hexadecimales o códigos unicode con escape de texto.

**Correcto** :white_check_mark:

```js
// Explicit use of the greek letter 'mu'
const units = "μm";
```

**Incorrecto** :x:

```js
// Don't use escaped hexadecimal or unicode
const units = "\u03bcm";
```

### 3.3.2. Caracteres especiales

Si el programador requiere usar caracteres especiales (como saltos de línea, tabulaciones, espacios en blanco, etc.), el programador deberá hacer uso de la secuencia de escape tradicional (`\"`, `\s`, `\t`, `\v`, etc.) en lugar de secuencias hexadecimales o códigos unicode con escape de texto.

**Correcto** :white_check_mark:

```js
// Always use the 'traditional' escaped character
const title = "Incidencia Delictiva\nMarzo de 2020";
```

**Incorrecto** :x:

```js
// Don't use the ascii escaped codes
const title = "Incidencia Delictiva\x0aMarzo de 2020";
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

### 3.3.4. Nomenclatura

Los nombres de objetos, funciones, métodos y clases **sólo podrán escribirse usando caracteres ASCII** (esto incluye el uso de acentos y la letra "ñ"). **Los nombres deben ser en inglés**. En el caso excepcional de que sean en castellano, se recomienda seguir las reglas de ortografía (es decir, acentuar correctamente y evitar la sustitución de `ñ` por `ni`: `año -> anio`).

El programador, en la medida de lo posible, siempre debe priorizar el uso de **nombres completos y descriptivos de los objetos**, funciones, métodos y clases en el código. Es decir, el programador debe evitar abreviaciones ambiguas, siglas y acrónimos ambiguos, así como la remoción de vocales. De igual forma, debe evitarse el uso de [notación húngara](https://en.wikipedia.org/wiki/Hungarian_notation). 

El programador podrá hacer excepciones en el caso de funciones estadísticas donde hay un uso razonablemente común de letras (latinas y griegas) para designar algunos objetos. Por ejemplo, las medias tienden a denotarse `mu`, la desviación estándar `s`, el tamaño de muestra `n`, la probabilidad `p` o `pi`, etc.

#### 3.3.4.1. Nomenclatura por tipo de identificador

##### 3.3.4.1.1. Paquetes y módulos

Los nombres de paquetes y módulos de código siempre deben ser `UpperCamelCase`. Por ejemplo: `DataIntAuth.Core.DataIntUser`.

##### 3.3.4.1.2. Clases

Los nombres de clases siempre deben ser `UpperCamelCase`. Por ejemplo: `DataIntUser`.

##### 3.3.4.1.3. Métodos y funciones

Los nombres de métodos y funciones siempre deben ser `lower_snake_case`, por ejemplo `DataIntUser.create_token()`.

##### 3.3.4.1.4. Variables y constantes globales

Los nombres de variables y constantes globales —incluidas las de ambiente (_environment_)— deben ser `UPPER_SNAKE_CASE`.

##### 3.3.4.1.5. Objetos privados

En idiomas de programación que no dispongan de una definición formal de objeto (propiedades, métodos, funciones, etc.) privado, éstas se denotarán con un guión bajo como prefijo ( `_` ). Por ejemplo: `_propiedad_privada`.

##### 3.3.4.1.6. Parámetros

Los parámetros de funciones y constructores de clase se escribirán en `lower_snake_case`.

##### 3.3.4.1.7. Variables y constantes locales

Los nombres de variables y constantes locales se escribirán en `lower_snake_case`.

### 3.3.5. Uso de espacios en expresiones y declaraciones

Al menos que el lenguaje de programación asi lo requiera, deberá evitarse añadir espacios en blanco inmediatamente al interior de paréntesis o llaves.

**Correcto** :white_check_mark:

```js
const my_formula = x_1 + x_2 * b_2 + x_3 * (b_3 + c);
```

**Incorrecto** :x:

```js
const my_formula = x_1 + x_2 * b_2 + x_3 * ( b_3 + c );
```

Al menos que el lenguaje de programación así lo requiera, deberá evitarse añadir espacios en blanco después de una coma y antes de un paréntesis o llave de cierre.

**Correcto** :white_check_mark:

```js
var array = [1, 3, 3,];
```

**Incorrecto** :x:

```js
var array = [1, 3, 3, ];
```

Al menos que el lenguaje de programación así lo requiera, deberá evitarse añadir espacios en blanco inmediatamente antes de comas.

**Correcto** :white_check_mark:

```js
var array = [1, 3, 3];
```

**Incorrecto** :x:

```js
var array = [1 , 3 , 3];
```

Deberá evitarse añadir espacios en blanco para alinear expresiones en el archivo.

**Correcto** :white_check_mark:

```js
const a = 1;
const b = 2;
const long_const_name = 99;
```

**Incorrecto** :x:

```js
const a               = 1;
const b               = 2;
const long_const_name = 99;
```

Siempre deberá añadirse un espacio en lanco al rededor de operadores binarios (`<`, `>`, `!=`, etc.) y expresiones de asignación (`=`, `<-`, `->`, `+=`, etc.).

**Correcto** :white_check_mark:

```js
const a = 1;
const b = 2;
const a_bigger_than_b = a > b;
```

**Incorrecto** :x:

```js
const a=1;
const b=2;
const a_bigger_than_b=a>b;
```
