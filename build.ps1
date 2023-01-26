pyinstaller --onefile --name="WeighBridgeScale"  --noconsole --icon=icon.ico main.pyw  

# PSMSI
New-Installer -ProductName "WeighBridgeScale" -UpgradeCode '1f72da53-3058-4b30-98de-99b4e0cf1ea0' -Content {
    New-InstallerDirectory -PredefinedDirectory "ProgramFilesFolder" -Content {
       New-InstallerDirectory -DirectoryName "WeighBridgeScale" -Id "WeighBridgeScale" -Content {
          New-InstallerFile -Source .\dist\WeighBridgeScale.exe -id main
       }
    }
    New-InstallerDirectory -PredefinedDirectoryName DesktopFolder -Content {
        New-InstallerShortcut -Name 'Weigh Bridge Scale' -FileId 'main' -WorkingDirectoryId 'WeighBridgeScale'
    }
 } -OutputDirectory (Join-Path $PSScriptRoot "output") -RequiresElevation -Version 1.1