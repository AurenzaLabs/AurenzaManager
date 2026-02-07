# Aurenza Money Manager

A Streamlit-based financial tracking application for managing income and expenses with authentication.

## Features

- 🔐 Shared password authentication for founders
- 💰 Track income and expenses
- 🏷️ Tag-based categorization
- 📊 Visual dashboard with metrics and charts
- 📸 Image attachment support for transactions
- 💳 Multiple payment modes (Cash, Card, UPI, Bank)

## Technology Stack

- **Frontend**: Streamlit
- **Database**: Supabase (PostgreSQL)
- **Authentication**: bcrypt password hashing
- **Visualization**: Plotly, Pandas

## Setup

### 1. Clone and Install Dependencies

```bash
cd /Users/abhishek/Documents/Aurenza/AurenzaManager
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

Get these from your Supabase project settings at https://app.supabase.com

### 3. Set Up Database

1. Create a Supabase project at https://supabase.com
2. Run the SQL migration script in the Supabase SQL Editor:
   - Navigate to SQL Editor in your Supabase dashboard
   - Copy contents from `migrations/001_create_tables.sql`
   - Execute the script

### 4. Create Initial User (Optional)

If you need to create or reset the founder password, use the Supabase dashboard:

1. Go to Table Editor → `users` table
2. Insert a new row:
   - `type`: `shared_founder_password`
   - `password`: (use a bcrypt hash of your desired password)
   - `created_at`: Current timestamp

To generate a bcrypt hash in Python:
```python
import bcrypt
password = "your_password"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
print(hashed.decode('utf-8'))
```

### 5. Run the Application

```bash
streamlit run Homepage.py
```

The app will be available at http://localhost:8501

## Project Structure

```
AurenzaManager/
├── Homepage.py                 # Main dashboard page
├── pages/
│   └── 1_Journal_Entries.py   # Transaction entry page
├── auth.py                     # Authentication logic
├── db.py                       # Database connection
├── migrations/
│   └── 001_create_tables.sql  # Database schema
├── scripts/
│   ├── export_mongo_data.py   # MongoDB export utility
│   └── import_to_supabase.py  # Supabase import utility
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in git)
└── MIGRATION_GUIDE.md         # Migration instructions
```

## Usage

1. **Login**: Enter the shared founder password on the homepage
2. **View Dashboard**: See income, expenses, balance, and category breakdowns
3. **Add Transaction**: Navigate to "Journal Entries" page to add new transactions
4. **Upload Images**: Optionally attach receipts or images to transactions
5. **Track Tags**: Use tags to categorize transactions for better insights

## Database Schema

### Users Table
- Stores authentication credentials
- Uses bcrypt for password hashing
- Supports shared founder password model

### Transactions Table
- Stores all financial transactions
- Supports multiple tags per transaction
- Optional binary image storage
- Indexed for performance on date and type fields

## Migration from MongoDB

If you're migrating from MongoDB, see [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for detailed instructions.

## Security Notes

- Passwords are hashed using bcrypt
- Environment variables should never be committed to git
- Row Level Security (RLS) can be enabled in Supabase for additional protection
- The `.env` file is gitignored by default

## License

Private project for Aurenza Labs founders.
