# 7.18.1. Form factor @offset 0x0E
[string[]]$FORM_FACTORS = @(
'Invalid', 'Other', 'Unknown', 'SIMM', # 00-03h
'SIP', 'Chip', 'DIP', 'ZIP' # 04-07h
'Proprietary Card', 'DIMM', 'TSOP', 'Row of chips', # 08-0Bh
'RIMM', 'SODIMM', 'SRIMM', 'FB-DIMM', # 0C-0Fh
'Die' # 10h
)
# 7.18.2. Memory type @offset 0x12
[string[]]$MEMORY_TYPES = @(
'Invalid', 'Other', 'Unknown', 'DRAM', # 00-03h
'EDRAM', 'VRAM', 'SRAM', 'RAM', # 04-07h
'ROM', 'FLASH', 'EEPROM', 'FEPROM', # 08-0Bh
'EPROM', 'CDRAM', '3DRAM', 'SDRAM', # 0C-0Fh
'SGRAM', 'RDRAM', 'DDR', 'DDR2', # 10-13h
'DDR2 FB-DIMM', 'Reserved', 'Reserved', 'Reserved', # 14-17h
'DDR3', 'FBD2', 'DDR4', 'LPDDR', # 18-1Bh
'LPDDR2', 'LPDDR3', 'LPDDR4', 'Logical non-volatile device' # 1C-1Fh
'HBM (High Bandwidth Memory)', 'HBM2 (High Bandwidth Memory Generation 2)',
'DDR5', 'LPDDR5' # 20-23h
)
# 7.18.3. Type detail @offset 0x13
[string[]]$TYPE_DETAILS = @(
'Reserved', 'Other', 'Unknown', 'Fast-paged', # bit 0-3
'Static column', 'Pseudo-static', 'RAMBUS', 'Synchronous', # bit 4-7
'CMOS', 'EDO', 'Window DRAM', 'Cache DRAM', # bit 8-11
'Non-volatile', 'Registered (Buffered)',
'Unbuffered (Unregistered)', 'LRDIMM' # 0C-0Fh
)
$csvPath = "File.csv"  # Define the variable outside the function
# Get computer name and IP address
$computerName = $env:COMPUTERNAME
$ipAddress = (Get-WmiObject Win32_NetworkAdapterConfiguration | Where-Object { $_.IPAddress -ne $null }).IPAddress[0]

function lookUp([string[]]$table, [int]$value)
{
if ($value -ge 0 -and $value -lt $table.Length) {
$table[$value]
} else {
"Unknown value 0x{0:X}" -f $value
}
}
function parseTable([array]$table, [int]$begin, [int]$end)
{
[int]$index = $begin
$size = [BitConverter]::ToUInt16($table, $index + 0x0C)
if ($size -eq 0xFFFF) {
"Unknown memory size"
} elseif ($size -ne 0x7FFF) {
if (($size -shr 15) -eq 0) { $size *= 1MB } else { $size *= 1KB }
} else {
$size = [BitConverter]::ToUInt32($table, $index + 0x1C)
}


$formFactor = $table[$index + 0x0E]
$formFactorStr = $(lookUp $FORM_FACTORS $formFactor)

$type = $table[$index + 0x12]
$result=create_excel $formFactorStr $(lookUp $MEMORY_TYPES $type) $(($size/1GB))
return $result
}
$marCounts = @{}  # Initialize a dictionary to store value counts
function create_excel($formf, $tip, $mar) {
    $ethernetAdapter = Get-NetAdapter -Name "Ethernet"
    $wifiAdapter = Get-NetAdapter -Name "Wi-Fi"
    
    $macEthernet = $ethernetAdapter.MacAddress
    $macWifi = $wifiAdapter.MacAddress
    
    $ipAddressInfoEthernet = Get-NetIPAddress -InterfaceAlias "Ethernet" -AddressFamily IPv4
    $ipAddressInfoWifi = Get-NetIPAddress -InterfaceAlias "Wi-Fi" -AddressFamily IPv4
    
    $ipAddressEthernet = $ipAddressInfoEthernet.IPAddress
    $ipAddressWifi = $ipAddressInfoWifi.IPAddress

    # Increment the count for the current value in the dictionary
    if ($marCounts.ContainsKey($mar)) {
        $marCounts[$mar]++
    } else {
        $marCounts[$mar] = 1
    }

    $ramPartNumbersString = $formf -join ";"
    $ramMemoryTypesString = $tip

    # Get OS information
    $osInfo = Get-WmiObject Win32_OperatingSystem -ComputerName $computerName

    # Get CPU information
    $cpu = Get-WmiObject Win32_Processor -ComputerName $computerName | Select-Object -ExpandProperty Name

# Get volume information for volumes with drive letters
$volumeInfo = Get-Volume | Where-Object { $_.DriveLetter -ne $null }

$drives = Get-WmiObject Win32_DiskDrive -ComputerName $computerName

$driveModels = $drives | ForEach-Object { $_.Model }
$driveSizesGB = $volumeInfo | ForEach-Object { [math]::Round($_.Size / 1GB, 2) }
$driveFreeSpaceGB = $volumeInfo | ForEach-Object { [math]::Round($_.SizeRemaining / 1GB, 2) }

# Calculate used drive space for each drive
$usedDriveSpaceGB = @()
for ($i = 0; $i -lt $volumeInfo.Count; $i++) {
    $usedSpace = $driveSizesGB[$i] - $driveFreeSpaceGB[$i]
    $usedDriveSpaceGB += [math]::Round($usedSpace, 2)
}

# Combine drive models into a single string
$driveModelsString = $driveModels -join ";"
# Calculate total drive size
$totalDriveSizeGBString = $driveSizesGB -join ";"
$usedDriveSpaceGBString = $usedDriveSpaceGB -join ";"

    
    $formattedRAMSizeGB = $marCounts.GetEnumerator() | ForEach-Object {
    $size = $_.Key
    $count = $_.Value
    if ($size -ge 1) {
        "$count`x$size GB"
}
}
    # Join the formatted sizes and counts into a single string
    $formattedRAMSizeGB = $formattedRAMSizeGB -join " "

    # Create a single custom object to hold all the information
    $outputObject = [PSCustomObject]@{
    PCName              = $computerName
    MAC_AddressEthernet = $macEthernet
    IPAddressEthernet   = $ipAddressEthernet
    MAC_AddressWifi     = $macWifi
    IPAddressWifi       = $ipAddressWifi
    Drive               = $driveModelsString
    Drive_Size          = $totalDriveSizeGBString
    Used_Drive          = $usedDriveSpaceGBString
    RAM                 = $ramPartNumbersString
    RamType             = $ramMemoryTypesString
    RAMSizeGB           = $formattedRAMSizeGB
    CPUModel            = $cpu
    OS                  = $osInfo.Caption
}

    $jsonData = $outputObject | ConvertTo-Json

    return $jsonData
}


function start_script{
$index = 0

$END_OF_TABLES = 127
$MEMORY_DEVICE = 17

$BiosTables = (Get-WmiObject -ComputerName . -Namespace root\wmi -Query `
"SELECT SMBiosData FROM MSSmBios_RawSMBiosTables" `
).SMBiosData

do
{
$startIndex = $index

# ========= Parse table header =========
$tableType = $BiosTables[$index]
if ($tableType -eq $END_OF_TABLES) { break }

$tableLength = $BiosTables[$index + 1]
# $tableHandle = [BitConverter]::ToUInt16($BiosTables, $index + 2)
$index += $tableLength

# ========= Parse unformatted part =========
# Find the '\0\0' structure termination
while ([BitConverter]::ToUInt16($BiosTables, $index) -ne 0) { $index++ }
$index += 2

# adjustment when the table ends with a string
if ($BiosTables[$index] -eq 0) { $index++ }

if ($tableType -eq $MEMORY_DEVICE) {$result=parseTable $BiosTables $startIndex $index
    }
} until ($tableType -eq $END_OF_TABLES -or $index -ge $BiosTables.length)

return $result
}

$data=start_script

Write-Host "$data"