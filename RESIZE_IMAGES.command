#!/bin/bash
cd "$(dirname "$0")"

# Directory containing images
image_dir="images"

# Max size in bytes (7.5MB in decimal)
max_size=7500000

# Max dimensions in pixels (the largest FB will process)
max_pixels=16384

# Loop over each file in the images directory
for image in "$image_dir"/*; do
  if [[ -f $image ]]; then
    # Get width and height
    width=$(magick identify -format "%w" "$image")
    height=$(magick identify -format "%h" "$image")

    # Check and resize if needed
    if (( width > max_pixels || height > max_pixels )); then
      echo "Resizing $(basename "$image") to max ${max_pixels}x${max_pixels}..."
      magick "$image" -scale "${max_pixels}x${max_pixels}>" "$image"
    fi

    # Get the file size in bytes
    size=$(stat -f%z "$image")
    
    # Check if the image size exceeds the max allowed size
    if [[ $size -le $max_size ]]; then
      echo "$(basename "$image") - OK (size: $(echo "scale=2; $size / 1000000" | bc) MB)"
    else
      # If it's too big, then we need it to be a jpeg to shrink it
      ext="${image##*.}"
      base_name="${image%.*}"

      # Convert to JPEG if not already in JPEG format
      if [[ $ext != "jpg" && $ext != "jpeg" ]]; then
        echo "Converting $(basename "$image") to JPEG..."
        magick "$image" "$base_name.jpg"
        image="$base_name.jpg"
      fi

      # Apply the size constraint
      echo "Compressing $(basename "$image") to fit under $max_size..."
      magick "$image" -define jpeg:extent=$max_size "$image"

      # Verify the final size
      final_size=$(stat -f%z "$image")
      final_size_mb=$(echo "scale=2; $final_size / 1000000" | bc)
      echo "$(basename "$image") - Final size: ${final_size_mb} MB"
    fi
  fi
done

