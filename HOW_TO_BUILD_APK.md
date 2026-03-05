# 📱 How to Build APK Using GitHub Actions

## ✅ Super Easy - No WSL Needed!

### Step 1: Create GitHub Account (if you don't have one)
1. Go to https://github.com
2. Click "Sign up"
3. Create your account

### Step 2: Create a New Repository
1. Click the **"+"** icon (top right)
2. Click **"New repository"**
3. Name it: `lecturer-student-app`
4. Keep it **Public**
5. **DO NOT** check "Initialize with README"
6. Click **"Create repository"**

### Step 3: Upload Your Project to GitHub

Open PowerShell in your project folder and run:

```powershell
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/lecturer-student-app.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your actual GitHub username!

### Step 4: GitHub Builds APK Automatically!

1. Go to your repository on GitHub
2. Click **"Actions"** tab
3. You'll see the build running (takes 15-20 minutes)
4. When done, click on the workflow
5. Download the APK from **"Artifacts"** section

### Step 5: Install on Phone

1. Download the APK to your phone
2. Open it and install
3. Done! 🎉

---

## 🆘 If Git is Not Installed

Download Git from: https://git-scm.com/download/win

Install it, then run the commands above.

---

## 📝 Quick Summary

1. Create GitHub account
2. Create repository
3. Upload project (3 commands)
4. Wait 15-20 minutes
5. Download APK
6. Install on phone

**That's it!** No WSL, no complicated setup! 🚀
