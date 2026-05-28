---
name: Premium Salon Agenda
colors:
  surface: '#fff8f5'
  surface-dim: '#edd5ca'
  surface-bright: '#fff8f5'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#fff1ea'
  surface-container: '#ffeadf'
  surface-container-high: '#fbe3d7'
  surface-container-highest: '#f6ded2'
  on-surface: '#251912'
  on-surface-variant: '#584235'
  inverse-surface: '#3b2d26'
  inverse-on-surface: '#ffede5'
  outline: '#8c7263'
  outline-variant: '#e0c0af'
  surface-tint: '#994700'
  primary: '#994700'
  on-primary: '#ffffff'
  primary-container: '#ff7a00'
  on-primary-container: '#5c2800'
  inverse-primary: '#ffb68b'
  secondary: '#5d5f5f'
  on-secondary: '#ffffff'
  secondary-container: '#dfe0e0'
  on-secondary-container: '#616363'
  tertiary: '#006399'
  on-tertiary: '#ffffff'
  tertiary-container: '#00a8ff'
  on-tertiary-container: '#003a5c'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdbc8'
  primary-fixed-dim: '#ffb68b'
  on-primary-fixed: '#321200'
  on-primary-fixed-variant: '#753400'
  secondary-fixed: '#e2e2e2'
  secondary-fixed-dim: '#c6c6c7'
  on-secondary-fixed: '#1a1c1c'
  on-secondary-fixed-variant: '#454747'
  tertiary-fixed: '#cde5ff'
  tertiary-fixed-dim: '#95ccff'
  on-tertiary-fixed: '#001d32'
  on-tertiary-fixed-variant: '#004a75'
  background: '#fff8f5'
  on-background: '#251912'
  surface-variant: '#f6ded2'
  bg-light: '#F8F9FA'
  bg-dark: '#121212'
  text-primary-light: '#1F2937'
  text-primary-dark: '#F3F4F6'
  border-subtle: rgba(0, 0, 0, 0.08)
  status-success: '#34C759'
  status-error: '#FF3B30'
typography:
  display-lg:
    fontFamily: metropolis
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: metropolis
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: metropolis
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.2'
  headline-md:
    fontFamily: metropolis
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  body-lg:
    fontFamily: metropolis
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: metropolis
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  label-md:
    fontFamily: metropolis
    fontSize: 14px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.05em
  caption:
    fontFamily: metropolis
    fontSize: 12px
    fontWeight: '400'
    lineHeight: '1.4'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  container-margin-mobile: 1.25rem
  container-margin-desktop: 2.5rem
  gutter: 1.5rem
  stack-sm: 0.5rem
  stack-md: 1rem
  stack-lg: 2rem
---

## Brand & Style

The design system is centered on a **Premium Minimalist** aesthetic, merging the meticulous hardware-inspired precision of Apple with the high-utility functionalism of modern SaaS tools. The goal is to elevate a standard hair salon booking process into a luxury digital experience.

The system prioritizes **Clarity and intentionality**. It avoids "academic" UI patterns like dense data tables in favor of high-contrast typography, generous negative space, and smooth, responsive transitions. The interface should feel calm, professional, and expensive, ensuring that the technology never distracts from the artistry of the salon service itself. 

Key stylistic pillars include:
- **Clean Lines:** Elimination of unnecessary dividers; using whitespace to define groupings.
- **Purposeful Motion:** Subtle transitions that mimic the physical world (soft fades, gentle card elevations).
- **Modern SaaS Aesthetics:** Utilizing shadows and blurs to create a sense of depth and hierarchy.

## Colors

The color palette is anchored by a high-energy **Vibrant Orange** (#FF7A00) used strictly for calls to action, brand highlights, and interactive states. This creates a striking contrast against the monochromatic foundation.

### Palette Strategy
- **Primary:** Reserved for the "Brand Moment"—buttons, active states in the timeline, and selection indicators.
- **Surface Strategy:** In Light Mode, we use a slightly off-white (#F8F9FA) for the background to reduce eye strain, with pure white cards. In Dark Mode, a deep matte charcoal (#121212) is used to maintain a premium "Pro" feel.
- **Functional Colors:** Success and Error states follow the iOS HIG standards to ensure instant user recognition of status changes.
- **Neutrals:** Grays are derived from the blue-tinted slate family to provide a modern, cool-toned counterweight to the warm primary orange.

## Typography

This design system utilizes **Metropolis** (as a high-fidelity alternative to SF Pro) to maintain the geometric, clean, and modern look characteristic of premium tech ecosystems.

### Hierarchy Rules
- **Display & Headlines:** Use tight letter spacing and bold weights to command attention. These should be set in near-black (#1F2937) for maximum legibility.
- **Body Text:** Optimized for readability with slightly increased line height (1.5-1.6x).
- **Labels:** Small caps or uppercase with increased tracking (letter spacing) are used for "over-titles" or meta-data (e.g., "SERVICE DURATION").
- **Timeline Scales:** Times on the vertical axis should use the `caption` style to remain helpful but unobtrusive.

## Layout & Spacing

The layout uses a **Fluid-Fixed Hybrid** model. While the overall container respects maximum widths on desktop to maintain readability, the internal spacing follows a strict 8px grid system.

### Layout Philosophy
- **Vertical Timeline:** The core of the admin experience. It utilizes a left-aligned time axis with cards spanning the remaining horizontal space.
- **Mobile Navigation:** Employs a fixed bottom navigation bar for high "thumb-zone" reachability. Icons should be clear and paired with `caption` labels.
- **Desktop Navigation:** A clean top header with no sidebar to maximize horizontal space for the agenda timeline.
- **Responsive Reflow:** On mobile, forms and card stacks are strictly single-column. On desktop, they transition into a two-column grid to prevent excessively long line lengths.

## Elevation & Depth

To achieve the "Apple-inspired" look, this design system avoids heavy, muddy shadows. Instead, it uses **Tonal Layers and Subtle Ambient Depth**.

- **Surface 0 (Background):** #F8F9FA. The lowest layer.
- **Surface 1 (Cards):** Pure White (#FFFFFF) with a very soft, diffused shadow (`0px 4px 20px rgba(0,0,0,0.04)`). 
- **Interaction Depth:** When a card is hovered or pressed, the shadow deepens slightly, and the card may lift (translate -2px) to provide tactile feedback.
- **Overlays:** Modals and bottom sheets use a **Backdrop Blur** (Glassmorphism) of 20px and a 60% opacity white/black tint to maintain context while focusing the user.

## Shapes

The shape language is **Rounded**, reflecting a friendly yet professional demeanor. 

- **Standard Elements:** Buttons, input fields, and small cards use a 0.5rem (8px) radius.
- **Large Components:** Main agenda containers and hero sections use a 1rem (16px) radius to feel more substantial.
- **Selection Indicators:** Small dots or status pills use a full "pill" radius for distinct visual differentiation from functional buttons.

## Components

### Buttons
- **Primary:** High-contrast outline buttons. 1.5px border in `#FF7A00`. On hover, the background fills with `#FF7A00` and text transitions to `#FFFFFF`.
- **Ghost:** No border, primary color text. Used for less urgent actions like "Cancel" or "Back".

### Cards
- **SaaS-Style Cards:** Defined by a 1px solid border (`#00000014`) and a very light ambient shadow. 
- **Timeline Cards:** Should feature a vertical accent bar on the left edge in the primary color to indicate "active" or "confirmed" status.

### Timeline
- A vertical "ruler" on the left side with 30-minute increments.
- Turno cards occupy the space to the right. 
- Overlapping appointments (if any) should slightly stagger, though the system logic aims to prevent this.

### Input Fields
- Understated design: 1px border that shifts from light gray to Primary Orange on focus. 
- Floating labels or high-contrast top labels using the `label-md` typography style.

### Chips/Pills
- Used for "Service Tags" (e.g., "Haircut", "Balayage"). Soft background tint of the primary color at 10% opacity with 100% opacity text.