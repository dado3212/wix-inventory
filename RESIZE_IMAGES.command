#!/bin/bash
cd "$(dirname "$0")"

# Directory containing images
image_dir="images"

# Max size in bytes (8MB in decimal)
max_size=$((8 * 1000000))

# Loop over each file in the images directory
for image in "$image_dir"/*; do
  if [[ -f $image ]]; then
    # Get the file size in bytes
    size=$(stat -f%z "$image")
    
    # Check if the image size exceeds the max allowed size
    if [[ $size -le $max_size ]]; then
      echo "$(basename "$image") - OK (size: $(echo "scale=2; $size / 1000000" | bc) MB)"
    else
      # Calculate the proportional resize percentage
      resize_factor=$(echo "scale=2; $max_size / $size" | bc)
      echo "$(basename "$image") is over 8MB at $(echo "scale=2; $size / 1000000" | bc) MB. Scale down to $(echo "($resize_factor * 100 + 0.5)/1" | bc)%."

      # Resize the image using the calculated resize factor
      magick "$image" -resize $(echo "$resize_factor * 100" | bc)% "$image"

      # Verify the new file size
      new_size=$(stat -f%z "$image")
      new_size_mb=$(echo "scale=2; $new_size / 1000000" | bc)
      
      if [[ $new_size -le $max_size ]]; then
        echo "$(basename "$image") - Resized to under 8 MB (final size: ${new_size_mb} MB)"
      else
        echo "$(basename "$image") - Scaled down to ${new_size_mb} MB, attempting further compression..."
        
        # Compress the image further to fit under 8 MB
        magick "$image" -quality 85 "$image"

        # Check again
        final_size=$(stat -f%z "$image")
        final_size_mb=$(echo "scale=2; $final_size / 1000000" | bc)
        echo "$(basename "$image") - Final size after compression: ${final_size_mb} MB"
      fi
    fi
  fi
done

