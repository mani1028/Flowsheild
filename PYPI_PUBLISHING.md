# PyPI Publishing Guide for FlowShield

This guide walks you through publishing `flowsh` (FlowShield) to PyPI using automated GitHub Actions workflows with trusted publishers (OIDC).

---

## 1. Prerequisites

✅ **Already done for you:**
- `setup.py` configured with `name="flowsh"`
- `pyproject.toml`-style metadata in place
- GitHub Actions workflow: `.github/workflows/publish.yml`

**What you need:**
- [PyPI account](https://pypi.org/account/register/) with `flowsh` project created
- GitHub repository set to public (or accessible to PyPI)
- Admin access to your GitHub repository

---

## 2. Configure Trusted Publishers on PyPI

This is the **critical step** for automated publishing without storing API tokens in GitHub secrets.

### Step A: Register Trusted Publisher in PyPI

1. Go to [https://pypi.org/project/flowsh/](https://pypi.org/project/flowsh/)
2. Click **Settings** (near top-right)
3. Left sidebar → **Publishing** → **Trusted Publishers**
4. Click **"Add a new trusted publisher"**
5. Fill in the form:
   - **PyPI Project Name:** `flowsh`
   - **GitHub repository owner:** `pravalika` (your username)
   - **Repository name:** `flowshield`
   - **Workflow filename:** `publish.yml`
   - **Environment name:** `pypi`

6. Click **"Save trusted publisher"**

The status will initially show **"pending"** until the first automated publish. After the first successful publish via GitHub Actions, it will become **"active"**.

### Step B: Verify Repository Settings (GitHub)

Your GitHub repo should have:
- **Settings** → **Environments** → **pypi** (optional, but recommended)
  - Leave "Environment protection rules" empty (trust all branches) OR
  - Add branch protection if desired (e.g., only main branch can publish)

---

## 3. Build & Publish Your First Release

### Option A: Automated (Recommended)

Once trusted publishers are configured, **create a GitHub release**:

```bash
# From your local repo
git tag -a v1.0.0 -m "FlowShield v1.0.0 - Production release"
git push origin main --tags
```

Then go to GitHub → **Releases** and draft/publish the release. The workflow will trigger automatically.

### Option B: Manual Upload (First Time)

If you prefer to upload manually before setting up the full workflow:

```bash
# 1. Install build tools
pip install build twine

# 2. Build distribution
python -m build

# 3. Upload to PyPI (with your username/password or API token)
twine upload dist/*
```

After this manual upload, the PyPI trusted publisher will activate automatically for future releases.

---

## 4. What the Workflow Does

The `.github/workflows/publish.yml` workflow is triggered by:
- **Automatic:** Creating a GitHub release
- **Manual:** Workflow dispatch button in GitHub Actions

The workflow:
1. ✅ Checks out your code
2. ✅ Installs Python 3.11
3. ✅ Builds `sdist` and `wheel` distributions
4. ✅ Validates packaging with `twine check`
5. ✅ Publishes to PyPI using **OIDC (Trusted Publishers)**
6. ✅ Creates a summary with distribution file sizes

**No API tokens or secrets needed!**

---

## 5. Publish a New Release

### Via GitHub UI (Easiest)

1. Update version in `setup.py`:
   ```python
   version="1.1.0"
   ```

2. Push your changes:
   ```bash
   git add setup.py
   git commit -m "Bump version to 1.1.0"
   git push origin main
   ```

3. Go to GitHub → **Releases** → **Draft a new release**
   - **Tag:** `v1.1.0`
   - **Title:** `FlowShield v1.1.0`
   - **Description:** Feature highlights, bug fixes, etc.
   - Click **Publish release**

4. The publish workflow will automatically trigger and upload to PyPI. Watch it in **Actions** tab.

### Via Command Line

```bash
# Update version
# ... edit setup.py ...

# Commit
git add setup.py
git commit -m "Bump version to 1.1.0"
git push origin main

# Create and push tag
git tag -a v1.1.0 -m "FlowShield v1.1.0"
git push origin main --tags

# Go to GitHub and create a release from the tag (or trigger manually via Actions)
```

---

## 6. Verify Publishing Success

### Check PyPI

1. Go to [https://pypi.org/project/flowsh/](https://pypi.org/project/flowsh/)
2. You should see your version listed with:
   - Download links (`.tar.gz` sdist and `.whl` wheel)
   - README rendered
   - Package metadata (classifiers, dependencies, etc.)

### Install Your Package

```bash
pip install flowsh
```

---

## 7. Version Numbering Best Practices

Use **semantic versioning** in your tags:

- **v1.0.0** → Initial production release
- **v1.0.1** → Patch (bug fixes only)
- **v1.1.0** → Minor (new features, backward compatible)
- **v2.0.0** → Major (breaking changes)

Always match the tag with `version` in `setup.py`.

---

## 8. Troubleshooting

### 429 Error / Rate Limit

The workflow includes `skip-existing: false`, which means it will reject re-uploading the same version. To republish:
- Increment version and tag
- Or delete the old release on PyPI (if needed)

### Workflow Fails with Auth Error

**Cause:** Trusted publisher not yet active or misconfigured

**Solution:**
1. Check PyPI Settings → Publishing → Trusted Publishers
   - Verify **owner**, **repo name**, **workflow filename**, **environment** are exactly correct
2. If it shows **"pending"**, do a manual `twine upload` first to activate it
3. After activation, subsequent releases will auto-publish

### Distribution Files Not Found

**Cause:** `python -m build` failed silently

**Solution:**
1. Run locally: `python -m build`
2. Check for errors in setup.py (missing imports, syntax issues)
3. Ensure `setup.py` is in the project root, not a subdirectory

### Can't Install from PyPI

**Cause:** Twine upload succeeded but PyPI indexing delay

**Solution:**
- Wait 5-10 minutes for CDN propagation
- Check [https://pypi.org/project/flowsh/](https://pypi.org/project/flowsh/) for your version
- Try `pip install --no-cache-dir flowsh`

---

## 9. Summary: Step-by-Step Checklist

- [ ] 1. Create PyPI account and register `flowsh` project
- [ ] 2. Configure **Trusted Publisher** in PyPI Settings (owner=pravalika, repo=flowshield, workflow=publish.yml, env=pypi)
- [ ] 3. (Optional) Set up GitHub environment protection rules
- [ ] 4. Update `setup.py` version to `1.0.0`
- [ ] 5. Create GitHub release (tag `v1.0.0`) via UI or git commands
- [ ] 6. Monitor workflow in **Actions** tab → **Publish to PyPI**
- [ ] 7. Verify on [PyPI project page](https://pypi.org/project/flowsh/)
- [ ] 8. Install and test: `pip install flowsh`
- [ ] 9. For future releases: update version → push → create release → workflow runs automatically ✅

---

## 10. What's Next?

### Automated Badge Updates

Your README usually references PyPI badges. Update them to:

```markdown
[![PyPI](https://img.shields.io/pypi/v/flowsh?style=for-the-badge)](https://pypi.org/project/flowsh/)
```

### CI/CD Integration

Your existing `.github/workflows/tests.yml` already runs on push/PR. The `publish.yml` workflow is separate and only triggers on releases.

### Post-Launch Promotion

Once published:
- Announce on Reddit (`/r/Python`, `/r/flask`)
- Share on Twitter/LinkedIn
- Submit to Awesome Python lists
- Create demo video (FlowShield vs SlowAPI)

---

## Questions?

For PyPI publishing help, see the official [PyPI docs](https://packaging.python.org/tutorials/packaging-projects/).
For GitHub Actions help, see [GitHub Docs – Publishing Packages](https://docs.github.com/en/actions/publishing-packages).
