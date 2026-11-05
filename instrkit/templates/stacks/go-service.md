## Project type
Go service.

## Repository layout
- `cmd/`: entry points
- `internal/`: application packages (not importable from outside)

## Setup and commands
- Build: `go build ./...`
- Test: `go test ./...`
- Race check: `go test -race ./...`
- Format/vet: `gofmt -l . && go vet ./...`

## Code rules
- Return errors with context (`fmt.Errorf("doing x: %w", err)`); do not panic in library code.
- Pass `context.Context` as the first argument to I/O functions.
- Keep `go.mod` tidy: `go mod tidy` after dependency changes.
