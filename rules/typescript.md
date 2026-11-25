# TypeScript rules

Scope: `TS-*`. React, Next.js and Vite projects: formatting, compiler and lint configuration, architecture, naming,
internationalization, secrets and quality gates.

| ID | Title | Level |
|---|---|---|
| [TS-STY-001](#ts-sty-001--format-with-the-shared-prettier-configuration) | Format with the shared Prettier configuration | MUST |
| [TS-STY-002](#ts-sty-002--import-through-the-alias-in-a-fixed-order) | Import through the `@/*` alias in a fixed order | MUST |
| [TS-CFG-001](#ts-cfg-001--compile-in-strict-mode-and-type-check-with-no-emit) | Compile in strict mode and type-check with no emit | MUST |
| [TS-LNT-001](#ts-lnt-001--lint-hooks-unused-variables-and-complexity-as-errors) | Lint hooks, unused variables and complexity as errors | MUST |
| [TS-TYP-001](#ts-typ-001--do-not-use-any-use-unknown-and-narrow) | Do not use `any`; use `unknown` and narrow | MUST |
| [TS-TYP-002](#ts-typ-002--declare-shared-types-in-types-and-keep-functions-out-of-them) | Declare shared types in `types/` and keep functions out of them | MUST |
| [TS-ARC-001](#ts-arc-001--separate-presentation-from-logic) | Separate presentation from logic | MUST |
| [TS-ARC-002](#ts-arc-002--keep-the-data-access-layer-thin-and-handle-errors-in-the-hook) | Keep the data-access layer thin and handle errors in the hook | SHOULD |
| [TS-NAM-001](#ts-nam-001--follow-the-naming-and-export-conventions) | Follow the naming and export conventions | MUST |
| [TS-INT-001](#ts-int-001--key-translations-by-namespace-and-update-every-locale) | Key translations by namespace and update every locale | MUST |
| [TS-SEC-001](#ts-sec-001--supply-secrets-and-environment-values-through-environment-variables) | Supply secrets and environment values through environment variables | MUST |
| [TS-SEC-002](#ts-sec-002--never-put-secrets-in-next_public_-variables) | Never put secrets in `NEXT_PUBLIC_*` variables | MUST |
| [TS-TST-001](#ts-tst-001--pass-the-quality-gates-before-opening-a-pull-request) | Pass the quality gates before opening a pull request | MUST |

### TS-STY-001 — Format with the shared Prettier configuration

- **Level:** MUST
- **Applies to:** all TypeScript and React repos
- **Enforced by:** `prettier --check`
- **Why:** one formatting style removes formatting noise from reviews. Frontends share the same options: 4-space indent, 120 columns, double quotes, ES5 trailing commas.
- **Source:** Shared frontend conventions.

Correct:
```json
{
    "printWidth": 120,
    "useTabs": false,
    "tabWidth": 4,
    "trailingComma": "es5",
    "singleQuote": false,
    "jsxSingleQuote": false,
    "quoteProps": "consistent",
    "bracketSpacing": true,
    "bracketSameLine": false,
    "arrowParens": "avoid"
}
```

Incorrect:
```json
{
    "printWidth": 80,
    "tabWidth": 2,
    "singleQuote": true
}
```

### TS-STY-002 — Import through the alias in a fixed order

- **Level:** MUST
- **Applies to:** all Next.js and React repos
- **Enforced by:** `prettier --check` with `@trivago/prettier-plugin-sort-imports`
- **Why:** a fixed order and a single `@/*` alias keep diffs small and avoid long relative paths. Order: `react`, `next/*`, third-party, `@/components`, `@/lib`, `@/context`, `@/app`, `@/config`, `@/public`, `@/types`, type imports, relative.
- **Source:** Shared frontend conventions.

Correct:
```json
{
    "plugins": ["@trivago/prettier-plugin-sort-imports"],
    "importOrder": [
        "^react",
        "^next/(.*)$",
        "<THIRD_PARTY_MODULES>",
        "^@/components/(.*)$",
        "^@/lib/(.*)$",
        "^@/context/(.*)$",
        "^@/app/(.*)$",
        "^@/config/(.*)$",
        "^@/public/(.*)$",
        "^@/types/(.*)$",
        "TS_TYPES",
        "^[./]"
    ],
    "importOrderSeparation": false,
    "importOrderSortSpecifiers": true
}
```

Incorrect:
```typescript
import { formatDate } from "../../../lib/dates/format";
import { useState } from "react";
```

### TS-CFG-001 — Compile in strict mode and type-check with no emit

- **Level:** MUST
- **Applies to:** all TypeScript repos
- **Enforced by:** `tsc --noEmit`
- **Why:** strict mode is the baseline for type safety. Do not weaken types to make code compile. The `@/*` alias is declared in `paths`.
- **Source:** Shared frontend conventions.

Correct:
```json
{
    "compilerOptions": {
        "strict": true,
        "noEmit": true,
        "skipLibCheck": true,
        "isolatedModules": true,
        "moduleResolution": "bundler",
        "paths": {
            "@/*": ["./*"]
        }
    }
}
```

Incorrect:
```json
{
    "compilerOptions": {
        "strict": false,
        "noImplicitAny": false
    }
}
```

### TS-LNT-001 — Lint hooks, unused variables and complexity as errors

- **Level:** MUST
- **Applies to:** all TypeScript and React repos
- **Enforced by:** `eslint`
- **Why:** hook mistakes, dead code and complex functions are the most common review findings. Extend the recommended ESLint and `typescript-eslint` sets, turn the base `no-unused-vars` off in favor of the TypeScript one, and limit cyclomatic complexity to 10.
- **Source:** Shared frontend conventions.

Correct:
```javascript
import js from "@eslint/js";
import reactHooks from "eslint-plugin-react-hooks";
import { defineConfig } from "eslint/config";
import ts from "typescript-eslint";

export default defineConfig(
    { ignores: ["**/node_modules/", ".next/"] },
    js.configs.recommended,
    ts.configs.recommended,
    reactHooks.configs.flat.recommended,
    {
        rules: {
            "react-hooks/exhaustive-deps": "error",
            "react-hooks/rules-of-hooks": "error",
            "no-unused-vars": "off",
            "@typescript-eslint/no-unused-vars": "error",
            complexity: ["error", 10],
        },
    }
);
```

Incorrect:
```javascript
export default [
    {
        rules: {
            "react-hooks/exhaustive-deps": "off",
            complexity: "off",
        },
    },
];
```

### TS-TYP-001 — Do not use `any`; use `unknown` and narrow

- **Level:** MUST
- **Applies to:** all TypeScript repos
- **Enforced by:** code review
- **Why:** `any` disables type checking at module boundaries such as API responses. Use `unknown` and narrow before use. A third-party untyped value is the only exception and is justified in the pull request.
- **Source:** Shared frontend conventions.

Correct:
```typescript
const parseCount = (value: unknown): number => {
    if (typeof value === "number") {
        return value;
    }
    return 0;
};
```

Incorrect:
```typescript
const parseCount = (value: any): number => {
    return value.count;
};
```

### TS-TYP-002 — Declare shared types in `types/` and keep functions out of them

- **Level:** MUST
- **Applies to:** Next.js and React repos
- **Enforced by:** code review
- **Why:** files under `types/` only declare `interface`, `type` and `enum`. Type guards and helpers go to `lib/`. Hook files do not declare inline types.
- **Source:** Shared frontend conventions.

Correct:
```typescript
export interface Contact {
    id: string;
    name: string;
}
```

```typescript
import type { Contact } from "@/types/contacts";

export const isContact = (value: unknown): value is Contact => {
    return typeof value === "object" && value !== null && "id" in value;
};
```

Incorrect:
```typescript
export interface Contact {
    id: string;
}

export const isContact = (value: unknown): value is Contact => {
    return typeof value === "object" && value !== null;
};
```

### TS-ARC-001 — Separate presentation from logic

- **Level:** MUST
- **Applies to:** Next.js and React repos
- **Enforced by:** code review
- **Why:** each file has a single responsibility. A hook file (`use*.ts`) declares only the hook; complex logic goes to a sibling file. A component file (`*.tsx`) renders UI and imports mapping constants and logic from `lib/` and `config/`. Sub-components get their own files. Prefer derived state with `useMemo` over an effect that sets state.
- **Source:** Shared frontend conventions.

Correct:
```typescript
import useSWR from "swr";

import { fetchConversations } from "./fetchConversations";

export const useConversations = () => useSWR("conversations", fetchConversations);
```

Incorrect:
```typescript
import useSWR from "swr";

const parseResponse = (data: unknown) => data;

export const useConversations = () => useSWR("conversations", () => parseResponse([]));
```

### TS-ARC-002 — Keep the data-access layer thin and handle errors in the hook

- **Level:** SHOULD
- **Applies to:** Next.js and React repos that fetch data
- **Enforced by:** code review
- **Why:** API client methods return the response unchanged, with no `try/catch` and no reshaping. The consumer hook builds the SWR fetcher with `useCallback` and handles the error state, so components and hooks do not change when the backend does.
- **Source:** Shared frontend conventions.

Correct:
```typescript
async getCitySummary(cityId: string) {
    return this.client.get<CitySummary>(`/v1/city-summary/${cityId}`);
}
```

Incorrect:
```typescript
async getCitySummary(cityId: string) {
    try {
        const response = await this.client.get<CitySummary>(`/v1/city-summary/${cityId}`);
        return { data: response.data, error: null };
    } catch (error) {
        return { data: null, error };
    }
}
```

### TS-NAM-001 — Follow the naming and export conventions

- **Level:** MUST
- **Applies to:** Next.js and React repos
- **Enforced by:** code review
- **Why:** consistent names make files predictable. Variables and functions use camelCase; components and types use PascalCase; files and directories use kebab-case; a hook file is named after its hook. Components and hooks use named exports; Next.js pages use `export default`.
- **Source:** Shared frontend conventions.

Correct:
```typescript
export const RouteCard = ({ route }: RouteCardProps) => {
    return <li>{route.name}</li>;
};
```

Incorrect:
```typescript
export default function route_card({ route }: any) {
    return <li>{route.name}</li>;
}
```

### TS-INT-001 — Key translations by namespace and update every locale

- **Level:** MUST
- **Applies to:** Next.js and React repos with internationalization
- **Enforced by:** code review
- **Why:** the translation namespace equals the locale file path, and the active language is passed to the translation hook from the route or the language context. A new key is added to every supported locale in the same change, so no language falls back to a missing string.
- **Source:** Shared frontend conventions.

Correct:
```typescript
const { t } = useClientTranslation(language, "reports/summary");
```

Incorrect:
```typescript
const { t } = useClientTranslation("en", "summary");
```

### TS-SEC-001 — Supply secrets and environment values through environment variables

- **Level:** MUST
- **Applies to:** all frontend repos
- **Enforced by:** code review; secret scanning
- **Why:** never commit secrets, tokens or credentials, never hardcode environment-specific values, and never log tokens, cookies or authorization headers. Values reach the code through environment variables read in the configuration layer. A committed secret is treated as compromised and rotated.
- **Source:** Shared frontend conventions.

Correct:
```typescript
const apiBaseUrl = process.env.API_BASE_URL;

export default { apiBaseUrl };
```

Incorrect:
```typescript
const apiKey = "example-secret";
const apiBaseUrl = "https://api.example.com";

console.log("token", apiKey);
```

### TS-SEC-002 — Never put secrets in `NEXT_PUBLIC_*` variables

- **Level:** MUST
- **Applies to:** Next.js repos
- **Enforced by:** code review; secret scanning
- **Why:** Next.js inlines every `NEXT_PUBLIC_*` value into the JavaScript sent to the browser, so anyone can read it. Only values that are public by design use that prefix, such as base URLs or browser keys restricted by origin. A key that must stay private is read on the server without the prefix, and the browser calls a route handler.
- **Source:** Shared frontend conventions.

Correct:
```typescript
export const GET = async () => {
    const response = await fetch("https://api.example.com/v1/items", {
        headers: { Authorization: `Bearer ${process.env.ITEMS_API_KEY}` },
    });
    return Response.json(await response.json());
};
```

Incorrect:
```typescript
const response = await fetch("https://api.example.com/v1/items", {
    headers: { Authorization: `Bearer ${process.env.NEXT_PUBLIC_ITEMS_API_KEY}` },
});
```

### TS-TST-001 — Pass the quality gates before opening a pull request

- **Level:** MUST
- **Applies to:** all TypeScript and React repos
- **Enforced by:** CI (`CI-PIP-001`)
- **Why:** the same checks run locally and in CI: type check, lint, format check, tests and build. A pull request that fails one of them is not reviewed.
- **Source:** Shared frontend conventions.

Correct:
```bash
tsc --noEmit
bun run lint
bun run format:check
bun run test
bun run build
```

Incorrect:
```bash
bun run build
```
