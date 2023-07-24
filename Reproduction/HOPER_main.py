import yaml
#from gem.embedding.node2vec import node2vec
from ppi_representations import Node2vec
from ppi_representations import HOPE
import pandas as pd
import os
import glob
import tqdm
from case_study.bin.Preprocess import Binary_DataSetPreprocess
from case_study.bin.Preprocess import RepresentationFusion
from case_study.bin.Function_Prediction import BinaryTrainandTestModelsWithHyperParameterOptimization
from sklearn.utils import shuffle
import os
import pickle
from case_study.bin.Function_Prediction import binary_prediction
from case_study.bin.Function_Prediction import binary_Test_score_calculator
import imghdr
from case_study.bin.Function_Prediction import ModelParameterClass as Model_parameter
import sys


# upload yaml file
path = os.getcwd()
sys.path.append(path + "/case_study/bin/")
stream = open(path + "/Hoper.yaml", "r")
data = yaml.safe_load(stream)
module_name=data["parameters"]["module_name"]
edge_f=data["parameters"]["interaction_data_path"][0]
protein_id=pd.read_csv(data["parameters"]["protein_id_list"][0])
node2vec_parameters=data["parameters"]["node2vec_module"]["parameter_selection"]
isDirected =False
if "PPI" in data["parameters"]["choice_of_module"] :

  os.system("conda env create -f /media/DATA2/sinem/hoper_config/HOPER/Reproduction/ppi_representations/ppi_environment.yml")
  if "Node2vec" in data["parameters"]["choice_of_representation_name"]:
    Node2vec.node2vec_repesentation_call(edge_f,protein_id,isDirected,node2vec_parameters["d"],node2vec_parameters["p"],node2vec_parameters["q"])
  if "HOPE" in  data["parameters"]["choice_of_representation_name"]:
    HOPE.hope_repesentation_call(edge_f,protein_id,isDirected,data["parameters"]["HOPE_module"]["parameter_selection"]["d"],data["parameters"]["HOPE_module"]["parameter_selection"]["beta"])

if "case_study" in data["parameters"]["choice_of_module"]:
  os.system("conda env create -f /media/DATA2/sinem/hoper_config/HOPER/Reproduction/case_study/case_study_env.yml")
  datapreprocessed_lst = []
# check if results file exist
  
  if "case_study_results" not in os.listdir(path + "/case_study/"):
    os.makedirs(path+ "/case_study/" + "/case_study_results", exist_ok=True)
  #breakpoint()
  parameter_class_obj=Model_parameter.ModelParameterClass(data["parameters"]["choice_of_task_name"],
    data["parameters"]["fuse_representations"],data["parameters"]["prepare_datasets"],
    data["parameters"]["model_training_test"],data["parameters"]["prediction"])

    
  if "fuse_representations" in parameter_class_obj.choice_of_task_name:
    
    representation_dataframe=parameter_class_obj.make_fuse_representation()

  representation_names_list = parameter_class_obj.fuse_representations[
                "representation_names"
            ]
  representation_names = "_".join([str(representation) for representation in representation_names_list])


  if "prepare_datasets" in parameter_class_obj.choice_of_task_name and "fuse_representations" in parameter_class_obj.choice_of_task_name:
    
    positive_sample_dataframe = pd.read_csv(parameter_class_obj.prepare_datasets["positive_sample_data"][0]
            
        )
    negative_sample_dataframe = pd.read_csv(parameter_class_obj.prepare_datasets["negative_sample_data"][0]
            
        )
    negative_sample_dataframe["Label"] = [0] * len(negative_sample_dataframe)
    positive_sample_dataframe["Label"] = [1] * len(positive_sample_dataframe)
    sample_dataframe = negative_sample_dataframe.append(
            positive_sample_dataframe, ignore_index=True
        )
     
    datapreprocessed_lst.append(
            Binary_DataSetPreprocess.integrate_go_lables_and_representations_for_binary(
                shuffle(sample_dataframe), pd.DataFrame(representation_dataframe), representation_names
            )
        )
   
   
  elif("prepare_datasets" in parameter_class_obj.choice_of_task_name):
    prepared_representation_file_path =parameter_class_obj.prepare_datasets["prepared_representation_file"][0]
    representation_dataframe = pd.read_csv(prepared_representation_file_path)
    representation_names_list = parameter_class_obj.prepare_datasets[
            "representation_names"
    ]
    if len(parameter_class_obj.prepare_datasets["representation_names"]) > 1:
      representation_names = "_".join(representation_names_list)
    else:
      representation_names = parameter_class_obj.prepare_datasets[
                "representation_names"
            ][0]
    positive_sample_dataframe = pd.read_csv(
    parameter_class_obj.prepare_datasets["positive_sample_data"][0]
        )
    negative_sample_dataframe = pd.read_csv(
            parameter_class_obj.prepare_datasets["negative_sample_data"][0]
        )
    negative_sample_dataframe["Label"] = [0] * len(negative_sample_dataframe)
    positive_sample_dataframe["Label"] = [1] * len(positive_sample_dataframe)
    sample_dataframe = negative_sample_dataframe.append(
    positive_sample_dataframe, ignore_index=True
        )
        
    datapreprocessed_lst.append(
            Binary_DataSetPreprocess.integrate_go_lables_and_representations_for_binary(
                shuffle(sample_dataframe), representation_dataframe, representation_names
            )
        )


  if "model_training_test" in parameter_class_obj.choice_of_task_name:
    breakpoint()
    scoring_func =  parameter_class_obj.model_training_test["scoring_function"]
    
    if "prepare_datasets" in parameter_class_obj.choice_of_task_name:
      for data_preproceed in datapreprocessed_lst:
            
        best_param = BinaryTrainandTestModelsWithHyperParameterOptimization.select_best_model_with_hyperparameter_tuning(
                representation_names,
                data_preproceed,
                scoring_func,
                parameter_class_obj.model_training_test["classifier_name"],
            )

    else:
        
      preprocesed_data_path = parameter_class_obj.model_training_test["prepared_path"]
      representation_names_list = parameter_class_obj.prepare_datasets[
            "representation_names"
        ]
      representation_names = "_".join(representation_names_list)
      for data_preproceed in preprocesed_data_path:
        data_preproceed_pickle = open(data_preproceed, "rb")
        data_preproceed_df = pickle.load(data_preproceed_pickle)
        best_param = BinaryTrainandTestModelsWithHyperParameterOptimization.select_best_model_with_hyperparameter_tuning(
                parameter_class_obj.model_training_test["representation_names"],
                data_preproceed_df[0],
                scoring_func,
                parameter_class_obj.model_training_test["classifier_name"],
        )


  if "prediction" in parameter_class_obj.choice_of_task_name:
    for i in parameter_class_obj.prediction["prepared_path"]:
      test_data = pd.read_csv(i)
      classifier_name_lst = parameter_class_obj.prediction["classifier_name"]
      binary_prediction.make_prediction(
            parameter_class_obj.prediction["representation_names"][0],
            test_data,
            parameter_class_obj.prediction["model_directory"],
            classifier_name_lst,
      )
if "Preprocessing" in data["parameters"]["choice_of_module"] :
  os.system("conda env create -f /media/DATA2/sinem/hoper_config/HOPER/Reproduction/text_representations/preprocess/preprocess.yml")
  os.system('python /media/DATA2/sinem/hoper_config/HOPER/Reproduction/text_representations/preprocess/preprocess_main.py')