# HOPER (Holistic Protein Representation)

**🚧️ Currently under construction! 🚧️**
We are streamlining this repository for better automation! Please be patient with us.

## Overview

![[Figures/figure_.jpg]]

- Holistic protein representation uses  multimodal learning model to predict protein functions even with low-data.

- Representation vectors created using protein sequence, protein text and protein-protein interaction data types to achieve this goal.

- The rationale behind  incorporating protein-protein interactions into our holistic protein representation model is the assumption that interacting proteins are likely to act in the same biological process. Also, these proteins are probably located at the same location in the cell.

- Text-based protein representations calculated with pre-trained natural language processing models.

- We aim to increase low-data prediction performance by using these three data types together.

## Installation Prerequisites

- You must have [Anaconda](https://www.anaconda.com/download) or [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/miniconda-other-installer-links.html) installed on your system.

## HOPER Instalation Instructions

1. Clone HOPER repository

    ```shell
    git clone https://github.com/serbulent/HOPER.git
    ```

1. Change directory to HOPER

    ```shell
    cd HOPER
    ```

1. Create an environment variable to point to the HOPER directory

    ```shell
    export HOPER_BASE=$(pwd) 
    ```

   This variable will be used in the following steps.

1. create the necessary environment with:

      ```shell
      sh create_env.sh
      ```

1. For the models to work, data, models files and uniprot_sprot.xml.gz files for uniprot preprocessing must be downloaded from the links below. The downloaded files should be placed in the HOPER folder in specific places. These will be indicated in the following steps. For now, you can download the files from the links below and place them in the HOPER folder

    - [Data files](https://drive.google.com/drive/folders/1tZ6Q60tQVaabEqUoBIu3CBiDa92Od3Nn?usp=drive_link)
  
    - [Model files](https://drive.google.com/drive/folders/1s5L2tlLjBurVGfE7GfXLhdjFYnQEEXqs?usp=drive_link)
  
    - [Uniprot preprocessing data](https://drive.google.com/file/d/1fOu7cWX9f-B-Ro41VvLGgG8eyGhV8IwD/view?usp=drive_link)

## PPI Model Installation Instructions

1. Install [GEM](https://github.com/palash1992/GEM) packages to use for Node2vec and HOPER in your ppi_representations directory, use:

   - You need to use GEM commit `213189b` for full reproducibility. To do this, you can use the following commands:
  
        ```shell
        cd $HOPER_BASE/ppi_representations
        git clone https://github.com/palash1992/GEM.git GEM 
        cd GEM   
        git checkout 213189b
        cd $HOPER_BASE/ppi_representations
        ```

   - Build Node2vec:
     - Clone the repository:

        ```shell
        git clone https://github.com/snap-stanford/snap $HOPER_BASE/ppi_representations/snap
        ```

   - Compile SNAP. This is done as follows:
  
        ```shell
        cd snap/
        rm -rf examples/Release
        make all
        cd examples/node2vec
        chmod +x node2vec
        ```

- Make `node2vec` executable and add to your *path* or move it to the location you run. ==<-- FIXME: according to final directory layout==

  - You can make protein names using edgelist_code.py.
  - These names will be needed later for the `node2vec.py` and `HOPE.py` files. Do not forget the location information. ==<- FIXME: We can't have the user remembering stuff for us!!==

## Text Model Installation Instructions

- Move the `uniprot` and `pubmed` directories you downloaded before from Google Drive to:

    ```shell
    $HOPER_BASE/text_representations/representation_generation/data/
    ```

- biosentvec and biowordvec models must be downloaded to `$HOPER_BASE/text_representations/representation_generation/models` You can set the ==`model_download` parameter in `$HOPER_BASE/Hoper_representation_generetor.yaml` to "y" to download models automatically if the biosentvec or biowordvec representations are selected for generation. Alternatively, you can download them beforehand:

  - To download BioSentVec:

    ```shell
    cd $HOPER_BASE/text_representations/representation_generation/models
    curl https://ftp.ncbi.nlm.nih.gov/pub/lu/Suppl/BioSentVec/BioSentVec_PubMed_MIMICIII-bigram_d700.bin > BioSentVec_PubMed_MIMICIII-bigram_d700.bin
    ```

  - To download BioWordVec:

    ```shell
    cd $HOPER_BASE/text_representations/representation_generation/models
    curl https://ftp.ncbi.nlm.nih.gov/pub/lu/Suppl/BioSentVec/BioWordVec_PubMed_MIMICIII_d200.bin > BioWordVec_PubMed_MIMICIII_d200.bin
    ```

## How to run HOPER

Run module main function after editing  the configuration file Hoper.yaml as below examples as;

```shell
python3 Hoper_representation_generetor_main.py 
```

- Run HOPER to produce Text Representation Preprocessing [readme.md](https://github.com/serbulent/HOPER/tree/main/text_representations/preprocess)
  
```text
  choice_of_module: [Preprocessing] # Module selection PPI,Preprocessing,SimpleAe
 #********************Preprocessing Module********************************
    module_name: Preprocessing
    uniprot_dir: ./uniprot_sprot.xml.gz 
```

- Run HOPER to produce text representation example for more information please read
[readme.md](https://github.com/serbulent/HOPER/blob/main/text_representations/representation_generation/README.md)

```yaml
 parameters:
     module_name: text
    choice_of_process:  [generate,visualize]
    generate_module:
        choice_of_representation_type:  [all]
        uniprot_files_path:  [./text_representations/representation_generation/data/uniprot/]
        pubmed_files_path:  [./text_representations/representation_generation/data/pubmed/]
        model_download: y
    visualize_module:
        choice_of_visualization_type:  [a]
        result_files_path:  [./data/text_representations/result_visualization/result_files/results/]
```

- Run HOPER to produce PPI representation example for more information please read
[readme.md](https://github.com/serbulent/HOPER/blob/main/ppi_representations/readme.md)

```yaml
parameters:
    choice_of_module: [PPI] # Module selection PPI,Preprocessing,case_study
    #*************************************MODULES********************************************************************
    #********************PPI Module********************************
    module_name: PPI
    choice_of_representation_name:  [Node2vec,HOPE]
    interaction_data_path:  [./data/hoper_PPI/PPI_example_data/example.edgelist]
    protein_id_list:  [./data/hoper_PPI/PPI_example_data/proteins_id.csv]
    node2vec_module:
        parameter_selection:
            d:  [10]  
            p: [0.25]
            q:  [0.25]
    HOPE_module:
        parameter_selection:
            d:  [5]
            beta:  [0.00390625]
```

- Run HOPER to produce SimpleAE example
  
```yaml
parameters:
    choice_of_module: [SimpleAe] # Module selection PPI,Preprocessing,SimpleAe
#*******************SimpleAe*********************************************
    module_name: SimpleAe #Protein sequence based protein representation 
    representation_path: ./case_study/case_study_results/modal_rep_ae_node2vec_binary_fused_representations_dataframe_multi_col.csv
```

- Run HOPER to produce MultiModalAE example

- Run HOPER to produce TransferAE example

## Reproducible run of paper

```shell
python case_study_main.py
```

- Run case_study_main.py for making immun escape prediction for more information please read
[readme.md](https://github.com/serbulent/HOPER/blob/main/case_study/readme.md)

```yaml
parameters:
    choice_of_module: [case_study] 
    #********************case_study Module********************************
    module_name: case_study
    choice_of_task_name:  [fuse_representations] #prepare_datasets,fuse_representations,model_training_test,prediction
    fuse_representations:
        representation_files: [./data/representation_files/node2vec_d_50_p_0.5_q_0.25_multi_col.csv,./data/hoper_case_study_example_data/representation_files/multi_modal_rep_ae_multi_col_256.csv]
        min_fold_number:  2
        representation_names:  [modal_rep_ae,node2vec]        
    prepare_datasets:  
        positive_sample_data:  ["./data/hoper_case_study_example_data/prepare_datasets/positive.csv"]
        negative_sample_data:  ["./data/hoper_case_study_example_data/prepare_datasets/neg_data.csv"]
        prepared_representation_file:  [./data/hoper_case_study_example_data/representation_files/node2vec_d_50_p_0.5_q_0.25_multi_col.csv] 
        representation_names:  [modal_rep_ae] 
    
    model_training_test:
        representation_names:  [modal_rep_ae]
        scoring_function:  ["f_max"]  #"f1_micro",f1_macro","f1_weighted"
        prepared_path:  ["./case_study/case_study_results/modal_rep_ae_node2vec_binary_data.pickle"]
        classifier_name:  ["Fully_Connected_Neural_Network"] 
   
    prediction:
        representation_names:  [modal_rep_ae]
        prepared_path:  ["./data/hoper_case_study_example_data/prediction_example_data/rep_dif_ae.csv"]
        classifier_name:  ['Fully_Connected_Neural_Network']         
        model_directory:  ["./case_study/case_study_results/training/m_o_d_a_l___r_e_p___a_e___n_o_d_e_2_v_e_c_Fully_Connected_Neural_Network_binary_classifier.pt"] 
```
