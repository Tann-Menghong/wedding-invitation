---
title: Wedding Invitation
emoji: 💍
colorFrom: pink
colorTo: yellow
sdk: docker
python_version: "3.10"
pinned: false
---

# 💍 Khmer Wedding Invitation

A beautiful Khmer-style wedding invitation website with admin panel.

## Features

- 🎨 Soft pink & white floral design with gold and dark green accents
- 🇰🇭 Full Khmer script support (Moul & Hanuman fonts)
- 🌐 Bilingual: Khmer (ខ្មែរ) & English toggle
- 📱 Mobile-first responsive design
- 🎵 Background music with toggle
- ⏰ Live countdown timer
- 📸 Photo gallery with masonry layout
- 💬 Guestbook for congratulations messages
- 💰 KHQR gift codes (USD/KHR)
- 🗺️ Venue with Google Maps link
- 🔐 Admin panel for content management

## Admin Panel

Access the admin panel at `/admin`

Default password: `wedding2025`

Set your own password via the `ADMIN_PASSWORD` environment variable in Hugging Face Spaces settings.

### Admin Features

- Upload/delete hero background photo
- Upload/delete gallery photos
- Edit all text content (couple names, dates, venue, parents, invitation text)
- Upload KHQR QR codes (USD and KHR)
- Manage wedding schedule/ceremonies
- View and delete guestbook messages

## Deployment to Hugging Face Spaces

1. Create a new Space on Hugging Face
2. Select **Docker** SDK
3. Upload all files
4. Set `ADMIN_PASSWORD` in Space secrets
5. Your wedding site is live!

## Local Development

```bash
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:7860` for the wedding site and `http://localhost:7860/admin` for the admin panel.

## File Structure

```
app.py                  # FastAPI backend
templates/
  index.html            # Wedding homepage
  admin.html            # Admin dashboard
static/
  css/style.css         # Styles
  js/main.js            # Frontend logic
  uploads/              # User-uploaded photos
data/
  content.json          # All editable content
  messages.json         # Guestbook entries
  gallery.json          # Gallery photos
requirements.txt
Dockerfile
```
