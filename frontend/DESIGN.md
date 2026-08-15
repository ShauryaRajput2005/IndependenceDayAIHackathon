# KAIROS Design System

## Design Read
> **Reading this as:** An editorial, premium creator tool for content strategists, with a highly restrained, tactile, and human visual language, leaning toward independent publishing interfaces and Apple-level restraint.

**Dial Configuration:**
- `DESIGN_VARIANCE: 6` (Editorial layout, deliberate asymmetry, highly functional but art-directed)
- `MOTION_INTENSITY: 5` (Fluid, physical micro-interactions, no constant chaotic movement)
- `VISUAL_DENSITY: 3` (Generous whitespace, letting generated content breathe)

## Design Principles
1. **KAIROS brand identity first.**
2. **Taste Skill guidelines:** Avoid generic AI slop, center human-centric design.
3. **Impeccable principles:** Refined typography, rigorous spacing, high-end finishing.
4. **Accessibility/usability:** Maintain contrast, semantic HTML, accessible interactions.
5. **Selective motion:** Use React Bits only for deliberate interaction feedback.

## Color Philosophy
KAIROS feels warm, tactile, and editorial. We strictly avoid the cold "AI palette".
- **80% Neutral** (`#F4F1EA` / `#FAF9F5`)
- **15% Supporting/Muted** (`#171717` / `#69665F` / `#D9D5CC`)
- **5% Accent** (`#D94F2B`)

*The interface must look exceptional even if the accent color is removed. Accent is reserved strictly for primary CTAs, active states, important highlights, viral score, and feedback confirmation.*

## Typography
A deliberate editorial type system:
- **Display:** `Instrument Serif` (Used for personality, big statements, and hooks).
- **Interface:** `Inter` (Used for usability, data, forms, and small UI text).

*Do NOT use the serif everywhere. Mix them purposefully. Copy should feel human and confident.*

## Spacing & Grid
- **Scale:** Base-4 scale (`4`, `8`, `12`, `16`, `24`, `32`, `48`, `64`, `96`, `128`).
- **Whitespace:** Generous. Do not fill every available area.
- **Grid:** 12-column editorial grid on desktop.
- **Layouts:** Allow asymmetry, strong alignment, negative space, large typography, full-width moments, and deliberate visual imbalance. Do not force every section into symmetrical card grids.

## UI Elements
### Radius
Restrained and deliberate:
- Small: `6px`
- Medium: `8px`
- Large: `12px`
*Do not make every element a huge rounded rectangle. Pills are reserved for tags, statuses, categories, and metadata.*

### Borders & Shadows
- **Primary Border:** `#D9D5CC`. Prefer subtle borders over shadows. Do not create heavy boxed interfaces.
- **Shadows:** Default is **No shadow**. Use very subtle elevation only where absolutely necessary. Avoid large soft SaaS shadows.

### Buttons
- **Primary:** Dark ink (`#171717`) or KAIROS accent (`#D94F2B`).
- **Secondary:** Neutral bordered.
- **Tertiary:** Text action.
*Avoid gradient buttons, glowing buttons, giant pills, or oversized CTA buttons.*

### Inputs & Forms
The product form should feel like a creative brief, not a configuration dashboard.
"Tell KAIROS about the thing."
Hierarchy: Product → Audience → Problem → Platform → Tone → Creative direction.
*Custom requirements should be visually important and feel conversational.*

## Content Surfaces
- **Meme Surfaces:** Should comfortably mix GIFs, images, dialogue, and scripts. Do not sanitize internet culture into corporate UI.
- **Viral Score:** Do not make it look like a generic SaaS KPI. No neon gauges, giant circular charts, or fake precision. Present it as e.g., `87 / 100 — STRONG POTENTIAL` with a concise explanation.

## Motion
Motion communicates transformation, progress, hierarchy, and feedback.
- Must be: Subtle, fast, purposeful, consistent.
- Respect `prefers-reduced-motion`.
- **React Bits:** Good candidates include text reveal, animated content list, small interaction feedback, button micro-interactions, result reveal.
- **Avoid:** Aurora backgrounds, plasma, ballpit, particle-heavy backgrounds, constant floating elements.

## Accessibility
- Strong contrast
- Semantic HTML
- Visible focus states
- Keyboard navigation
- Accessible labels
- Appropriate text sizes

## Responsive Behavior
- **Primary target:** Desktop.
- **Support:** 1440px, 1280px, 1024px, Mobile.
- **On mobile:** Reconsider hierarchy, collapse columns, preserve whitespace, preserve readable typography. Do not blindly stack every desktop element.

## Anti-AI-Slop Rules (DO NOT USE)
- Purple/blue-purple AI gradients
- Neon cyan, rainbow gradients
- Glowing borders, giant gradient text
- Glassmorphism, aurora backgrounds, floating blobs
- AI brain graphics, robot illustrations, generic sparkle icons
- Excessive "magic" effects
- Excessive rounded cards / everything inside cards
- Generic SaaS dashboards, fake analytics
- Excessive pills, excessive shadows
