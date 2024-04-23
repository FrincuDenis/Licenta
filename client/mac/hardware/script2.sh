#!/bin/bash

# Function to check if a disk is SSD
is_ssd() {
    diskutil info "$1" | grep -q 'Solid State'
    return $?
}

# Get list of disks
disks=$(diskutil list | grep '/dev/' | awk '{print $1}')

# Loop through each disk
for disk in $disks; do
    # Check if the disk is an SSD
    if is_ssd "$disk"; then
        echo "$disk is an SSD."
    else
        # Display additional information for HDDs
        echo "$disk is an HDD."
        echo "Device Type: $(diskutil info "$disk" | grep 'Device / Media Type' | awk -F ': ' '{print $2}')"
        echo "Size: $(diskutil info "$disk" | grep 'Total Size' | awk -F ': ' '{print $2}')"
        echo "Partition Map Type: $(diskutil info "$disk" | grep 'Partition Map Scheme' | awk -F ': ' '{print $2}')"
        # Add more properties as needed
    fi
done
