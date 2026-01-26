# 📦 Publishing TodoX to PyPI

This guide walks you through the complete process of publishing TodoX to the Python Package Index (PyPI).

## Prerequisites

1. **PyPI Account**: Register at [pypi.org](https://pypi.org/account/register/)
2. **TestPyPI Account** (optional but recommended): Register at [test.pypi.org](https://test.pypi.org/account/register/)
3. **API Tokens**: Generate tokens for authentication

## 🔧 Setup

### 1. Install Build Tools

```bash
pip install --upgrade pip
pip install build twine
```

### 2. Configure PyPI Credentials

Create `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR_PRODUCTION_TOKEN_HERE

[testpypi]
username = __token__
password = pypi-YOUR_TEST_TOKEN_HERE
repository = https://test.pypi.org/legacy/
```

**Security Note**: Keep your tokens secure! Never commit `.pypirc` to Git.

## 📝 Pre-Publishing Checklist

- [ ] Update version number in `pyproject.toml`
- [ ] Update `README.md` with latest features
- [ ] Test all CLI commands locally
- [ ] Test TUI functionality
- [ ] Run linters/formatters (if applicable)
- [ ] Commit all changes to Git
- [ ] Tag the release: `git tag v0.1.0`

## 🏗️ Building the Package

### Clean Previous Builds

```bash
rm -rf dist/ build/ *.egg-info/
```

### Build Distribution Files

```bash
python -m build
```

This creates:
- `dist/todox-X.X.X-py3-none-any.whl` (wheel file)
- `dist/todox-X.X.X.tar.gz` (source distribution)

### Verify the Build

```bash
ls dist/
# Should show .whl and .tar.gz files
```

## 🧪 Testing on TestPyPI (Recommended)

### Upload to TestPyPI

```bash
twine upload --repository testpypi dist/*
```

### Test Installation

```bash
# Create a test environment
python -m venv test_env
source test_env/bin/activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ todox

# Test the installation
todox --help
todox add "Test task"
todox list

# Clean up
deactivate
rm -rf test_env
```

## 🚀 Publishing to Production PyPI

### Upload to PyPI

```bash
twine upload dist/*
```

You'll be prompted to confirm. Type `yes` to proceed.

### Verify the Upload

1. Visit: `https://pypi.org/project/todox/`
2. Check that your package appears correctly
3. Test installation:

```bash
pip install todox
todox --help
```

## 🔄 Updating to a New Version

### 1. Update Version Number

Edit `pyproject.toml`:

```toml
[project]
name = "todox"
version = "0.2.0"  # Increment this
```

### 2. Document Changes

Update `CHANGELOG.md` (create if needed):

```markdown
## [0.2.0] - 2024-01-26

### Added
- New feature X
- Improved Y

### Fixed
- Bug Z
```

### 3. Commit and Tag

```bash
git add pyproject.toml CHANGELOG.md
git commit -m "Bump version to 0.2.0"
git tag v0.2.0
git push origin main --tags
```

### 4. Build and Upload

```bash
rm -rf dist/
python -m build
twine upload dist/*
```

## 📋 Version Numbering Guide

Follow [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH):

- **MAJOR** (1.0.0): Breaking changes, incompatible API changes
- **MINOR** (0.2.0): New features, backwards-compatible
- **PATCH** (0.1.1): Bug fixes, backwards-compatible

Examples:
- `0.1.0` → `0.1.1`: Bug fix
- `0.1.0` → `0.2.0`: New feature
- `0.9.0` → `1.0.0`: First stable release

## 🛡️ Security Best Practices

1. **Use API Tokens**: Never use your password directly
2. **Scope Tokens**: Create separate tokens for each project
3. **Keep `.pypirc` Private**: Add to `.gitignore`
4. **Rotate Tokens**: Periodically regenerate tokens
5. **Enable 2FA**: On your PyPI account

## 🐛 Troubleshooting

### "Package already exists"

If you see this error, you've already uploaded this version:
- Increment the version number in `pyproject.toml`
- Rebuild and upload again

### "Invalid credentials"

- Check your API token in `~/.pypirc`
- Ensure you're using `__token__` as username
- Regenerate token on PyPI if needed

### "Missing dependencies"

```bash
# Install all build dependencies
pip install --upgrade build twine setuptools wheel
```

### Verify Package Metadata

```bash
twine check dist/*
```

## 📚 Additional Resources

- [PyPI Help](https://pypi.org/help/)
- [Python Packaging Guide](https://packaging.python.org/)
- [Twine Documentation](https://twine.readthedocs.io/)

## 🎯 Quick Reference Commands

```bash
# Complete publishing workflow
rm -rf dist/ build/ *.egg-info/
python -m build
twine check dist/*
twine upload --repository testpypi dist/*  # Test first
twine upload dist/*                        # Production

# Verify installation
pip install todox
todox --help
```

---

**Note**: Always test on TestPyPI before publishing to production!
