# Design System Inspired by Duolingo

## 1. Visual Theme & Atmosphere

The Duolingo design system embodies a playful yet focused learning experience. It combines vibrant, energetic green tones with calming neutral backgrounds to create an approachable and motivating interface. The visual language is modern and friendly, leveraging rounded corners, generous spacing, and accessible typography to make language learning feel fun rather than intimidating. The palette emphasizes clarity and joy, with strategic use of bright accent colors to guide users toward key actions. The overall mood is optimistic, inclusive, and designed to reduce friction in the learning journey.

**Key Characteristics**

- Bright, energetic green as the primary brand color symbolizing growth and achievement
- Rounded, soft edges throughout components creating a friendly, approachable feel
- Generous whitespace and breathing room between elements
- Clear hierarchy using weight and size contrasts rather than color alone
- Playful yet professional balance suitable for diverse age groups
- Emphasis on positive reinforcement through visual feedback and interactive elements

## 2. Color Palette & Roles

### Primary
- **Brand Green** (`#1CB0F6`): Primary action buttons, key CTAs, brand identity, and interactive highlights. This is the dominant color signaling "go" and "learn."
- **Duolingo Lime** (`#00B086`): Secondary accent for supporting elements, badges, and supporting visual indicators. Used sparingly for visual variety.

### Interactive
- **Link Blue** (`#0000EE`): Standard hyperlinks and text links. Maintains web accessibility conventions for clickable text.

### Neutral Scale
- **Charcoal** (`#3C3C3C`): Primary text color for body copy, headings, and navigation. Provides high contrast for readability.
- **White** (`#FFFFFF`): Text on colored backgrounds, primary background for input fields and content areas.

### Surface & Borders
- **Light Border** (`#C1C1C1`): Input field borders and subtle dividers. Provides definition without visual weight.
- **Off-White Background** (`#F5F5F5`): Secondary background surfaces and hover states. Inferred for subtle contrast.

## 3. Typography Rules

### Font Family
- **Primary Font**: DIN Round Pro (`din-round`) with fallback stack: `din-round, 'Trebuchet MS', Helvetica, Arial, sans-serif`
- **Secondary Font**: Feather (`feather`) with fallback stack: `feather, 'Georgia', serif`

### Hierarchy

| Role | Font | Size | Weight | Line Height | Letter Spacing | Notes |
|------|------|------|--------|-------------|----------------|-------|
| Display / H1 | feather | 48px | 700 | normal | normal | Page titles and hero headings |
| Heading 1 | din-round | 32px | 700 | normal | normal | Major section headings |
| Heading 2 | din-round | 24px | 700 | 1.2 | normal | Subheadings and card titles |
| Body | din-round | 17px | 500 | 24px | normal | Primary content and descriptions |
| Button / Label | din-round | 15px | 700 | normal | normal | CTA buttons, labels, and emphasis |
| Caption / Small | din-round | 14px | 500 | 1.4 | normal | Secondary text and metadata |
| Code / Monospace | din-round | 13px | 400 | 1.5 | normal | Technical content if applicable |

### Principles
- Use DIN Round as the default, modern, and approachable primary typeface for all UI elements.
- Reserve Feather for dramatic display moments such as hero sections and campaign headlines.
- Maintain 24px line height for body text to ensure readability and accessibility at 17px size.
- Use weight 700 for all interactive elements (buttons, links, labels) to signify interactivity.
- Keep letter spacing normal (0) to maintain brand consistency and natural flow.
- Scale heading sizes in logical increments to maintain visual hierarchy clarity.

## 4. Component Stylings

### Buttons

**Primary Button (CTA)**
- Background: `#1CB0F6`
- Text Color: `#FFFFFF`
- Font: din-round, 15px, weight 700
- Padding: `0px 16px`
- Height: `50px`
- Width: `330px` (full-width on mobile, auto on desktop)
- Border Radius: `12px`
- Border: `none`
- Box Shadow: `none`
- Hover State: Background `#1A95D1` (darken 10%), cursor pointer
- Active State: Background `#158AC1`, scale `0.98`
- Disabled State: Background `#CCCCCC`, text color `#999999`, cursor not-allowed

**Secondary Button**
- Background: `transparent`
- Text Color: `#1CB0F6`
- Font: din-round, 15px, weight 700
- Padding: `0px 16px`
- Height: `50px`
- Width: `auto`
- Border Radius: `12px`
- Border: `2px solid #1CB0F6`
- Box Shadow: `none`
- Hover State: Background `rgba(28, 176, 246, 0.1)`, border color `#1A95D1`
- Active State: Background `rgba(28, 176, 246, 0.2)`

**Ghost Button**
- Background: `transparent`
- Text Color: `#3C3C3C`
- Font: din-round, 15px, weight 700
- Padding: `0px 16px`
- Height: `50px`
- Width: `auto`
- Border Radius: `12px`
- Border: `none`
- Box Shadow: `none`
- Hover State: Background `rgba(0, 0, 0, 0.05)`

### Cards & Containers

**Content Card**
- Background: `#FFFFFF`
- Border: `1px solid #E0E0E0`
- Border Radius: `12px`
- Padding: `24px`
- Box Shadow: `0px 2px 8px rgba(0, 0, 0, 0.08)`
- Hover State: Box Shadow `0px 4px 12px rgba(0, 0, 0, 0.12)`

**Achievement Card**
- Background: `linear-gradient(135deg, #FFE082 0%, #FFC107 100%)`
- Border: `none`
- Border Radius: `12px`
- Padding: `20px`
- Box Shadow: `0px 4px 12px rgba(255, 193, 7, 0.3)`
- Text Color: `#3C3C3C`

### Inputs & Forms

**Text Input**
- Background: `#FFFFFF`
- Border: `1px solid #C1C1C1`
- Border Radius: `8px`
- Padding: `12px 16px`
- Font: din-round, 17px, weight 400
- Text Color: `#000000`
- Height: `40px`
- Box Shadow: `none`
- Focus State: Border color `#1CB0F6`, box shadow `0px 0px 0px 3px rgba(28, 176, 246, 0.1)`
- Placeholder Color: `#999999`

**Form Label**
- Font: din-round, 15px, weight 700
- Text Color: `#3C3C3C`
- Margin Bottom: `8px`
- Display: `block`

**Form Error State**
- Border Color: `#E53935`
- Text Color: `#E53935`
- Font: din-round, 13px, weight 500
- Margin Top: `4px`

### Navigation

**Top Navigation Bar**
- Background: `#FFFFFF`
- Height: `70px`
- Border Bottom: `1px solid #EEEEEE`
- Padding: `0px 24px`
- Display: `flex`
- Align Items: `center`

**Navigation Link**
- Font: din-round, 17px, weight 500
- Text Color: `#3C3C3C`
- Line Height: `20px`
- Padding: `8px 16px`
- Border Radius: `8px`
- Hover State: Background `rgba(0, 0, 0, 0.05)`, text color `#1CB0F6`
- Active State: Text color `#1CB0F6`, border bottom `3px solid #1CB0F6`

### Links

**Text Link (Default)**
- Font: din-round, 17px, weight 500
- Text Color: `#0000EE`
- Background: `transparent`
- Text Decoration: `underline`
- Hover State: Text color `#1CB0F6`, text decoration `underline`
- Active State: Text color `#0000CC`

**Button Link (Inverted)**
- Font: din-round, 15px, weight 700
- Text Color: `#FFFFFF`
- Background: `#1CB0F6`
- Padding: `12px 20px`
- Border Radius: `12px`
- Height: `44px`
- Hover State: Background `#1A95D1`

### Badges

**Achievement Badge**
- Background: `#00B086`
- Text Color: `#FFFFFF`
- Font: din-round, 12px, weight 700
- Padding: `4px 8px`
- Border Radius: `2px`
- Display: `inline-block`

**Progress Badge**
- Background: `#1CB0F6`
- Text Color: `#FFFFFF`
- Font: din-round, 12px, weight 700
- Padding: `4px 8px`
- Border Radius: `2px`

## 5. Layout Principles

### Spacing System
- **Base Unit**: `8px`
- **Scale**: `8px`, `12px`, `16px`, `24px`, `32px`, `40px`, `48px`, `64px`, `72px`, `80px`, `96px`, `100px`
- **Usage Context**:
  - `8px` – Micro spacing within components (icon-to-text gaps)
  - `12px` – Internal component padding, tight grouping
  - `16px` – Standard button padding, form field padding
  - `24px` – Card padding, section gaps, navigation items
  - `32px` – Medium section spacing, sidebar gutters
  - `40px` – Top/bottom margins for key sections
  - `48px` – Section containers, medium hero spacing
  - `64px` – Large section separation
  - `72px` – Hero section padding vertical
  - `80px` – Feature section gaps
  - `96px` – Major layout dividers
  - `100px` – Full page margin for ultra-wide screens

### Grid & Container
- **Max Width**: `1200px` for desktop layouts
- **Column Strategy**: 12-column grid system with `24px` gutter width
- **Container Padding**: `48px` horizontal on desktop, `24px` on tablet, `16px` on mobile
- **Section Pattern**: Full-width sections with inner containers centered at max-width

### Whitespace Philosophy
Duolingo's design prioritizes breathing room and clarity. Generous whitespace reduces cognitive load and creates visual rest areas. Each section is clearly separated by at least `64px` vertical spacing on desktop. Micro-interactions and animations use whitespace to guide focus without clutter. Touch targets maintain `50px` minimum height with `16px` horizontal padding to ensure comfortable interaction.

### Border Radius Scale
- `2px` – Badges, small indicators, minimal rounding
- `8px` – Form inputs, subtle containers
- `12px` – Buttons, cards, primary interactive elements
- `16px` – Modal containers, large cards
- `24px` – Hero containers, featured sections
- `50%` – Circular profile images, avatar containers

## 6. Depth & Elevation

| Level | Treatment | Use |
|-------|-----------|-----|
| Ground (0) | No shadow | Flat backgrounds, base surface |
| Raised (1) | `0px 2px 8px rgba(0, 0, 0, 0.08)` | Standard cards, subtle elevation |
| Floating (2) | `0px 4px 12px rgba(0, 0, 0, 0.12)` | Hovering cards, dropdown menus |
| Modal (3) | `0px 8px 24px rgba(0, 0, 0, 0.15)` | Modals, overlays, prominent containers |
| Overlay (4) | `0px 12px 32px rgba(0, 0, 0, 0.2)` | Full-screen overlays, critical focus |

Duolingo uses minimal shadow treatment to maintain a flat, modern aesthetic while providing subtle depth cues for interactive states. Shadows increase gradually as elements move forward in the z-axis, creating a cohesive depth system. Shadows are always soft and use low-opacity black to avoid harsh contrasts. On achievement or celebratory elements, warmer shadows (gold/yellow tints) may replace neutral shadows to reinforce positive emotions.

## 7. Do's and Don'ts

### Do
- Use `#1CB0F6` for all primary CTAs and the most important user actions.
- Maintain `50px` minimum height for all interactive elements (buttons, input fields).
- Apply `12px` border radius to all buttons and card components for consistency.
- Pair `#3C3C3C` text with `#FFFFFF` backgrounds for optimal readability (WCAG AA compliant).
- Use DIN Round for all UI text; reserve Feather for headline campaigns only.
- Group related elements with `24px` spacing; separate sections with `64px` or more.
- Include hover and active states on all interactive elements with clear visual feedback.
- Use a maximum of three colors in any single component (background, text, accent).
- Scale typography consistently using the defined hierarchy table.
- Test buttons and inputs on mobile with a `44px` minimum touch target (iOS guideline).

### Don't
- Don't use `#0000EE` for primary actions; reserve it for standard text links only.
- Don't apply shadows to flat background elements or override the defined elevation system.
- Don't mix DIN Round and Feather fonts within the same component or section.
- Don't set line height to `normal` for body copy; always use at least `1.4` multiplier.
- Don't reduce button padding below `12px` horizontally or height below `44px` on mobile.
- Don't use more than two font weights (500 and 700) in the default palette.
- Don't apply border radius values outside the defined scale (e.g., `10px` or `15px`).
- Don't use white text (`#FFFFFF`) on light backgrounds or gray text on neutral surfaces.
- Don't set font sizes outside the defined hierarchy; maintain consistent scale.
- Don't remove focus states from keyboard-accessible elements; always maintain visible focus indicators.

## 8. Responsive Behavior

### Breakpoints

| Breakpoint | Width | Key Changes |
|------------|-------|------------|
| Mobile | `320px – 479px` | Single column, `16px` padding, `44px` button height, `48px` heading size, full-width modals |
| Small Mobile | `480px – 767px` | Single column, `24px` padding, `50px` button height, responsive typography scaling |
| Tablet | `768px – 1023px` | 2-column grid, `32px` padding, `330px` button width, navigation collapses to hamburger |
| Desktop | `1024px – 1439px` | 3-column grid, `48px` padding, full navigation bar, max-width `1200px` containers |
| Large Desktop | `1440px+` | 4-column grid, `64px` padding, side navigation possible, `100px` margins |

### Touch Targets
- **Minimum Size**: `44px × 44px` (iOS standard) or `48px × 48px` (Android standard)
- **Spacing Between Targets**: Minimum `8px` to `12px` to prevent accidental taps
- **Button Implementation**: All buttons default to `50px` height on mobile, scaled to `44px` minimum on touch devices
- **Input Fields**: Minimum `40px` height with `12px` padding to accommodate comfortable typing
- **Link Hit Area**: Extend invisible hit area to at least `44px` square around text links

### Collapsing Strategy
- **Navigation**: Top bar navigation collapses to hamburger menu below `768px` width
- **Multi-Column Layouts**: 3-column grid collapses to 2-column at `768px`, then single-column at `480px`
- **Buttons**: Full-width (`330px`) buttons on mobile/tablet; auto-width on desktop
- **Cards**: Stack vertically on mobile; arrange in 2-column grid on tablet; 3+ columns on desktop
- **Hero Section**: Image-text layout stacks vertically below `768px`; text overlays image on desktop
- **Spacing**: Reduce gap/padding values by 50% below `768px` (e.g., `24px` becomes `12px`, `64px` becomes `32px`)

## 9. Agent Prompt Guide

### Quick Color Reference
- **Primary CTA**: Brand Green (`#1CB0F6`) – Use for main action buttons, key interactions
- **Secondary CTA**: Transparent with Blue Border (`#0000EE` stroke) – Use for alternative actions
- **Background**: White (`#FFFFFF`) or Off-White (`#F5F5F5`) – Default page/section backgrounds
- **Text**: Charcoal (`#3C3C3C`) – All body text, headings, navigation
- **Links**: Link Blue (`#0000EE`) – Hyperlinks and inline text actions
- **Accents**: Lime Green (`#00B086`) – Badges, secondary highlights, supporting elements
- **Borders**: Light Border (`#C1C1C1`) – Input borders, subtle dividers
- **Hover Overlay**: `rgba(28, 176, 246, 0.1)` – Subtle background tint on interactive hover

### Iteration Guide

1. **Always use DIN Round typeface** for all UI elements unless explicitly creating a campaign hero. Fall back to Trebuchet MS or Helvetica if DIN Round is unavailable.

2. **Apply `#1CB0F6` to primary buttons and key CTAs only.** This is the brand's signature color and should draw immediate attention. Overuse dilutes its impact.

3. **Maintain minimum `50px` button height** and `16px` horizontal padding. This ensures comfortable interaction on all devices and meets accessibility guidelines.

4. **Use `12px` border radius** as the default for buttons, cards, and interactive elements. Consistency in corner rounding creates a cohesive, friendly aesthetic.

5. **Group whitespace intentionally**: Use `24px` for related elements, `48px` for section separation, `64px+` for major content divisions. Breathing room reduces cognitive load.

6. **Implement hover and active states on all interactive elements.** At minimum: darken the background by 10% on hover, apply subtle scale (0.98) on active state.

7. **Ensure text contrast meets WCAG AA standards**: Use `#3C3C3C` on white; never use gray on gray or reduce opacity below 70% for body text.

8. **Scale typography using the defined hierarchy.** Avoid arbitrary font sizes; use the provided table for h1 (32px), body (17px), and button text (15px).

9. **Test all buttons and inputs at `44px` minimum height** on iOS/Android to meet native mobile guidelines. Scale up to `50px` for desktop emphasis.

10. **Use shadows sparingly and follow the elevation table.** Apply `0px 2px 8px rgba(0, 0, 0, 0.08)` for standard cards; increase only on hover or focus. Avoid hard shadows that create visual clutter.