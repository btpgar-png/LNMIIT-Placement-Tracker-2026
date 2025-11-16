# Export Companies from Live Site - Quick Guide

## Why This Matters

**Your manually added companies ARE saved in the database** on Render. However, if the database gets reset or you redeploy, only the companies in `seed.py` will be restored.

To make your 37 companies permanent, we need to update `seed.py` with all of them.

## Quick Solution (2 minutes)

### Option 1: Browser Console Export (Easiest)

1. **Open your site**: https://lnmiit-placement-tracker-2026-1.onrender.com/

2. **Open Browser Console**:

   - Press `F12` OR
   - Right-click → Inspect → Console tab

3. **Paste and run this code**:

   ```javascript
   fetch("/api/companies")
     .then((r) => r.json())
     .then((data) => {
       const jsonStr = JSON.stringify(data, null, 2);
       console.log(jsonStr);
       // Copy everything from the console
       navigator.clipboard.writeText(jsonStr).then(() => {
         console.log("✓ Copied to clipboard!");
       });
     });
   ```

4. **Save the output**:

   - Copy the JSON from console (or it auto-copied to clipboard)
   - Create file: `backend/companies.json`
   - Paste the JSON content

5. **Update seed file**:

   ```bash
   cd backend
   python update_seed_from_json.py
   ```

6. **Done!** Your `seed.py` now has all 37 companies.

### Option 2: Direct API Access

If you have access to the Render dashboard:

1. Get the database connection string
2. Export directly using SQL or database tools
3. Convert to JSON format
4. Use `update_seed_from_json.py`

## Verify It Worked

After running `update_seed_from_json.py`, check:

```bash
# Count companies in seed.py
python -c "from app.seed import sample_data; print(f'Companies in seed: {len(sample_data)}')"
```

Should show: `Companies in seed: 37`

## Important Notes

- ✅ **Data on Render persists** - Your 37 companies are safe in the live database
- ✅ **After updating seed.py** - They'll persist even if database resets
- ✅ **Commit to Git** - Push the updated `seed.py` to GitHub so it's backed up

## Troubleshooting

**"companies.json not found"**

- Make sure you saved the file in the `backend/` folder
- Check the filename is exactly `companies.json` (not `companies.json.txt`)

**"Invalid JSON"**

- Make sure you copied the entire JSON output
- Check for any extra text before/after the JSON
- The JSON should start with `[` and end with `]`

**Still showing 28 companies**

- Make sure you ran `update_seed_from_json.py` from the `backend/` folder
- Check that `app/seed.py` was updated (check file modification time)
