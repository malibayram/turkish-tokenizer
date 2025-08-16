# GitHub Actions Setup Guide

This guide will help you set up automated testing and PyPI publishing for the Turkish Tokenizer project.

## 🚀 Quick Setup

### 1. Add PyPI API Token to GitHub Secrets

1. **Get your PyPI API token:**

   - Go to [PyPI Account Settings](https://pypi.org/manage/account/)
   - Scroll down to "API tokens"
   - Click "Add API token"
   - Give it a name (e.g., "turkish-tokenizer-pypi")
   - Select "Entire account (all projects)" or "Specific project: turkish-tokenizer"
   - Copy the token (it starts with `pypi-`)

2. **Add the token to GitHub:**
   - Go to your GitHub repository: `https://github.com/malibayram/turkish-tokenizer`
   - Click "Settings" tab
   - In the left sidebar, click "Secrets and variables" → "Actions"
   - Click "New repository secret"
   - Name: `PYPI_API_TOKEN`
   - Value: Your PyPI token (e.g., `pypi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)
   - Click "Add secret"

### 2. (Optional) Add TestPyPI Token

If you want to also publish to TestPyPI for testing:

1. **Get TestPyPI API token:**

   - Go to [TestPyPI Account Settings](https://test.pypi.org/manage/account/)
   - Create an account if you don't have one
   - Add an API token similar to PyPI

2. **Add to GitHub secrets:**

- Name: `TEST_PYPI_API_TOKEN`
- Value: Your TestPyPI token

## 📦 Publishing Workflows

### Automatic Publishing

The project will automatically publish to PyPI when:

1. **Version tags are pushed:**

   ```bash
   # Create a new version
   make version-minor  # or version-major, version-bump

   # Create and push a release tag
   make release
   ```

2. **Manual triggering:**
   - Go to GitHub Actions tab
   - Click on "Publish to PyPI" workflow
   - Click "Run workflow"

### Manual Publishing

For manual publishing without GitHub Actions:

```bash
# Build and publish locally
make publish
```

## 🧪 Testing Workflows

Tests run automatically on:

- Every push to `main` or `develop` branches
- Every pull request to `main` branch
- Multiple Python versions (3.8, 3.9, 3.10, 3.11, 3.12, 3.13)

## 🔧 Troubleshooting

### Common Issues

1. **"Trusted publishing exchange failure"**

   - This happens when using the old trusted publishing workflow
   - The new workflow uses token-based authentication
   - Make sure you've added the `PYPI_API_TOKEN` secret

2. **"No matching distribution found"**

   - PyPI takes a few minutes to index new packages
   - Wait 5-10 minutes after publishing

3. **"Permission denied"**
   - Check that your PyPI token has the correct permissions
   - Ensure the token is for the correct project

### Debugging

1. **Check GitHub Actions logs:**

   - Go to Actions tab in your repository
   - Click on the failed workflow run
   - Check the logs for specific error messages

2. **Test locally first:**

   ```bash
   make test
   make build
   twine check dist/*
   ```

3. **Verify secrets:**
   - Go to repository Settings → Secrets and variables → Actions
   - Ensure `PYPI_API_TOKEN` is set correctly

## 📋 Release Checklist

Before creating a new release:

- [ ] Run tests: `make test`
- [ ] Check code quality: `make lint`
- [ ] Update version: `make version-minor` (or appropriate)
- [ ] Create release: `make release`
- [ ] Monitor GitHub Actions for success
- [ ] Verify package on PyPI: https://pypi.org/project/turkish-tokenizer/

## 🔗 Useful Links

- [PyPI Account Settings](https://pypi.org/manage/account/)
- [TestPyPI Account Settings](https://test.pypi.org/manage/account/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyPI Publishing Guide](https://packaging.python.org/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/)
