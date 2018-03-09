# Early Diagnosis of Parkinson's Disease via keystrokes
## Inspired
Parkinson's disease sickened over 6 million individuals worldwide. The impact extended to their immediate families and friends, societies, medical communities and many more resources are not negligible. <br><br>
This neurodegenerative disease is incurable but early discovery indisputably benefit the wellbeing of the patient and all involved. Diagnosis typically relies on neurologists but it is the individual patient (or close family member) who has to first discover that he or she is having the symptom of Parkinson's disease. When the well-known symptom of movement disorder becomes obvious to the patient it typically has been five to ten years since the patient has the disease. More than half of the area affected in the brain are damaged and many episodes of falls and injuries have already occurred. It is certainly more stressful to care for a patient with Parkinson's disease and physical injuries and some other form of damages like depression compare to just the disease itself.<br><br>
A cost-effective test that can be done at home with simple and familiar apparatus would be one of the best solution for early detection.<br><br>
Experiment has been conducted to use keyboard stroke as a mean to allow non-clinical personnel to make a guided diagnosis. This help captures the pre-motor phase of the disease, which could be years, or decades before the degeneration and the tell-tale symptoms of the failing motor control. <br><br>
Inspired by the study 'High-accuracy detection of early Parkinson's Disease using multiple characteristics of finger movement while typing' recorded in physionet.org, I am eager to put machine learning to work to build a great classification model so that precious opportunity to start treating or researching the disease is not lost.<br><br>
## Goal
The goal is to take in data sets provided by physionet.org for the study 'High-accuracy detection of early Parkinson's Disease using multiple characteristics of finger movement while typing' (Tappy keystroke data) and build a satisfactory binary classification model out of it. The model will be able to predict by using patient's keystroke data input if he or she has Parkinson's disease. 
<br><br>
There is another project also hosted by physio.net: neuroQWERTY MIT-CSXPD. The way keystroke data was acquired is different from the Tappy project but the difference is in the soft wares and environments set up. The data collected by neuroQWERTY have the similar attribute that Tappy project collected. The preliminary exploration has shown that they can be used together with Tappy data set thereby increasing the total volume of available data. 
## Environment of this project:
Anaconda Navigator 1.6.12<br>
Python 3.6<br>
Jupyter notebook 5.2.1<br>
Spyder 3.2.6 <br>
* special package needed: xgboost
Please proceed to PDReadme2.docx in documentation for detailed steps.
## Benchmark
A crude, simple model like default parameterized support vector machine classifier or decision tree model could blatantly predict that everyone has Parkinson's disease and the precision would be 203/300 which is 67.7%, and recall will top at 100%. F1 score is logged at 80%. But the ROC AUC will suffer at 50%, which is useless as the model lose the ability to tell the difference. <br>
Below is another better benchmark score and graph for default Decision Tree classifier.
![Benchmark Score](https://github.com/cteeeri/parkinson_keystroke/blob/master/doccs/benchmark_score.png)
![Benchmark Graph](https://github.com/cteeeri/parkinson_keystroke/blob/master/doccs/benchmark_graph.png)

## Results
Many binary classifiers are tried. They includes bagging decision tree, bagging random forest, boosting gradientboosting, boosting XGBoost and voting ensemble involving classifiers mentioned. A lot of time is spent fine tuning hyperparameters, GridSeachCV is used to facilitate this task as well.
The results are as follow:
![Benchmark Score](https://github.com/cteeeri/parkinson_keystroke/blob/master/doccs/models_score.png)
![Benchmark Graph](https://github.com/cteeeri/parkinson_keystroke/blob/master/doccs/vc_model_graph.png)
Please also refer to PDReport.pdf for details.

## Thanks to references below
1.	Goldberger AL, Amaral LAN, Glass L, Hausdorff JM, Ivanov PCh, Mark RG, Mietus JE, Moody GB, Peng C-K, Stanley HE. PhysioBank, PhysioToolkit, and PhysioNet: Components of a New Research Resource for Complex Physiologic Signals. Circulation 101(23):e215-e220 [Circulation Electronic Pages; http://circ.ahajournals.org/content/101/23/e215]; 2000 (June 13). <br>
2.	L. Giancardo, A. Sánchez-Ferro, T. Arroyo-Gallego, I. Butterworth, C. S. Mendoza, P. Montero, M. Matarazzo, J. A. Obeso, M. L. Gray, R. San José Estépar. Computer keyboard interaction as an indicator of early Parkinson's disease. Scientific Reports 6, 34468; doi: 10.1038/srep34468 (2016)
3.	http://news.mit.edu/2015/typing-patterns-diagnose-early-onset-parkinsons-0401
Anne Trafton, MIT News Office
April 1, 2015 <br>
4.	https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5708704/
Holger Fröhlich
2017<br>
5.	http://xgboost.readthedocs.io/en/latest/python/python_api.html<br>
6.	https://machinelearningmastery.com/feature-importance-and-feature-selection-with-xgboost-in-python/<br>
7.	https://www.kaggle.com/lct14558/imbalanced-data-why-you-should-not-use-roc-curve<br>
8.	https://acutecaretesting.org/en/articles/precision-recall-curves-what-are-they-and-how-are-they-used<br>
9.	https://jakevdp.github.io/PythonDataScienceHandbook/04.14-visualization-with-seaborn.html<br>


