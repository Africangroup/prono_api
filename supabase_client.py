from supabase import create_client
import os

SUPABASE_URL = os.getenv("https://fhppvlhsdwshrpaexueg.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZocHB2bGhzZHdzaHJwYWV4dWVnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzAyMzAzMTMsImV4cCI6MjA4NTgwNjMxM30.LN8kaedkabeP5lROrIs5NOJsjXWIm4EyiAI4Vn4Vo9k")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
