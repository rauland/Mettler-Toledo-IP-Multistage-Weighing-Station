pyinstaller --onefile --noconsole --icon=icon.ico main.pyw 

# PSMSI
New-Installer -ProductName "WeighBridge Scale" -UpgradeCode '1f72da53-3058-4b30-98de-99b4e0cf1ea0' -Content {
    New-InstallerDirectory -PredefinedDirectory "ProgramFilesFolder"  -Content {
       New-InstallerDirectory -DirectoryName "WeighBridge Scale" -Content {
          New-InstallerFile -Source .\dist\config.ini
          New-InstallerFile -Source .\dist\main.exe -id main
       }
    }
    New-InstallerDirectory -PredefinedDirectoryName DesktopFolder -Content {
        New-InstallerShortcut -Name 'WeightBridge Scale' -FileId 'main' -WorkingDirectoryId 'MyDir'
    }
 } -OutputDirectory (Join-Path $PSScriptRoot "output") -RequiresElevation