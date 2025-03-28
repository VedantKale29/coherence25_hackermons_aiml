# Create 'data' directory if it doesn't exist
$DataPath = "$PSScriptRoot\..\data"
if (!(Test-Path -Path $DataPath)) {
    New-Item -ItemType Directory -Path $DataPath | Out-Null
}

# Download basic_res_cat.zip
Invoke-WebRequest -Uri "https://www.kaggle.com/api/v1/datasets/download/gauravduttakiit/resume-dataset" -OutFile "$DataPath\basic_res_cat.zip"

# Unzip the file
Expand-Archive -Path "$DataPath\basic_res_cat.zip" -DestinationPath $DataPath -Force

# Remove the zip file
Remove-Item "$DataPath\basic_res_cat.zip"

# Download resume_pdfs.zip
Invoke-WebRequest -Uri "https://www.kaggle.com/api/v1/datasets/download/snehaanbhawal/resume-dataset" -OutFile "$DataPath\resume_pdfs.zip"

# Unzip the file
Expand-Archive -Path "$DataPath\resume_pdfs.zip" -DestinationPath $DataPath -Force

# Remove the zip file
Remove-Item "$DataPath\resume_pdfs.zip"

# Download labelled_resume.zip
Invoke-WebRequest -Uri "https://www.kaggle.com/api/v1/datasets/download/saugataroyarghya/resume-dataset" -OutFile "$DataPath\labelled_resume.zip"

# Unzip the file
Expand-Archive -Path "$DataPath\labelled_resume.zip" -DestinationPath $DataPath -Force

# Remove the zip file
Remove-Item "$DataPath\labelled_resume.zip"

Write-Output "✅ All files downloaded and extracted successfully!"
