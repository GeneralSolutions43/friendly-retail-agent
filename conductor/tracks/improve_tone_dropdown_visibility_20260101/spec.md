# Spec: Improve Tone Dropdown Visibility

## Overview
The tone selection dropdown in the chat header is currently difficult to see, and the options within it lack sufficient contrast. This track aims to improve the visibility and usability of the dropdown by updating its text color, border, and background styles.

## Functional Requirements
- **Text Color:** Update the dropdown text and its options to `text-zinc-900`.
- **Border Styling:** Update the border color to `border-zinc-300` for better definition.
- **Background Styling:** Add a light background color `bg-zinc-50` to the dropdown.

## Acceptance Criteria
- [ ] The "Tone:" label and the selected value in the dropdown are clearly visible (zinc-900).
- [ ] All options within the dropdown menu have high contrast and are easy to read.
- [ ] The dropdown has a visible border (zinc-300) and a subtle background (zinc-50).
- [ ] The dropdown remains functional and correctly updates the agent's tone.

## Out of Scope
- Changing the position of the dropdown in the header.
- Modifying the list of available tones.
