# HTML and CSS rules

Scope: `CSS-*`. HTML and CSS conventions.

| ID | Title | Level |
|---|---|---|
| [CSS-STY-001](#css-sty-001--use-utility-classes-and-theme-tokens-instead-of-loose-colors-and-sizes) | Use utility classes and theme tokens instead of loose colors and sizes | SHOULD |
| [CSS-ACC-001](#css-acc-001--use-button-and-a-for-interactive-elements) | Use `button` and `a` for interactive elements | MUST |
| [CSS-ACC-002](#css-acc-002--give-icon-only-buttons-an-accessible-name-and-images-an-alt-text) | Give icon-only buttons an accessible name and images an `alt` text | MUST |
| [CSS-ACC-003](#css-acc-003--replace-a-removed-outline-with-a-focus-visible-style) | Replace a removed outline with a `focus-visible` style | MUST |

### CSS-STY-001 — Use utility classes and theme tokens instead of loose colors and sizes

- **Level:** SHOULD
- **Applies to:** frontends styled with utility classes (for example Tailwind)
- **Enforced by:** code review
- **Why:** colors and measures defined as theme tokens change in one place and keep the interface consistent, including in dark mode. Literal values scattered in markup drift apart.
- **Source:** Shared frontend conventions.

Correct:
```tsx
<div className="bg-surface text-foreground p-4 rounded-md" />
```

Incorrect:
```tsx
<div style={{ backgroundColor: "#1a1a2e", color: "#eeeeee", padding: "13px" }} />
```

### CSS-ACC-001 — Use `button` and `a` for interactive elements

- **Level:** MUST
- **Applies to:** all frontends
- **Enforced by:** `eslint-plugin-jsx-a11y`; code review
- **Why:** `button` and `a` provide keyboard focus, activation with `Enter` and `Space`, and the correct role for assistive technology. A `div` with `onClick` provides none of them.
- **Source:** WCAG 2.2, success criterion 4.1.2.

Correct:
```tsx
<button type="button" onClick={handleSave}>
    Save
</button>
<a href="/settings">Settings</a>
```

Incorrect:
```tsx
<div onClick={handleSave}>Save</div>
```

### CSS-ACC-002 — Give icon-only buttons an accessible name and images an `alt` text

- **Level:** MUST
- **Applies to:** all frontends
- **Enforced by:** `eslint-plugin-jsx-a11y`; code review
- **Why:** a button with only an icon has no name for a screen reader, and an image without `alt` is announced by its file name. Decorative images use an empty `alt`.
- **Source:** WCAG 2.2, success criteria 1.1.1 and 4.1.2.

Correct:
```tsx
<button type="button" aria-label="Close dialog" onClick={handleClose}>
    <CloseIcon aria-hidden="true" />
</button>
<img src="/chart.png" alt="Monthly usage chart" />
```

Incorrect:
```tsx
<button type="button" onClick={handleClose}>
    <CloseIcon />
</button>
<img src="/chart.png" />
```

### CSS-ACC-003 — Replace a removed outline with a `focus-visible` style

- **Level:** MUST
- **Applies to:** all frontends
- **Enforced by:** code review; keyboard navigation check
- **Why:** the focus outline tells keyboard users where they are. Removing it without a replacement leaves them without a position.
- **Source:** WCAG 2.2, success criterion 2.4.7.

Correct:
```css
button:focus {
    outline: none;
}

button:focus-visible {
    outline: 2px solid var(--color-focus);
    outline-offset: 2px;
}
```

Incorrect:
```css
button:focus {
    outline: none;
}
```
