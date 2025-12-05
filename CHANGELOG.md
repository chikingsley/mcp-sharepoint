# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2024-12-05

### Added
- **Certificate authentication** - Secure app-only auth using X.509 certificates instead of client secrets
- **Interactive setup wizard** (`mcp-sharepoint-setup`) - Generates certificates, walks through Azure setup, outputs ready-to-use config
- **Comprehensive test suite** - 45+ tests including unit and integration tests
- **Real SharePoint integration tests** - Tests against actual SharePoint API
- **CI/CD pipeline** - GitHub Actions with lint, type check, and test jobs
- **Code coverage reporting** - Codecov integration with coverage badges
- **Type checking** - Full type annotations with `ty` checker

### Changed
- **Python 3.12+ required** - Upgraded from Python 3.10
- **Pydantic settings** - Configuration now uses pydantic-settings for validation
- **Ruff for linting** - Replaced previous linter with Ruff
- **Improved path validation** - SharePoint path security checks

### Fixed
- Various path traversal security improvements
- Better error handling throughout

## [0.1.7] - Previous Release

### Added
- File metadata tools (get/update metadata)
- SharePoint tree visualization
- PDF content extraction
- Large file upload support

## [0.1.6] - Earlier

### Added
- Enhanced documentation
- Improved service stability

## [0.1.0] - Initial Release

### Added
- Basic SharePoint document operations
- Folder management
- Client secret authentication
