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
    - [3.3.4. Final de archivo](#334-final-de-archivo)
  - [3.4. Disposición del código](#34-disposición-del-código)
    - [3.4.1. Longitud máxima de línea](#341-longitud-máxima-de-línea)
    - [3.4.2. Tamaño y estructura de las clases](#342-tamaño-y-estructura-de-las-clases)
    - [3.4.3. Líneas en blanco](#343-líneas-en-blanco)
    - [3.4.4. Sangrado (_indentation_) y tabulación](#344-sangrado-indentation-y-tabulación)
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
- [4. Archivos de configuración](#4-archivos-de-configuración)
  - [4.1. Python](#41-python)
    - [4.1.1. Pylint](#411-pylint)

# 1. Introducción

En esta guía se definen los lineamientos y convenciones que deberán seguirse al momento de escribir código en proyectos
de DataInt. El principal objetivo de la guía es delinear un estándar de consistencia y coherencia en el código. Un
proyecto con estilo consistente y coherente es más fácil de leer, entender y, por lo tanto, mantener.

Es importante recordar que esta guía solo es eso: una guía, es decir, un punto arbitrario de referencia sobre cómo debe
verse el código. Es imposible cubrir todos los casos y situaciones en un solo documento. Por esto, el programador
siempre tiene la última palabra; con su experiencia y conocimientos, juzgará cómo aplicar la guía y en qué situaciones
pueden hacerse excepciones a los lineamientos que en ella se presentan.

Esta guía esta divida en cuatro partes. En primer lugar, se define un grupo de guías auxiliares para lenguajes de
programación en específico. Estas deberán usarse para complementar los lineamientos de esta guía y solo deberán usarse
en aquellos casos que no se encuentran contemplados en este documento. En segundo lugar, se presentan los lineamientos
generales de la organización. Aquí se definen algunas reglas básicas para trabajar en los proyectos de DataInt. Estas
reglas deberán seguirse, en la medida de lo posible, en todos los lenguajes de programación. En la tercera parte, se
definen reglas específicas para cada lenguaje de programación. Si una regla específica para un lenguaje de programación
entra en conflicto con un lineamiento general, la regla específica tendrá preferencia sobre el lineamiento general.
Finalmente, en la cuarta parte se presentan archivos de configuración que pueden usarse con IDEs y otras herramientas
de análisis de código estático ([_linters_](https://en.wikipedia.org/wiki/Lint_(software))) para detectar inconsistencias y violaciones a las recomendaciones de esta guía.

# 2. Guías auxiliares

A continuación se definen las guías auxiliares a la guía de estilo de DataInt. Las guías auxiliares son guías de estilo
usadas por otras organizaciones (principalmente Google) y cuya función es complementar los lineamientos que se definen
en este documento. Las guías auxiliares son específicas a cada lenguaje de programación.

Las guías auxiliares deberán usarse en aquellos casos que no son cubiertos por la guía de estilo de DataInt. Si una
regla en una guía auxiliar entra en conflicto con una regla específica de lenguaje o un lineamiento general definidos en
este documento, las reglas o lineamientos definidos aquí tendrán preferencia sobre aquellas definidas en una guía
auxiliar. En resumen, la jerarquía de reglas es la siguiente:

1. Reglas específicas para lenguajes de programación (guía de estilo de DataInt).
2. Lineamientos generales (guía de estilo de DataInt).
3. Guía auxiliar de estilo.

Si en la guía de estilo de DataInt no hay reglas específicas para un lenguaje de programación, el programador deberá
usar la guía de estilo definida por Google para dicho lenguaje de programación. Las guías de estilo de Google pueden
encontrarse en [su respectivo repositorio](https://github.com/google/styleguide).

## 2.1. Listado de guías auxiliares

- **JavaScript**: [Guía de estilo para JavaScript de Google](https://google.github.io/styleguide/jsguide.html).
- **TypeScript**: [Guía de estilo para TypeScript de Google](https://google.github.io/styleguide/tsguide.html).
- **Python**: [Guía de estilo para Python definida en la PEP-0008](https://www.python.org/dev/peps/pep-0008/).
- **HTML y CSS**: [Guía de estilo para HTML/CSS de Google](https://google.github.io/styleguide/htmlcssguide.html).
- **PHP**: [Guía de estilo para PHP de WordPress](https://developer.wordpress.org/coding-standards/wordpress-coding-standards/php/).

# 3. Lineamientos generales

En esta sección se definen los lineamientos generales para escribir código en los proyectos de DataInt. Los lineamientos
generales deberán seguirse, en la medida de lo posible, en todo los lenguajes de programación. Ante cualquier situación
no cubierta en estos lineamientos generales, el programador deberá remitirse a los lineamientos específicos para su
lenguaje de programación y, en su defecto, a una de las guías auxiliares.

## 3.1. Estructura de proyecto

Al iniciarse un proyecto nuevo, el programador deberá crear un directorio en blanco donde se colocarán todos los
archivos del proyecto. De igual forma, el programador deberá generar un repositorio de git en el directorio. Todos los
proyectos de DataInt deberán usar git como _software_ de control de cambios, incluso cuando el proyecto no sea alojado
en un servidor git (como GitHub).

La implementación de parches, nuevas características, _hotfixes_, o cualquier modificación sobre un trabajo ya existente
no requiere la creación de un nuevo espacio de trabajo (directorio + control de cambios), a menos que así sea
expresamente indicado por el responsable del proyecto.

En el nivel principal (_root_, `/`) del repositorio, siempre deberán estar presentes estos archivos:

1. README: Un, léeme con una descripción breve de los contenidos del repositorio.
2. LICENSE: Un archivo con la nota de copyright, si el código del proyecto es propietario, o una licencia de código
   abierto, si el proyecto es _open source_.

El programador deberá evitar, en la medida de lo posible, incluir archivos de código fuente (_source files_) en el nivel
principal (_root_, `/`) del proyecto.

## 3.2. Flujo de trabajo con sistema de control de versiones

El programador deberá tener en cuenta las siguientes reglas al momento de trabajar con git en los proyectos de DataInt:

1. La rama principal del proyecto y la que contendrá la última versión estable del código se llamará `master`.
2. El programador deberá evitar trabajar directamente cambios sobre la rama `master`.
3. Todo proyecto de DataInt deberá tener una rama de desarrollo que se llamará `dev`.
4. La rama `dev` será una bifurcación de `master`.
5. Cada vez que el programador empiece la implementación de una nueva característica o tarea, deberá crear una
   bifurcación de `dev` hacia una nueva rama `feat/*`. Una vez terminada la implementación de la nueva característica,
   deberá hacer un _merge_ con la rama de desarrollo `dev` o, en su defecto, solicitar un _pull request_ o un _merge
   request_ al responsable de proyecto (según las reglas previamente definidas del proyecto).
6. Cada vez que el programador empiece a trabajar en parches o soluciones a problemas que se presentaron en
   características ya implementadas del código, deberá crear una bifurcación de `dev` hacia una nueva rama `fix/*`. Una
   vez terminada la implementación de la solución, deberá hacer un _merge_ con la rama de desarrollo `dev` o, en su
   defecto, solicitar un _pull request_ o un _merge request_ al responsable de proyecto (según las reglas previamente
   definidas del proyecto).
7. Cuando el responsable de proyecto así lo indique, deberá crearse una rama de entrega o _release_ `release/*`. La
   rama `release/*` deberá ser una bifurcación del estado que guarda la rama `dev`.
8. Una vez creada la rama `release/*`, los integrantes del proyecto no podrán crear nuevas ramas de
   características (`feat/*`) y solo podrán limitar su trabajo en el proyecto a tareas de documentación y arreglo de _
   bugs_ presentes en la rama `release/*`.
9. Para el arreglo de _bugs_ y otros problemas en el código detectados en la rama `release/*`, el programador deberá
   crear una rama `bugfix/*` a partir de `release/*`. Una vez terminada la implementación del parche, el programador
   deberá hacer un _merge_ con la rama de entrega `release/*` o, en su defecto, solicitar un _pull request_ o un _merge
   request_ al responsable de proyecto (según las reglas previamente definidas del proyecto).
10. En algunos proyectos será necesario liberar versiones de acceso temprano para realizar pruebas directamente con
    clientes o con otras áreas de DataInt. En estos casos, el equipo de desarrollo podrá montar la aplicación o servicio
    directamente desde la última rama `release/*`. Los parches para problemas detectados en esta prueba de etapas sobre
    acceso temprano se realizarán conforme a lo estipulado en el punto 9 de estos lineamientos.
11. Cuando el responsable de proyecto así lo indique, y el _software_ esté listo para entrega, se hará un _merge_ entre
    la rama `release/*` y el `master` del repositorio.
12. Si el equipo de desarrollo detecta un problema en la última versión del código disponible en la rama `master`, podrá
    realizarse un parche directamente sobre esta rama. Este tipo de parches deberán realizarse en una rama `hotfix/*`
    que se bifurcará directamente de `master` y deberá ser fusionada directamente con esta (previa autorización del
    responsable del proyecto o vía _pull request_). Los parches `hotfix/*` solo deberán ser aplicados en los siguientes
    casos: i) cuando el equipo de desarrollo no programe otro _release_ del producto en un periodo menor a 30 días y ii)
    cuando la implementación del `hotfix/*` propuesto sea razonablemente menor y no tenga un impacto directo en el
    usuario final.
13. Los equipos de desarrollo deberán dar seguimiento a errores y problemas en el código usando los sistemas de _issues_
    proporcionados por las plataformas de alojamiento de repositorios, como GitHub o GitLab.

### 3.2.1. Nomenclatura

Los nombres de las ramas en las que trabaja el programador deberán ser claros y descriptivos del trabajo realizado,
evitando, en la medida de lo posible, abreviaciones o siglas. 
**Solo se permitirá el uso de siglas reconocidas de forma internacional**.

**Deberá usarse el idioma inglés para nombrar las ramas de trabajo** y solo puede usarse el guion medio `-` como
separador de palabras. Las diagonales `/` se reservarán para etiquetas o categorías como prefijo del nombre de la rama.

Los prefijos permitidos, como se estableció en la sección anterior, son: `feat/`, `fix/`, `release/`, `bugfix/`
y `hotfix/`.

En el caso de parches o soluciones (`fix/`, `bugfix/` y `hotfix/`), el nombre de la rama debe empezar con el
identificador de problema asignado por el sistema de _issues_ proporcionados por las plataformas de alojamiento de
repositorios, como GitHub o GitLab.

**Correcto** :white_check_mark:

```bash
git checkout -b feat/function-to-compute-differences
git checkout -b fix/12-map-not-changing
```

**Incorrecto** :x:

```bash
git checkout -b wip-nuevos-colores-en-mapa
git checkout -b feat/NewColorSchemeForMaps
```

### 3.2.2. Convención de versionado

En el caso de las ramas `release/*`, estas siempre recibirán como nombre la versión del producto. Los proyectos de
DataInt usarán [CalVer](https://calver.org/) como la convención de versionado. Esta convención está basada en fechas de
liberación y no en un identificador incremental (como Ubuntu, ECMAScript o Pip).

La versión de proyectos de DataInt seguirá el siguiente patrón: `YY.0M.MINOR-PRE`, donde `YY` es el año a dos
dígitos, `0M` es el mes en número y con prefijo cero (`08`, `09`, `10`, etc.), `MINOR` es un indicativo de la "versión
menor" del producto, es decir, parches y reparaciones que no rompen la compatibilidad del producto, y `PRE` es un
identificador de acceso temprano (_pre-release_) que puede ser `alpha`, `beta` o `rc`.

`PRE` es el único componente opcional y solo será usado cuando las características del proyecto así lo requieran.

**Correcto** :white_check_mark:

```bash
git checkout -b release/v21.12.0
git checkout -b release/v22.01.0-alpha
git checkout -b release/v22.01.0-rc
```

**Incorrecto** :x:

```bash
git checkout -b release/v22.7.1
git checkout -b release/v0.0.1
git checkout -b release/latest
```

## 3.3. Archivos de código fuente (_source files_)

### 3.3.1. Codificación

Todos los archivos deberán ser codificados en **UTF-8**.

### 3.3.2. Nombre

Los nombres de los archivos siempre deberán ser en minúsculas (_lowercase_) y podrán contener guiones medios ( `-` ) y
bajos ( `_` ).

Los nombres de archivo no podrán contener signos de puntuación adicionales a los requeridos para especificar la
extensión del archivo (`.py`, `.js`, etc.).

Los nombres de archivos no podrán contener espacios en blanco.

### 3.3.3. Estructura

Los archivos con código deberán tener, en la medida de lo posible, la siguiente estructura:

1. Shebang, si es requerido (solo en los puntos de entrada).
2. Importación de dependencias de la librería estándar.
3. Importación de dependencias escritas por terceros.
4. Importación de dependencias escritas por DataInt.
5. Implementación.

### 3.3.4. Final de archivo

Todos los archivos deberán terminar con un salto de línea (`\n`) o, en su defecto, un retorno de carro con nueva
línea (`\rn`).

## 3.4. Disposición del código

### 3.4.1. Longitud máxima de línea

Las líneas de código deberán limitarse a **120 caracteres**.

Las líneas de comentarios y documentación en código (_docstring_) deberán limitarse a **80 caracteres** para facilitar
su legibilidad.

### 3.4.2. Tamaño y estructura de las clases

Las clases deben limitarse, en la medida de lo posible, a 500 líneas de código, 5 atributos y 20 métodos de hasta 25 
líneas de código.

### 3.4.3. Líneas en blanco

Deberán colocarse dos líneas en blanco por encima de definiciones de clases.

Deberán colocarse una línea en blanco alrededor de definiciones de métodos o funciones.

El programador deberá separar con líneas en blanco grupos de declaraciones, métodos o funciones.

**Correcto** :white_check_mark:

```js
const name = "Fulano";
const last_name = "Pérez";
const phone = "1010101010";

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

### 3.4.4. Sangrado (_indentation_) y tabulación

Cada vez que se abre un nuevo bloque de código, se incrementa el **sangrado en 4 espacios en blanco** (`\s`). El
sangrado del código deberá hacerse con espacios en blanco y deberá evitarse el uso de tabuladores (`\t`).

## 3.5. Estilo de código

### 3.5.1. Caracteres fuera de la especificación ASCII

Si el programador requiere usar caracteres fuera de la especificación ascii (como caracteres pertenecientes a alfabetos
distintos al latino), el programador deberá escribirlo explícitamente y deberá evitar el uso de secuencias hexadecimales
o códigos unicode con escape de texto.

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

### 3.5.2. Caracteres especiales

Si el programador requiere usar caracteres especiales (como saltos de línea, tabulaciones, espacios en blanco, etc.), el
programador deberá hacer uso de la secuencia de escape tradicional (`\"`, `\s`, `\t`, `\v`, etc.) en lugar de secuencias
hexadecimales o códigos unicode con escape de texto.

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

### 3.5.3. Comentarios y documentación en código

#### 3.5.3.1. Comentarios

Solamente se debe comentar las instrucciones que, debido a su complejidad, son difíciles de comprender 
(por ejemplo: expresiones regulares). En estos casos, debe priorizarse la actualización de estos comentarios 
después de aplicar un cambio. Por lo tanto, **los nombres de las clases, propiedades y métodos deben ser
lo suficientemente claros y descriptivos para que no sea necesario comentar el código**.

**Los comentarios en el código siempre deberán escribirse en inglés**.

En idiomas de programación que permiten bloques de comentarios, se recomienda reservar la notación de bloque para
comentarios que abarquen más de una línea. Si el comentario solo abarca una línea, se recomienda usar exclusivamente la
marca de línea comentada por default.

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

#### 3.5.3.2. Documentación en código (_docstring_)

Únicamente en proyectos donde se implementen librerías nuevas y resulte necesario aprovechar las
herramientas de documentación automática a través de _docstring_, los desarrolladores harán uso de _docstring_. 
Esta documentación deben ser suficientemente claras para que otros colaboradores del proyecto (dentro y fuera de
DataInt), puedan entender el código que están leyendo.

El uso de _docstrings_ no menoscabará, ni remplazará, el uso de comentarios para
describir el código cuando sea necesario.

Toda documentación en código deberá contener, por lo menos, los siguientes elementos:

1. Descripción breve de la función, método o clase.
2. Nombre de los parámetros requeridos, su tipo y una breve descripción.
3. Tipo del objeto devuelto (_return_) y descripción.

### 3.5.4. Nomenclatura

Los nombres de objetos, funciones, métodos y clases **sólo podrán escribirse usando caracteres ASCII** (esto incluye el
uso de acentos y la letra "ñ"). **Los nombres deben ser en inglés**. En el caso excepcional de que sean en castellano,
se recomienda seguir las reglas de ortografía (es decir, acentuar correctamente y evitar la sustitución de `ñ`
por `ni`: `año -> anio`).

El programador, en la medida de lo posible, siempre debe priorizar el uso de **nombres completos y descriptivos de los
objetos**, propiedades, métodos y clases. Es decir, el programador debe evitar usar letras individuales,
abreviaciones o nombres ambiguos, siglas, y acrónimos ambiguos, así como la remoción de vocales. De igual forma, debe
evitarse también el empleo de la [notación húngara](https://en.wikipedia.org/wiki/Hungarian_notation).

El programador podrá hacer excepciones a lo anterior en los siguientes casos:

1. En el caso de funciones estadísticas donde hay un uso razonablemente común de letras (latinas y griegas) para
   designar algunos objetos. Por ejemplo, las medias tienden a denotarse `m` o `mu`, la desviación estándar `s`, el
   tamaño de muestra `n`, la probabilidad `p` o `pi`, etc.
2. En el caso de iteradores, se permitirá el uso de las letras `c`, `i`, `j`, `k`, `r`, `x`, `y`, `z`, siempre y cuando
   sea en un bloque de código reducido y no haya otros bloques de iteración anidados.
3. En el caso de las siglas, las reconocidas internacionalmente, por ejemplo: `url`, `dni`, `pin`.

#### 3.5.4.1. Nomenclatura por tipo de identificador

##### 3.5.4.1.1. Paquetes y módulos

Los nombres de paquetes y módulos de código siempre deben ser `UpperCamelCase`. Por
ejemplo: `DataIntAuth.Core.DataIntUser`.

##### 3.5.4.1.2. Clases

Los nombres de clases siempre deben ser `UpperCamelCase`. Por ejemplo: `DataIntUser`.

##### 3.5.4.1.3. Métodos y funciones

Los nombres de métodos y funciones siempre deben ser `lower_snake_case`, por ejemplo `DataIntUser.create_token()`.

##### 3.5.4.1.4. Variables y constantes globales

Los nombres de variables y constantes globales —incluidas las de ambiente (_environment_)— deben ser `UPPER_SNAKE_CASE`.

##### 3.5.4.1.5. Objetos privados

En idiomas de programación que no dispongan de una definición formal de objeto (propiedades, métodos, funciones, etc.)
privado, éstas se denotarán con un guion bajo como prefijo ( `_` ). Por ejemplo: `_propiedad_privada`.

##### 3.5.4.1.6. Parámetros

Los parámetros de funciones y constructores de clase se escribirán en `lower_snake_case`.

##### 3.5.4.1.7. Variables y constantes locales

Los nombres de variables y constantes locales se escribirán en `lower_snake_case`.

### 3.5.5. Uso de espacios en expresiones y declaraciones

Al menos que el lenguaje de programación asi lo requiera, deberá evitarse añadir espacios en blanco inmediatamente al
interior de paréntesis o llaves.

**Correcto** :white_check_mark:

```js
const my_formula = x_1 + x_2 * b_2 + x_3 * (b_3 + c);
```

**Incorrecto** :x:

```js
const my_formula = x_1 + x_2 * b_2 + x_3 * ( b_3 + c );
```

Al menos que el lenguaje de programación así lo requiera, deberá evitarse añadir espacios en blanco después de una coma
y antes de un paréntesis o llave de cierre.

**Correcto** :white_check_mark:

```js
var array = [1, 3, 3,];
```

**Incorrecto** :x:

```js
var array = [1, 3, 3, ];
```

Al menos que el lenguaje de programación así lo requiera, deberá evitarse añadir espacios en blanco inmediatamente antes
de comas.

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

Siempre deberá añadirse un espacio en blanco alrededor de operadores binarios (`<`, `>`, `!=`, etc.) y expresiones de
asignación (`=`, `<-`, `->`, `+=`, etc.).

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

# 4. Archivos de configuración

## 4.1. Python

### 4.1.1. Pylint

El archivo de configuración para pylint puede descargarse [aquí](./Config/.pylintrc).
