# 🚀 Migration Guide - Environment Variable Controlled Migrations

## 📋 **How It Works**

This system uses environment variables to control when migrations and superuser creation happen, following Alan's suggestion from Render support.

## 🔧 **Current Configuration**

Your `render.yaml` is currently set to run migrations and create superuser on every deploy:

```yaml
envVars:
  - key: RUN_MIGRATIONS
    value: "true"
  - key: CREATE_SUPERUSER
    value: "true"
```

## 🎯 **Deployment Process**

### **Step 1: Initial Setup (Current State)**
- ✅ Migrations will run during build
- ✅ Superuser will be created during build
- ✅ Database tables will be created
- ✅ Admin panel will be accessible

### **Step 2: After First Successful Deploy**
Once your database is set up and working:

1. **Remove the environment variables** from your Render dashboard:
   - Go to your service settings
   - Remove `RUN_MIGRATIONS` environment variable
   - Remove `CREATE_SUPERUSER` environment variable
   - Save changes

2. **Update render.yaml** to remove the env vars:
   ```yaml
   # Remove these lines:
   # - key: RUN_MIGRATIONS
   #   value: "true"
   # - key: CREATE_SUPERUSER
   #   value: "true"
   ```

3. **Deploy again** - Now migrations won't run on every deploy

## 🔄 **Future Migrations**

When you need to run migrations in the future:

1. **Temporarily add the env var** in Render dashboard:
   - Add `RUN_MIGRATIONS` = `"true"`
   - Deploy
   - Remove the env var
   - Deploy again

2. **Or use the CLI approach** (if you have SSH access):
   ```bash
   render ssh hackwesttx-backend
   python3 manage.py migrate
   ```

## 🎛️ **Environment Variables Explained**

| Variable | Purpose | When to Use |
|----------|---------|-------------|
| `RUN_MIGRATIONS` | Runs `python manage.py migrate` | First deploy, when you add new models |
| `CREATE_SUPERUSER` | Creates admin user | First deploy only |
| `DEBUG` | Django debug mode | Never in production |
| `SECRET_KEY` | Django secret key | Always required |

## 🚨 **Important Notes**

- **Don't leave env vars set permanently
- **Remove env vars after first successful deploy**
- **Migrations only run when env vars are present**
- **Superuser creation only runs when env var is present**

## 🔍 **Monitoring**

Check your Render logs to see:
- ✅ Migration progress
- ✅ Superuser creation
- ✅ Build completion
- ✅ Server startup

## 🎉 **Expected Result**

After the first deploy with env vars:
- ✅ All database tables created
- ✅ Superuser `admin`/`admin123` created
- ✅ Admin panel accessible at `/admin/`
- ✅ No more "no such table" errors

## 🛠️ **Troubleshooting**

If something goes wrong:
1. Check Render logs for error messages
2. Verify environment variables are set correctly
3. Try removing and re-adding env vars
4. Check that all dependencies are installed

---

**This approach gives you full control over when migrations run, following Alan's excellent suggestion!** 🎯
