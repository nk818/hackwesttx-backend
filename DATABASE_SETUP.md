# PostgreSQL Database Setup for Render

## Issue
The database `blueprint-postures-learn` doesn't exist in your PostgreSQL instance.

## Solution Options

### Option 1: Create Database Manually in Render Dashboard (Recommended)

1. Go to your Render Dashboard
2. Navigate to your PostgreSQL database service
3. Open the **PostgreSQL** shell or use the **Connect** tab
4. Run this SQL command:
   ```sql
   CREATE DATABASE "blueprint-postures-learn";
   ```
   Or if hyphens cause issues:
   ```sql
   CREATE DATABASE blueprint_postures_learn;
   ```

### Option 2: Use the Auto-Creation Script

The `create_database.py` script will attempt to create the database automatically during build. If you have sufficient privileges, it should work.

### Option 3: Verify Database Name

The database name in your connection string might be incorrect. Check:

1. In Render Dashboard → Your PostgreSQL Service
2. Look at the **Connections** tab
3. Verify the actual database name
4. Update `DATABASE_URL` in `render.yaml` if different

### Option 4: Use Default Database

If your user has access to a default database (usually `postgres`), you can:

1. Connect to the `postgres` database first
2. Create your database from there

## Current Configuration

Your current connection string points to:
- **Host**: `dpg-d3s34rodl3ps73d29o70-a`
- **Port**: `5432`
- **Database**: `blueprint-postures-learn`
- **User**: `blueprint_postures_learn_user`

## Quick Fix

If the database exists but has a different name, update `render.yaml`:

```yaml
- key: DATABASE_URL
  value: postgresql://blueprint_postures_learn_user:FOlENaCbVYqr9ZwBOE5QEkSRxkKgp8Lv@dpg-d3s34rodl3ps73d29o70-a:5432/ACTUAL_DB_NAME
```

Replace `ACTUAL_DB_NAME` with the correct database name from your Render PostgreSQL service.

