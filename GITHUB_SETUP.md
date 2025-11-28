# GitHub Setup Guide for Rubik's Cube Solver

## 📋 Prerequisite: GitHub Account

Make sure you have:
1. A GitHub account (https://github.com)
2. Git installed on your system
3. SSH key or Personal Access Token set up

## 🚀 Step 1: Initialize Git Repository Locally

Open PowerShell in the project directory and run:

```powershell
cd "c:\Users\hp\OneDrive\Desktop\rubik solver"

# Initialize git repository
git init

# Configure git with your name and email
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Rubik's Cube solver with IDA*, BFS, and Kociemba algorithms"
```

## 🌐 Step 2: Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `rubik-cube-solver`
3. Description: "High-performance Rubik's Cube solver with multiple algorithms (IDA*, BFS, Kociemba)"
4. Choose: Public (for portfolio) or Private (for security)
5. DO NOT initialize with README (we already have one)
6. Click "Create repository"

## 🔗 Step 3: Connect Local to Remote

After creating the repo on GitHub, you'll see setup instructions. Run:

### Option A: Using HTTPS (Easier)

```powershell
# Add remote origin
git remote add origin https://github.com/YOUR_USERNAME/rubik-cube-solver.git

# Rename main branch if needed
git branch -M main

# Push to GitHub
git push -u origin main
```

### Option B: Using SSH (More Secure)

```powershell
# Add remote origin with SSH
git remote add origin git@github.com:YOUR_USERNAME/rubik-cube-solver.git

# Rename main branch if needed
git branch -M main

# Push to GitHub
git push -u origin main
```

## ✅ Verification

Check that your repo was pushed successfully:

```powershell
# View remote URL
git remote -v

# Should output:
# origin  https://github.com/YOUR_USERNAME/rubik-cube-solver.git (fetch)
# origin  https://github.com/YOUR_USERNAME/rubik-cube-solver.git (push)
```

Then visit: `https://github.com/YOUR_USERNAME/rubik-cube-solver`

## 📝 Step 4: Update README with GitHub Link (Optional)

Edit `README.md` and update the URLs:

```markdown
## 🔗 Links

- **GitHub Repository**: [rubik-cube-solver](https://github.com/YOUR_USERNAME/rubik-cube-solver)
- **Issues**: [Report bugs](https://github.com/YOUR_USERNAME/rubik-cube-solver/issues)
```

Then commit and push:

```powershell
git add README.md
git commit -m "Update GitHub links in README"
git push
```

## 🔄 Future Updates

After making changes:

```powershell
# Check status
git status

# Add changes
git add .

# Commit with meaningful message
git commit -m "Add feature: XYZ"

# Push to GitHub
git push
```

## 📚 Useful Git Commands

```powershell
# View commit history
git log --oneline

# Create a new branch
git checkout -b feature/my-feature

# Switch branches
git checkout main

# Merge branch
git merge feature/my-feature

# Remove file from git (but keep locally)
git rm --cached filename

# Undo last commit (keep changes)
git reset --soft HEAD~1
```

## 🎖️ Portfolio Tips

For maximum impact on your portfolio:

1. **Add a badge to README**:
```markdown
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
```

2. **Add GitHub Actions (CI/CD)**:
Create `.github/workflows/tests.yml`:
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v
```

3. **Add Topics** to your GitHub repo:
   - `python`
   - `rubiks-cube`
   - `solver`
   - `ida-star`
   - `algorithm`
   - `opencv`

4. **Create Releases** for versions:
```powershell
# Create a tag
git tag -a v1.0.0 -m "Version 1.0.0 - Initial release"

# Push tags
git push origin v1.0.0
```

## 🆘 Troubleshooting

### "fatal: not a git repository"
```powershell
# You need to run git init in the project directory
git init
```

### "Permission denied (publickey)"
```powershell
# Use HTTPS instead of SSH, or set up SSH keys:
# https://docs.github.com/en/authentication/connecting-to-github-with-ssh
```

### "fatal: The current branch main has no upstream branch"
```powershell
# Run this to set upstream
git push -u origin main
```

### Accidentally committed large files
```powershell
# Remove from git history (careful!)
# Use BFG Repo-Cleaner: https://rtyley.github.io/bfg-repo-cleaner/
```

## 📞 Support

- GitHub Docs: https://docs.github.com
- Git Help: `git help <command>`
- GitHub Support: https://github.com/contact

---

**Congratulations!** Your Rubik's Cube Solver is now on GitHub! 🎉
