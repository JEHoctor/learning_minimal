## Updated Readme

I've added new information at the top of this readme to document what I've learned while replicating the results in this repo/paper. The original readme is preserved at the bottom of this file.

Replication Steps
-----------------

## Operating System and Packages

The original readme suggests using apt to install the Eigen dependency. Ideally, this dependency would be managed by CMake, or at least have a specific version number that it depends on. For now, we can get an appropriate version by using a recent version of Ubuntu or Debian, or maybe even WSL2. I'm using Debian 11, and as of 2022-06-25, I can build the code without issue. For future reference, Debian 11 seems to install Eigen version 3.3.9.

I recommend installing build-essential (for make and gcc) at the same time, and python3-venv, which we will need later:
```bash
$ sudo apt install build-essential libeigen3-dev python3-venv
```

## CMake

I like to use the latest version of CMake available from Kitware, and install it via shell script. In this case, I downloaded version 3.23.2. If you have issues with a later version, try downgrading to this one. You can find the files for this release [here](https://github.com/Kitware/CMake/releases/tag/v3.23.2). Old CMake language features are occasionally obsoleted.

Usually, I would recommend running `ccmake` in place of `cmake`, but there really isn't anything interesting to configure for this code, so just run the commands suggested in the original readme to build the C code:

```bash
$ cmake -DCMAKE_BUILD_TYPE=Release ."
$ make
```

## Python and Packages

Now, you need to create a python virtual environment, activate it, and install the python dependencies. The authors did not provide a `requirements.txt` file, but the only dependencies are numpy and pytorch, so I've contributed a simple one that is suitable. I installed torch without GPU support, but it shouldn't be too hard to modify the requirments.txt to install the GPU-accellerated version instead.

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Data

The last thing to do before running the code is to download the data. I thought that the original readme was a little vague about the intended way to organize the data, so I've provided a shell script to download the data and arrange it the way I did. It takes about 11GB to store the uncompressed data. The shell script downloads archived data and deletes the archives after extracting the data, so the peak disk usage during this process is probably less than 17GB.

```bash
$ ./download_data.sh
```

## To be continued...

I will write about the next steps soon...

Original Readme
===============

Everything below this point is the original readme file.

LHC TRAINING AND TESTING PIPELINE 4p3v
======================================

Install
-------
1. Download the repo.
2. (If not installed) Install Eigen by "sudo apt-get install libeigen3-dev"
3. enter the repo and run "cmake -DCMAKE_BUILD_TYPE=Release ."
4. run "make" to compile the files

Assumption
----------
From now on we assume that the binaries have been compiled into directory BIN and the data has been downloaded into directory DATA. We assume that there is a directory MODEL (which contains file trainParam.txt at the beginning) into which the parts of the model (anchors, neural network, ...) are stored. If the directories are different, please substitute the strings BIN, DATA and MODEL with the actual paths to the directories containing the binaries and the data.</br>
The file testParam.txt files is located in the root of the repository. If the binaries are run from the root of the repository, please erase the string ROOT from the cmd commands. If the binaries are run from a different directory, please substitute ROOT with the relative location of the root of the repository.

Executables
-----------
After the compilation, the BIN folder contains the following files:</br>
<b>data_sampler</b> The input is the location of the COLMAP model and number of samples per camera pair. The binary samples problem-solution pairs from the model located in the given folder and stores them to the given file.</br>
Run as: ./BIN/data_sampler COLMAP_folder (num_samples) > sampled_data</br></br>

<b>connectivity</b> The input is the file with the anchor generation data. The binary computes the connectivity graph where the problems from the anchor generation file are the nodes and the edge connects the nodes if the Homotopy continuation is able to track from one of the problems to the other one.</br>
Run as: ./BIN/connectivity ./DATA/anchor_data.txt ./MODEL ./MODEL/trainParam.txt</br></br>

<b>anchors</b> The input is the connectivity graph generated in the previous step and the anchor generation data file. The binary produces a file which contains the anchors which cover some portion of the data.</br>
Run as: ./BIN/anchors ./DATA/anchor_data.txt ./MODEL ./MODEL/trainParam.txt</br></br>

<b>labels</b> The input is the set of the training (or validation) problems, the set of anchors and the transformation matrix generated in the previous binaries. The binary runs the homotopy continuation from every anchor to every training problems and generates two files: one of them (X_train.txt) contains the 14D representations of the training data and the other one (Y_train.txt) contains the labels of the training data which are the IDs of the anchors able to reach the problems.
Run as: ./BIN/labels ./DATA/train_data.txt ./MODEL ./MODEL train ./MODEL/trainParam.txt (to generate train data) and as </br> ./BIN/labels ./DATA/test_data.txt ./MODEL ./MODEL test ./MODEL/trainParam.txt (to generate test data) </br></br>

<b>evaluate</b> The input is the file containing the testing problem-solution pairs, and the location of the model folder. The output is the success rate and the running time of the solver on the data. The classifier does not use the TRASH bin.
Run as: ./BIN/evaluate ./DATA/test_data ./MODEL ./MODEL/trainParam.txt

<b>evaluate_T</b> The input is the file containing the testing problem-solution pairs, and the location of the model folder. The output is the success rate and the running time of the solver on the data. The classifier uses the TRASH bin.
Run as: ./BIN/evaluate_T ./DATA/test_data ./MODEL ./MODEL/trainParam.txt

Python scripts
--------------
In addition to the compiled binaries, the repo contains the following python scripts:

<b>sample_data.py</b> This script simplifies the sampling of the problem-solution pairs, which is performed by the binary ./BIN/data_sampler The input is the folder which contains the COLMAP model, the desired output file, and the expected total number of samples. The script samples approximately the given number of samples from the model in the folder and stores them to the given output file.
Run as: python3 ./ROOT/sample_data.py input_folder output_file num_samples

<b>train_nn.py</b> whose input is the training and validation data generated with the labels directory. The script sets up and trains a neural network. It produces a text file which contains the weights of the neural network. This file is readable by the testing binary. </br>
Run as: python3 ./ROOT/train_nn.py ./MODEL ./ROOT/trainParam.txt </br><br>

Settings
--------
The files with settings <b>trainParam.txt</b> and <b>testParam.txt</b> contain the settings. The trainParam.txt file contains settings for the homotopy continuation, alignment, anchors generation, low dimensional data representation and neural network training. The testParam.txt file contains settings for the testing and for the Ransac.

Data sampling
-------------
We use training data from ETH 3D dataset. The training data can be downloaded from https://www.eth3d.net/datasets#high-res-multi-view
We use data NAME_dslr_undistorted.7z, where NAME is the name of sequence. We assume, that the archive has been extracted into a folder NAME_dslr_undistorted
Folder NAME_dslr_undistorted contains a directory NAME, which contains directories dslr_calibration_undistorted and images. Directory dslr_calibration_undistorted contains the COLMAP model (files "cameras.txt", "images.txt", "points3D.txt").
In order to sample problem-solution pairs from a COLMAP folder, please run:

python3 ./sample_data.py COLMAP_folder output_file num_samples

For training data, we run:
python3 ./sample_data.py NAME_dslr_undistorted/NAME/dslr_calibration_undistorted/ ./DATA/train_NAME.txt 1000000

For testing data, we run:
python3 ./sample_data.py NAME_dslr_undistorted/NAME/dslr_calibration_undistorted/ ./DATA/test_NAME.txt 30000

For data for generating anchors, we run:
python3 ./sample_data.py NAME_dslr_undistorted/NAME/dslr_calibration_undistorted/ ./DATA/anchor_data_NAME.txt 40000
(the number of data may be smaller)

Data format
-----------
The sampled problem-solution pairs are stored in text files.
In the first line, there is a single number N, which gives the number of samples.
Each of the following N lines contains one sampled problem-solution pair in the following format:
First 24 numbers represent 2D projections of 4 points into 3 cameras in the order u1 u2 ... u4 v1 v2 ... v4 u1' u2' ... u4' v1' v2' ... v4'' u1'' u2'' ... u4'' v1'' v2'' ... v4'' (ui is the first coordinate of the i-th point into the 1st camera, vi is second coordinate of the same projection; (ui' vi') is the projection of the same point into the second camera, (ui'' vi'') is the projection of the same point into the third camera)
The next 12 numbers represent the depths in the order d1 d2 ... d4 d1' d2' ... d4'' d1'' d2'' ... d4'' (di is the depth of i-th point in the first camera, di' is the depth of the same point in the second camera, di'' is the depth of the same point in the third camera)

Data sam
--------
In order to train the model, run the following commands. Substitute the strings BIN, DATA, MODEL, ROOT, NAME according to the <b>Assumption</b> section of the Readme file.
1) Sample the data:</br>
python3 ./ROOT/sample_data.py NAME1_dslr_undistorted/NAME1/dslr_calibration_undistorted/ ./DATA/anchor_data.txt 40000</br>
python3 ./ROOT/sample_data.py NAME2_dslr_undistorted/NAME2/dslr_calibration_undistorted/ ./DATA/val_data.txt 30000</br>
python3 ./ROOT/sample_data.py NAME3_dslr_undistorted/NAME3/dslr_calibration_undistorted/ ./DATA/val_data.txt 30000</br>
python3 ./ROOT/sample_data.py NAME_dslr_undistorted/NAME/dslr_calibration_undistorted/ ./DATA/train_data_NAME.txt 1000000</br>
2) ./BIN/connectivity ./DATA/anchor_data.txt ./MODEL ./MODEL/trainParam.txt
3) ./BIN/anchors ./DATA/anchor_data.txt ./MODEL ./MODEL/trainParam.txt
4) ./BIN/labels ./DATA/val_data.txt ./MODEL ./MODEL val ./MODEL/trainParam.txt
5) ./BIN/labels ./DATA/train_data_NAME/.txt ./MODEL ./MODEL train_NAME ./MODEL/trainParam.txt
(if training data from different sources NAME_A, NAME_B, ..., NAME_Z are used, concatenate them):
6) cat ./DATA/X_train_NAME_A.txt ./DATA/X_train_NAME_B.txt ... ./DATA/X_train_NAME_Z.txt > ./DATA/X_train.txt
7) cat ./DATA/Y_train_NAME_A.txt ./DATA/Y_train_NAME_B.txt ... ./DATA/X_train_NAME_Z.txt > ./DATA/Y_train.txt
8) python3 ./ROOT/train_nn.py ./MODEL ./MODEL/trainParam.txt

After this, the trained model should be located in the MODEL directory.

Evaluation
----------
With trash: ./BIN/evaluate_T ./DATA/test_data.txt ./MODEL/ ./MODEL/trainParam.txt
Without trash: ./BIN/evaluate ./DATA/test_data.txt ./MODEL/ ./MODEL/trainParam.txt

Included data
-------------
We include one trained model together with the code. This model is located in folder ./ROOT/model and contains the following files:
<b>anchors.txt</b> Contains the starting problem-solution pairs generated with our procedure.
<b>nn.txt</b> Contains the MLP classifier generated with our procedure, this classifier is trained to select one of 134 anchors stored in anchors.txt.
<b>trainParam.txt</b> Contains the settings of the homotopy continuation, and of the MLP training procedure.


