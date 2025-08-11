# Diagnóstico de la Guía de Estilo de DataInt

_Fecha: 2025-08-11_

## 1) Inventario completo (estructura vigente)

- **1. Introducción**
- **2. Guías auxiliares**
  - 2.1. Listado de guías auxiliares (Google styleguides, PEP8, etc.)
- **3. Lineamientos generales**
  - 3.1. Estructura de proyecto
  - 3.2. Flujo de trabajo con sistema de control de versiones
    - 3.2.1. Nomenclatura (ramas)
    - 3.2.2. Convención de versionado (CalVer)
  - 3.3. Archivos de código fuente
    - 3.3.1. Codificación (UTF-8)
    - 3.3.2. Nombre (lowercase, , `_`)
    - 3.3.3. Estructura (orden de imports)
    - 3.3.4. Final de archivo (newline)
  - 3.4. Disposición del código
    - 3.4.1. Longitud máxima de línea (120)
    - 3.4.2. Tamaño/estructura de clases
    - 3.4.3. Líneas en blanco
    - 3.4.4. Indentación (4 espacios)
  - 3.5. Estilo de código
    - 3.5.1. Caracteres no ASCII
    - 3.5.2. Caracteres especiales
    - 3.5.3. Comentarios y docstring
      - 3.5.3.1. Comentarios (inglés)
      - 3.5.3.2. Docstrings (solo librerías)
    - 3.5.4. Nomenclatura
      - 3.5.4.1. Por identificador
        - Paquetes/módulos: UpperCamelCase
        - Clases: UpperCamelCase
        - Métodos/funciones: `lower_snake_case`
        - Globales: `UPPER_SNAKE_CASE`
        - Privados: `_prefijo`
        - Parámetros: `lower_snake_case`
        - Locales: `lower_snake_case`
    - 3.5.5. Espacios en expresiones
- **4. Archivos de configuración**
  - 4.1. Python → 4.1.1. Pylint

---

## 2) Evaluación de calidad por sección

| Sección                     | Estado        | Justificación breve                                                                             |
| --------------------------- | ------------- | ----------------------------------------------------------------------------------------------- |
| 1. Introducción             | **Clara**     | Objetivo bien definido; falta anclar al stack actual (React/Next/TS/Tailwind).                  |
| 2. Guías auxiliares         | **Ambigua**   | Remite a Google/PEP8 pero no prioriza para JS/TS; mezcla lenguajes.                             |
| 3.1 Estructura de proyecto  | **Ambigua**   | Genérica; faltan pautas de monorepo/app dir, alias TS, colocation, tests.                       |
| 3.2 Git workflow            | **Obsoleta**  | Usa `master/dev` y GitFlow pesado; hoy `main` + trunk-based/PRs es estándar.                    |
| 3.2.1 Nomenclatura ramas    | **Ambigua**   | Bien los prefijos; falta alinear con issues/Conventional Commits.                               |
| 3.2.2 Versionado            | **Ambigua**   | CalVer ok; ejemplos mezclan `v` prefijo y patrón; no cubre tags/CI.                             |
| 3.3 Source files            | **Ambigua**   | Orden de imports orientado a Python; falta regla para `import type`, `@/` alias.                |
| 3.3.2 Nombre de archivos    | **Obsoleta**  | Pide lowercase/kebab/underscore universal; en React los componentes van `PascalCase.tsx`.       |
| 3.4 Layout (líneas, indent) | **Ambigua**   | 120 chars ok; indent 4 espacios **alineado a tu Prettier**.                                     |
| 3.4.2 Tamaño de clases      | **No aplica** | En front moderno predominan funciones/hooks; métrica por “clase” no guía.                       |
| 3.5.1–3.5.3 Comentarios     | **Clara**     | Inglés y criterio razonable; falta TSDoc/JSDoc para lib/hooks.                                  |
| 3.5.4 Nomenclatura          | **Obsoleta**  | Snake_case para funciones/variables choca con camelCase/pascalCase de JS/TS/React.              |
| 3.5.5 Espacios              | **Ambigua**   | Ejemplos favorecen trailing comma en línea única; en tu Prettier (`es5`) se usan en multilínea. |
| 4. Config (Pylint)          | **Obsoleta**  | Solo Python; falta ESLint/Prettier/tailwind plugin/.                                            |

---

## 3) Mapa de brechas vs. _Clean Code_

- **Nomenclatura:** Falta alinear a camelCase (vars/funciones), PascalCase (Componentes/Tipos), kebab-case (rutas/archivos), SCREAMING_SNAKE_CASE (constantes).
- **Funciones pequeñas / SRP:** No hay guías para tamaño de funciones/hooks, separación de efectos y render, ni límites de props.
- **Dependencias:** No define import layering, alias `@/`, barriles (`index.ts`), ni control de side-effects.
- **Comentarios/documentación:** Carece de TSDoc/JSDoc mínima para APIs/hooks/utilidades.
- **Organización de módulos:** No hay pautas para Next.js app dir, colocation, i18n keys, assets, ni estructura de features.
- **Automatización:** Falta estandarizar Prettier + ESLint + pre-commit hooks.
- **Accesibilidad:** Sin reglas a11y.
- **TailwindCSS:** Sin guía de orden de utilidades, tokens y variantes.
- **Testing/QA:** No hay estándar documentado para QA manual actual ni plan para evolución a tests automáticos.

---

## 4) Reglas obsoletas o difíciles en React/Next/TS/Tailwind

- Snake_case para funciones/variables → incompatible con JS/TS (usar camelCase).
- UpperCamelCase para módulos → incompatible con archivos front (excepto componentes).
- Tamaño de clases → irrelevante para funciones/componentes.
- Solo Pylint → falta ESLint/Prettier con plugins.
- GitFlow con master/dev → migrar a main + PRs cortos.

---

## 5) Ejemplos concretos

**1. Funciones JS/TS**

Antes: `function get_user_data() {}`

Después: `function getUserData() {}`

**2. Componentes React**

Antes: `components/user_card.tsx`

Después: `components/UserCard.tsx`

**3. Variables locales**

Antes: `const user_name = "Ana";`

Después: `const userName = "Ana";`

**4. Indentación (Prettier 4 espacios)**

```tsx
if (isLoading) {
  return <Spinner />;
}
```

**5. Imports con alias**

Antes:

```tsx
import Button from "../../components/button";
```

Después:

```tsx
import { Button } from "@/components/ui/button";
```

---

## 6) Recomendaciones accionables

### Quick wins

- Mantener tu configuración Prettier (4 espacios, printWidth 120, trailingComma "es5").
- Prettier plugin TailwindCSS (opcional, añadir al final del array de plugins).
- ESLint con `@typescript-eslint`, `react`, `jsx-a11y`, `import`, `tailwindcss`.
- camelCase (vars/funciones), PascalCase (componentes/tipos), SCREAMING_SNAKE_CASE (constantes).
- Archivos: PascalCase para componentes, kebab-case para utilidades/hooks.
- Migrar a `main`, mantener prefijos de rama y Conventional Commits.
- Orden y alias en imports; `import type` separado.
- Comentarios en inglés; TSDoc mínima para hooks/libs.

### Cambios estructurales

- Dividir por lenguaje (Frontend vs. Python).
- Guías Next.js (app dir, colocation, imports).
- Tailwind (orden clases, tokens, dark mode).
- Accesibilidad (focus, aria, contraste).
- Documentar control de calidad manual en QA (checklist PR).
- Evolución futura a tests automáticos como complemento.

---

## 7) Control de calidad manual (QA)

**Objetivo**

- Validar funcional, visual y accesible en QA antes de release.

**Checklist por PR**

- [ ] Escenarios críticos (happy/sad paths).
- [ ] i18n correcto (ES/EN), sin hardcode.
- [ ] Responsivo en 360, 768, 1024, 1280px.
- [ ] A11y básico (focus visible, aria-\*).
- [ ] Dark mode (si aplica).
- [ ] Estados de carga, error y vacío.
- [ ] Orden de imports y estilo pasan Prettier.
- [ ] Sin regresiones en mapas, selects, formularios y toasts.
- [ ] Performance perceptual OK.

---

## 8) Plan de actualización

1. Nueva sección Frontend (React/Next/TS/Tailwind).
2. Actualizar Git workflow (`main`, PRs cortos).
3. Toolchain ESLint/Prettier + husky.
4. Guías de arquitectura (app dir, imports).
5. Anexos por lenguaje.
6. Incluir sección QA manual con checklist.

---

## 9) Checklist de aceptación

- [x] Inventario completo
- [x] Evaluación de calidad
- [x] Mapa de brechas
- [x] Reglas obsoletas
- [x] Ejemplos antes/después
- [x] Recomendaciones (≤1 página)
- [x] Publicación en rama nueva
- [x] Inclusión de prácticas QA manual
