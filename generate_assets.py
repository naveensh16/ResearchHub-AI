"""
ResearchHub AI - Static Assets Generator
Generates favicon, og-image, twitter-card, and placeholder images
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_gradient(width, height, color1=(102, 126, 234), color2=(118, 75, 162)):
    """Create a gradient image"""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    for i in range(height):
        ratio = i / height
        r = int(color1[0] + (color2[0] - color1[0]) * ratio)
        g = int(color1[1] + (color2[1] - color1[1]) * ratio)
        b = int(color1[2] + (color2[2] - color1[2]) * ratio)
        draw.rectangle([(0, i), (width, i+1)], fill=(r, g, b))
    
    return img

def create_og_image():
    """Create Open Graph image (1200x630)"""
    print("📸 Creating Open Graph image...")
    img = create_gradient(1200, 630)
    draw = ImageDraw.Draw(img)
    
    # Try to use a nice font, fallback to default
    try:
        title_font = ImageFont.truetype("arial.ttf", 80)
        subtitle_font = ImageFont.truetype("arial.ttf", 40)
    except:
        print("⚠️  Arial font not found, using default")
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # Add text (using white tuple instead of rgba)
    draw.text((100, 220), "🧪 ResearchHub AI", fill='white', font=title_font)
    draw.text((100, 340), "AI-Powered Research Collaboration", fill='white', font=subtitle_font)
    draw.text((100, 420), "Connect · Collaborate · Create", fill=(255, 255, 255), font=subtitle_font)
    
    img.save('app/static/img/og-image.png', optimize=True, quality=85)
    print("✅ og-image.png created")

def create_twitter_card():
    """Create Twitter Card image (1200x600)"""
    print("🐦 Creating Twitter Card image...")
    img = create_gradient(1200, 600)
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("arial.ttf", 80)
        subtitle_font = ImageFont.truetype("arial.ttf", 40)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    draw.text((100, 200), "🧪 ResearchHub AI", fill='white', font=title_font)
    draw.text((100, 320), "AI-Powered Research Collaboration", fill='white', font=subtitle_font)
    
    img.save('app/static/img/twitter-card.png', optimize=True, quality=85)
    print("✅ twitter-card.png created")

def create_favicons():
    """Create favicon files"""
    print("🖼️  Creating favicons...")
    
    # Create base icon (180x180 for Apple Touch Icon)
    icon = create_gradient(180, 180)
    draw = ImageDraw.Draw(icon)
    
    # Add flask emoji (simplified as circle with text)
    try:
        emoji_font = ImageFont.truetype("seguiemj.ttf", 100)  # Windows emoji font
    except:
        try:
            emoji_font = ImageFont.truetype("arial.ttf", 100)
        except:
            emoji_font = ImageFont.load_default()
    
    # Draw flask emoji or "RH" text
    draw.text((40, 40), "🧪", fill='white', font=emoji_font)
    
    # Save Apple Touch Icon
    icon.save('app/static/img/apple-touch-icon.png', optimize=True)
    print("✅ apple-touch-icon.png created")
    
    # Save different favicon sizes
    icon.resize((32, 32), Image.Resampling.LANCZOS).save('app/static/img/favicon-32x32.png')
    print("✅ favicon-32x32.png created")
    
    icon.resize((16, 16), Image.Resampling.LANCZOS).save('app/static/img/favicon-16x16.png')
    print("✅ favicon-16x16.png created")
    
    # Convert to ICO (multi-size)
    icon_32 = icon.resize((32, 32), Image.Resampling.LANCZOS)
    icon_16 = icon.resize((16, 16), Image.Resampling.LANCZOS)
    icon_32.save('app/static/favicon.ico', format='ICO', sizes=[(16, 16), (32, 32)])
    print("✅ favicon.ico created")

def create_placeholder_avatar():
    """Create placeholder avatar for users without profile pics"""
    print("👤 Creating placeholder avatar...")
    
    # Gray background
    avatar = Image.new('RGB', (200, 200), (229, 231, 235))
    draw = ImageDraw.Draw(avatar)
    
    # Draw generic user icon (head + shoulders)
    # Head (circle)
    draw.ellipse([60, 40, 140, 120], fill=(156, 163, 175))
    # Shoulders (ellipse)
    draw.ellipse([50, 100, 150, 180], fill=(156, 163, 175))
    
    avatar.save('app/static/img/placeholder-avatar.png', optimize=True)
    print("✅ placeholder-avatar.png created")

def create_loading_spinner():
    """Create loading spinner SVG"""
    print("⏳ Creating loading spinner...")
    
    spinner_svg = '''<svg width="40" height="40" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
        </linearGradient>
    </defs>
    <circle cx="20" cy="20" r="16" stroke="rgba(102, 126, 234, 0.1)" stroke-width="4" fill="none"/>
    <circle cx="20" cy="20" r="16" stroke="url(#gradient)" stroke-width="4" fill="none" 
            stroke-dasharray="80" stroke-dashoffset="60" stroke-linecap="round">
        <animateTransform attributeName="transform" type="rotate" from="0 20 20" to="360 20 20" 
                          dur="1s" repeatCount="indefinite"/>
    </circle>
</svg>'''
    
    with open('app/static/img/loading-spinner.svg', 'w') as f:
        f.write(spinner_svg)
    
    print("✅ loading-spinner.svg created")

def create_logo_svg():
    """Create ResearchHub AI logo SVG"""
    print("🎨 Creating logo SVG...")
    
    logo_svg = '''<svg width="200" height="50" viewBox="0 0 200 50" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="logo-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
        </linearGradient>
    </defs>
    <!-- Flask Icon (as circle) -->
    <circle cx="25" cy="25" r="20" fill="url(#logo-gradient)"/>
    <text x="14" y="35" font-size="24" fill="white">R</text>
    <!-- ResearchHub AI Text -->
    <text x="55" y="32" font-family="Arial, sans-serif" font-weight="bold" font-size="24" fill="#1f2937">
        ResearchHub AI
    </text>
</svg>'''
    
    with open('app/static/img/logo.svg', 'w', encoding='utf-8') as f:
        f.write(logo_svg)
    
    print("✅ logo.svg created")

def create_css_files():
    """Create CSS files for loading states"""
    print("💅 Creating CSS files...")
    
    css_content = '''/* ResearchHub AI - Custom Styles */

/* Loading Spinner */
.spinner {
    border: 4px solid rgba(102, 126, 234, 0.1);
    border-top: 4px solid #667eea;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin: 20px auto;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Gradient button */
.btn-gradient {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    transition: transform 0.2s;
}

.btn-gradient:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

/* Loading overlay */
.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
}

/* Fade in animation */
.fade-in {
    animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Avatar styles */
.avatar {
    border-radius: 50%;
    object-fit: cover;
}

.avatar-sm { width: 32px; height: 32px; }
.avatar-md { width: 48px; height: 48px; }
.avatar-lg { width: 64px; height: 64px; }
.avatar-xl { width: 128px; height: 128px; }
'''
    
    os.makedirs('app/static/css', exist_ok=True)
    with open('app/static/css/custom.css', 'w') as f:
        f.write(css_content)
    
    print("✅ custom.css created")

def main():
    """Generate all static assets"""
    print("🚀 ResearchHub AI - Static Assets Generator\n")
    
    # Create directories if they don't exist
    os.makedirs('app/static/img', exist_ok=True)
    
    try:
        create_og_image()
        create_twitter_card()
        create_favicons()
        create_placeholder_avatar()
        create_loading_spinner()
        create_logo_svg()
        create_css_files()
        
        print("\n✅ All assets generated successfully!")
        print("\n📁 Files created:")
        print("   - app/static/favicon.ico")
        print("   - app/static/img/og-image.png")
        print("   - app/static/img/twitter-card.png")
        print("   - app/static/img/apple-touch-icon.png")
        print("   - app/static/img/favicon-32x32.png")
        print("   - app/static/img/favicon-16x16.png")
        print("   - app/static/img/placeholder-avatar.png")
        print("   - app/static/img/loading-spinner.svg")
        print("   - app/static/img/logo.svg")
        print("   - app/static/css/custom.css")
        
        print("\n🔧 Next steps:")
        print("   1. Test favicon in browser (clear cache if needed)")
        print("   2. Validate OG image: https://developers.facebook.com/tools/debug/")
        print("   3. Validate Twitter Card: https://cards-dev.twitter.com/validator")
        print("   4. Update base.html to include custom.css")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Tip: Install Pillow if not installed: pip install Pillow")

if __name__ == "__main__":
    main()
