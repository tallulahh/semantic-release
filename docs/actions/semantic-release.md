# Semantic Release
**Path:** `.github/actions/semantic-release/action.yml`  **README:** [View full documentation](../../.github/actions/semantic-release/README.md)
## Description
Run semantic-release to automate versioning, changelog, and releases

## Inputs
| Name | Required | Default | Description |
|------|----------|---------|-------------|
| node-version | False | 18 | Node.js version to use |
| npm-token | False |  | NPM token for publishing packages (optional) |
| github-token | True |  | GitHub token with repo write permissions |
## Outputs
_None_
## Runs
- **using:** `composite`
- **steps:** 4

## Example Usage
```yaml
- uses: tallulahh/semantic-release/actions/semantic-release@v1
  with:
    node-version: 18
    npm-token: <value>
    github-token: <value>
```
