#!/bin/bash
mkdir ./../data
curl -L -o ./../data/basic_res_cat.zip
  https://www.kaggle.com/api/v1/datasets/download/gauravduttakiit/resume-dataset
unzip ./../data/basic_res_cat.zip -d ./../data/
rm ./../data/basic_res_cat.zip

curl -L -o ./../data/resume_pdfs.zip
  https://www.kaggle.com/api/v1/datasets/download/snehaanbhawal/resume-dataset
unzip ./../data/resume_pdfs.zip -d ./../data/
rm ./../data/resume_pdfs.zip

#!/bin/bash
curl -L -o ./../data/labelled_resume.zip
  https://www.kaggle.com/api/v1/datasets/download/saugataroyarghya/resume-dataset
unzip ./../data/labelled_resume.zip -d ./../data/
rm ./../data/labelled_resume.zip