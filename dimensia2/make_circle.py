from PIL import Image, ImageOps, ImageDraw

def crop_to_circle(image_path, output_path):
    try:
        # Open the image
        img = Image.open(image_path).convert("RGBA")
        
        # Create a circular mask
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + img.size, fill=255)
        
        # Apply the mask to the image
        output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        
        # Save the result
        output.save(output_path)
        print(f"✅ Success! Saved circular image as: {output_path}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

# Run the function on your specific file
# Make sure 1.png is inside the 'static' folder
crop_to_circle("static/1.png", "static/1_circle.png")