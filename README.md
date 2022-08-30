# Exploring the use of GAN-based anomaly detection in prolonging independent living for the ageing population

Exploring the use of GAN-based anomaly detection in prolonging independent living for the ageing population

Supporting Repository for Individual Project in Partial Fulfilment of the requirements for the MSc degree in Computing

Author
Gen Hall
Imperial College London

Supervisors
Knottenbelt, William (wjk)
Uchyigit, Gulden

Department
Computing

Abstract
Context
This research proposal contributes towards developing applications in the area of IoT for smart homes to prolong independent living for the aging population. Specifically, it explores the use of GAN-based anomaly detection algorithms to detect anomalies within Activities of Daily Living (ADL). In doing so, it tests and evaluates the TadGAN model designed by Geiger et. al [1] on datasets HH101 and 120 from the the CASAS repository.

Anomaly detection, aka outlier detection or novelty detection, refers to finding patterns in data that do not conform to expected behaviour. Anomaly detection is popular in domains such as fraud detection, network intrusion, image processing etc. In recent years, anomaly detection has been popular for smart home technology to prolong independent living and enhance quality of life in the aging population by identifying opportune moments for healthcare interventions.

Data Sets
The experiments will be carried out using publicly available CASAS datasets, available from the Centre for Advanced Adaptive Systems, Washington State University. These datasets contain the Active Daily Living (ADL) of both individual and group occupants. Activities included include sleeping eating, bathing, dressing, toileting etc.

source for [1] (bibtex):

@inproceedings{geiger2020tadgan,
  title={TadGAN: Time Series Anomaly Detection Using Generative Adversarial Networks},
  author={Geiger, Alexander and Liu, Dongyu and Alnegheimish, Sarah and Cuesta-Infante, Alfredo and Veeramachaneni, Kalyan},
  booktitle={2020 IEEE International Conference on Big Data (IEEE BigData)},
  organization={IEEE},
  year={2020}
}

Setup:

1. Build a virtual environment using a compatible version of python for orion-ml (<v3.8)
2. pip install requirements.txt
