#!/bin/bash
cd "$(dirname "$0")"

# Directory containing images
image_dir="images"

# Max size in bytes (7.5MB in decimal)
max_size=7500000

# Max dimensions in pixels (the largest FB will process)
max_pixels=145000000
max_dim=16384

# Loop over each file in the images directory
for image in "$image_dir"/*; do
  if [[ -f $image ]]; then
    # Get width and height
    width=$(magick identify -format "%w" "$image")
    height=$(magick identify -format "%h" "$image")

    # Determine the scaling (bc -l does integer math)
    scale_by_pixels=$(echo "scale=10; sqrt($max_pixels / ($width * $height))" | bc -l)
    scale_by_width=$(echo "scale=10; $max_dim / $width" | bc -l)
    scale_by_height=$(echo "scale=10; $max_dim / $height" | bc -l)

    # Pick the smallest scale
    scale=$(echo "$scale_by_pixels $scale_by_width $scale_by_height" | awk '{s=$1; if($2<s) s=$2; if($3<s) s=$3; print s}')

    # Check and resize if needed
    if (( $(echo "$scale < 1" | bc -l) )); then
      new_width=$(printf "%.0f" $(echo "$width * $scale" | bc -l))
      new_height=$(printf "%.0f" $(echo "$height * $scale" | bc -l))
      echo "Resizing $(basename "$image") to ${new_width}x${new_height}..."
      magick "$image" -scale "${new_width}x${new_height}>" "$image"
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

