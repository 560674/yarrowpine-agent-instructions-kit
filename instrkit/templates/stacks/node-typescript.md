## Project type
Node.js + TypeScript.

## Repository layout
- `src/`: TypeScript source
- `test/` or `*.test.ts`: tests

## Setup and commands
- Install: `npm ci`
- Build: `npm run build`
- Test: `npm test`
- Typecheck: `npx tsc --noEmit`
- Lint: `npm run lint`

## Code rules
- `strict` TypeScript; no `any` without a comment explaining why.
- Use the package manager already in the repo (look at the lockfile); do not switch.
- Do not edit `dist/` or other build output.
