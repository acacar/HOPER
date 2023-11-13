#!/usr/bin/env bash

echo "Creating conda environments for HOPER" && \
echo "Creating conda environment for HOPER case study" && \
conda env create -f case_study/hoper_case_study_env.yml && \
echo "Creating conda environment for HOPER PPI" && \
conda env create -f ppi_representations/hoper_PPI.yml && \
echo "Creating conda environment for HOPER preprocess" && \
conda env create -f text_representations/preprocess/hoper_preprocess.yml && \
echo "Creating conda environment for HOPER text representations" && \
conda env create -f text_representations/text_representations.yml && \
echo "Creating conda environment for HOPER multimodal representations" && \
conda env create -f multimodal_representations/simple_ae_env.yml && \
echo "Done. All necessary environments have been created."