#!/usr/bin/env python3
"""
Manual Data Seeding Script
Run this to seed/reseed the database with realistic Vietnamese high school data
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database.init_db import clear_database, init_database
from database.seed_data import seed_database


def main():
    print("=" * 60)
    print("  THPT Grade Manager - Database Seeding Tool")
    print("=" * 60)
    print("\nOptions:")
    print("1. Clear all data and seed with fresh sample data")
    print("2. Initialize database (if not exists) and seed data")
    print("3. Only seed data to existing database")
    print("4. Exit")
    print()
    
    choice = input("Choose option (1-4): ").strip()
    
    if choice == "1":
        print("\n⚠ Warning: This will delete all existing data!")
        confirm = input("Are you sure? (yes/no): ").strip().lower()
        if confirm in ['yes', 'y']:
            print("\n🔄 Clearing database...")
            clear_database()
            print("🔧 Initializing database...")
            init_database()
            print("🌱 Seeding sample data...")
            seed_database()
            print("\n✅ Done!")
        else:
            print("❌ Cancelled.")
    
    elif choice == "2":
        print("\n🔧 Initializing database...")
        init_database()
        print("🌱 Seeding sample data...")
        seed_database()
        print("\n✅ Done!")
    
    elif choice == "3":
        print("\n🌱 Seeding sample data...")
        try:
            seed_database()
            print("\n✅ Done!")
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    elif choice == "4":
        print("Exiting...")
        sys.exit(0)
    
    else:
        print("Invalid option!")
        sys.exit(1)


if __name__ == "__main__":
    main()
