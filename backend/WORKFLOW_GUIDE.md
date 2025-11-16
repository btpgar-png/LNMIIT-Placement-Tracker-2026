# Workflow Guide - Adding Companies

## Quick Answer: Do I Need to Update seed.py Every Time?

**NO!** You don't need to update `seed.py` every time you add companies.

## How It Works

### Your Normal Workflow (Adding Companies):

1. **Add companies via frontend** → Data saved to database ✅
2. **That's it!** Your data persists automatically ✅

### seed.py is Just a Backup

- `seed.py` is only used when database is **empty** (fresh deployments)
- Your **live database** is the source of truth
- `seed.py` is a **backup/restore file**

## When to Update seed.py

### Option 1: Periodic Backup (Recommended)

Update `seed.py` periodically (e.g., monthly or after major additions):

```bash
# 1. Export from live site (browser console)
fetch('/api/companies').then(r => r.json()).then(d => {
  console.log(JSON.stringify(d, null, 2));
  navigator.clipboard.writeText(JSON.stringify(d, null, 2));
});

# 2. Save as companies.json in backend folder

# 3. Run sync script
python sync_seed_from_live.py
```

### Option 2: Before Important Deployments

Update `seed.py` before major deployments to ensure backup is current.

### Option 3: Never (Not Recommended)

You can skip updating `seed.py`, but if database resets, you'll lose manually added companies.

## Recommended Workflow

### Daily/Weekly:

- ✅ Add companies via frontend
- ✅ Data saves automatically
- ✅ No need to touch seed.py

### Monthly/Quarterly:

- 📦 Export data from live site
- 📦 Run `sync_seed_from_live.py`
- 📦 Commit to Git as backup

## Summary

| Action                   | Update seed.py? | Why                                  |
| ------------------------ | --------------- | ------------------------------------ |
| Add company via frontend | ❌ No           | Data saves to database automatically |
| Monthly backup           | ✅ Yes          | Keep seed.py as backup               |
| Before deployment        | ✅ Yes          | Ensure backup is current             |
| Database reset           | ✅ Already done | seed.py restores data                |

## Bottom Line

**Your data is safe in the database!**

- Add companies normally via frontend
- Update `seed.py` only when you want to backup
- Your data persists automatically ✅
