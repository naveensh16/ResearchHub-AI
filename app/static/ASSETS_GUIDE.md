# Static Assets Guide

## Required Files for Production

### Favicon Files
Generate these using https://realfavicongenerator.net/ or https://favicon.io/

1. **favicon.ico** (16x16, 32x32, 48x48 multi-size)
   - Location: `app/static/favicon.ico`
   - Used by: Most browsers in tab/bookmark

2. **apple-touch-icon.png** (180x180)
   - Location: `app/static/img/apple-touch-icon.png`
   - Used by: iOS Safari when adding to home screen

3. **favicon-32x32.png** (32x32)
   - Location: `app/static/img/favicon-32x32.png`
   - Used by: Modern browsers

4. **favicon-16x16.png** (16x16)
   - Location: `app/static/img/favicon-16x16.png`
   - Used by: Legacy browsers

### Open Graph Images
Generate with Canva or Figma (template size: 1200x630 for best compatibility)

5. **og-image.png** (1200x630)
   - Location: `app/static/img/og-image.png`
   - Used by: Facebook, LinkedIn, Slack link previews
   - Content: "ResearchHub AI" logo + tagline + gradient background
   - Design tips:
     - Keep text readable (min 40px font)
     - Safe zone: 20% padding from edges
     - Brand colors: #667eea (indigo) to #764ba2 (purple gradient)

6. **twitter-card.png** (1200x600)
   - Location: `app/static/img/twitter-card.png`
   - Used by: Twitter/X link previews
   - Similar design to og-image but slightly different aspect ratio

### Loading/Placeholder Images

7. **logo.svg** (vector)
   - Location: `app/static/img/logo.svg`
   - ResearchHub AI logo (flask icon + text)

8. **placeholder-avatar.png** (200x200)
   - Location: `app/static/img/placeholder-avatar.png`
   - Generic avatar for users without profile pictures

9. **loading-spinner.svg** (animated)
   - Location: `app/static/img/loading-spinner.svg`
   - Used during API calls

## Quick Generation Commands

### Using Python PIL (Pillow)
```bash
pip install Pillow
python -c "
from PIL import Image, ImageDraw, ImageFont
import os

# Create gradient background function
def create_gradient(width, height):
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    for i in range(height):
        ratio = i / height
        r = int(102 + (118 - 102) * ratio)  # 667eea to 764ba2
        g = int(126 + (75 - 126) * ratio)
        b = int(234 + (162 - 234) * ratio)
        draw.rectangle([(0, i), (width, i+1)], fill=(r, g, b))
    return img

# OG Image
og = create_gradient(1200, 630)
draw = ImageDraw.Draw(og)
font = ImageFont.truetype('arial.ttf', 80)
draw.text((100, 250), 'ResearchHub AI', fill='white', font=font)
font_small = ImageFont.truetype('arial.ttf', 40)
draw.text((100, 360), 'AI-Powered Research Collaboration', fill='white', font=font_small)
og.save('app/static/img/og-image.png')

# Twitter Card
twitter = og.resize((1200, 600))
twitter.save('app/static/img/twitter-card.png')

# Apple Touch Icon
icon = create_gradient(180, 180)
draw = ImageDraw.Draw(icon)
font = ImageFont.truetype('arial.ttf', 60)
draw.text((30, 60), '🧪', font=font)
icon.save('app/static/img/apple-touch-icon.png')

# Favicons
icon.resize((32, 32)).save('app/static/img/favicon-32x32.png')
icon.resize((16, 16)).save('app/static/img/favicon-16x16.png')

# Placeholder Avatar
avatar = Image.new('RGB', (200, 200), '#e5e7eb')
draw = ImageDraw.Draw(avatar)
draw.ellipse([50, 50, 150, 150], fill='#9ca3af')
draw.ellipse([75, 120, 125, 200], fill='#9ca3af')
avatar.save('app/static/img/placeholder-avatar.png')

print('✅ All images created!')
"
```

### Using Online Tools (Recommended)
1. **Favicon**: https://favicon.io/favicon-generator/
   - Text: "RH"
   - Background: Gradient (#667eea to #764ba2)
   - Font: Roboto Bold
   - Download ZIP and extract to `app/static/`

2. **OG Image**: https://www.canva.com/
   - Template: "Facebook Post" (1200x630)
   - Design with ResearchHub AI branding
   - Export as PNG

3. **Logo**: https://www.canva.com/
   - Template: "Logo" (500x500)
   - Add flask emoji 🧪 + "ResearchHub AI" text
   - Export as SVG

## CSS for Loading Spinner

Create `app/static/css/spinner.css`:
```css
.spinner {
    border: 4px solid rgba(102, 126, 234, 0.1);
    border-top: 4px solid #667eea;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
```

## Update base.html to use new assets

Already updated in base.html with:
```html
<link rel="icon" type="image/x-icon" href="{{ url_for('static', filename='favicon.ico') }}">
<link rel="apple-touch-icon" sizes="180x180" href="{{ url_for('static', filename='img/apple-touch-icon.png') }}">
```

## Verification Checklist
- [ ] favicon.ico appears in browser tab
- [ ] Apple touch icon shows when saving to iOS home screen
- [ ] OG image displays in Facebook link preview (test: https://developers.facebook.com/tools/debug/)
- [ ] Twitter card shows correctly (test: https://cards-dev.twitter.com/validator)
- [ ] All images load without 404 errors
- [ ] Placeholder avatar displays for users without profile pics

## Production Optimization
```bash
# Compress images (70% quality is usually fine)
pip install Pillow
python -c "
from PIL import Image
for img in ['og-image.png', 'twitter-card.png']:
    im = Image.open(f'app/static/img/{img}')
    im.save(f'app/static/img/{img}', optimize=True, quality=70)
print('✅ Images optimized')
"
```

## Fallback if generation fails
Download placeholder images from:
- Favicon: https://via.placeholder.com/32
- OG Image: https://via.placeholder.com/1200x630/667eea/ffffff?text=ResearchHub+AI
- Avatar: https://via.placeholder.com/200/9ca3af/ffffff?text=?
