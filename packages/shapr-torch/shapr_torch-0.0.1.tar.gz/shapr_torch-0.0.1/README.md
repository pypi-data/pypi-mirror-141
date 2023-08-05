# SHAPR
<p align="center">
<img src="shapr_logo.png"  width="200" />
</p>
Reconstructing 3D objects from 2D images is both challenging for our brains and machine learning algorithms. To support this spatial reasoning task, contextual information about the overall shape of an object is critical. However, such information is not captured by established loss terms (e.g. Dice loss).
We propose to complement geometrical shape information by including multi-scale topological features, such as connected components, cycles, and voids, in the reconstruction loss. Our method calculates topological features from 3D volumetric data based on cubical complexes and uses an optimal transport distance to guide the reconstruction process. This topology-aware loss is fully differentiable, computationally efficient, and can be added to any neural network.
We demonstrate the utility of our loss by incorporating it into SHAPR, a model for predicting the 3D cell shape of individual cells based on 2D microscopy images. Using a hybrid loss that leverages both geometrical and topological information of single objects to assess their shape, we find that topological information substantially improves the quality of reconstructions, thus highlighting its ability to extract more relevant features from image datasets.

please refer to our preprint on bioRxiv 
[here](ToDo)


<p align="center">
<img src="shapr_architecture.png"  width="400" />
</p>
SHAPR consists of a 2D encoder, which embeds 2D images into a
latent space, and a 3D decoder, which reconstructs 3D shapes from the latent space representation.
To train SHAPR we segment 3D microscopy images (we show an exemplary single red blood cell).
We pair a 2D segmentation with the microscopy image of the same slice to enter the encoder as input.
During supervised training (Fig. 1, step 1), we minimize the reconstruction loss (see Methods),
which is the sum of the Dice loss and the binary cross entropy loss between the 3D segmentations and SHAPR predictions.
For an input image of 64 x 64 pixels, we provide the pixel sizes for each layer in the gray boxes and the filter sizes on top of each box.
In the second step, we fine-tune SHAPR by adding a discriminator.
The discriminator is trained to differentiate between SHAPR output and ground truth segmentation and minimize
the adversarial loss. It thereby challenges SHAPR to output realistic 3D objects.

<p align="center">
<img src="SHAPR_topology.png"  width="600" />
</p>
Given a predicted object and a 3D ground truth object, we calculatetopological features using (cubical)
persistent homology, obtaining a set of per-sistence diagrams.
Each point in a persistence diagram denotes the birth anddeath of a topological feature of some dimension of the given object.
We com-pare these diagrams using LT, our topology-based loss, and weight this withexisting loss terms like binary cross entropy (BCE)
and Dice.



## Installation:

Fork the repository.

### Installation using a poetry:
We recommend to install and run SHAPR_torch using python-poetry: https://python-poetry.org

```console
$ cd SHAPR
$ poetry install
```


```console
$ cd SHAPR
$ pip3 install -e .
```

For running SHAPR_torch with the topological loss the additional requirement of pytorch_topological is required: https://github.com/aidos-lab/pytorch-topological


### Installation using a vitual environment:
We would recommend to first set a virtual environment and then install the package:

```console
$ cd SHAPR
$ conda env create -f SHAPR_environment_pytorch.yml
$ python setup.py install
```


Now by openning the Jupyter-Notebook you have the option to select the `.venv_shapr` as the kernel.

## Installation using pip install:
You can also install SHAPR using:
```console
pip install shapr_torch
```

For running the code, you need to have Python 3.6 or higher installed. In addition, these are the main dependencies:

```yaml
- cudatoolkit: 10.1.243 # in case of GPU existance
- cudnn: 7.6.5 # in case of GPU existance
- h5py: 2.10.0
- hdf5: 1.10.6
- imageio: 2.9.0
- matplotlib: 3.3.4
- numpy: 1.20.3
- python: 3.6.7
- scikit-image: 0.18.1
- scikit-learn: 0.24.1
- scipy: 1.6.2
- torch: 1.10.1
- pytorch-lightning: 1.5.7
```


## Running SHAPR:

Please find an example of how to run SHAPR from a jupyter notebook in  /SHAPR/docs/jupyter notebook/Run SHAPR from notebook.ipynb

You can also run SHAPR using a params.json file, which is provided in SHAPR/docs/sample/params.json.

# Setting parameters
To run SHAPR you should set the following parameters:
Setting parameters are:
- `path`: path to a folder that includes three subfolder of
    1. `obj`: containing the 3D groundtruth segmentations, 
    2. `mask`: containing the 2D masks, 
    3. `image`: containing the images from which the 2D masks were segmented (e.g. brightfield).
- `result_path`: path to a folder for saving the results of predictions.
- `pretrained_weights_path`: path to a folder for saving and reloading pretrain model 
- `random_seed`: seed for random generator in order to keep the results reproducible.
- "epochs_SHAPR": The number of epochs SHAPR_torch will train at a maximum in the supervised fashion (early stopping with a patience of 15 is implemented)
- "epochs_cSHAPR":  The number of epochs SHAPR_torch will train at a maximum in the adverserial fashion, after training in supervised fashion (early stopping with a patience of 15 is implemented)
- "topo_lambda": The Lambda of the loss sum, determines the contribution of the topological loss to the geometrical loss
- "topo_interp": To which dimensions the volume is scaled before calculating the topological featues
- "topo_feat_d": The dimension of the topological featues

The setting parameters are read from the `settings` object. You may change the setting parameters by directly changing their default values in a '/SHAPR/params.json` file or simply package API like:
```console
> from shapr import settings
> settings.path = "a/new/path"
```
We have added an example of a 'params.json' file to SHAPR/docs/sample/params.json. If you want to use it, please adapt the paths to your project and copy the 'params.json' to /SHAPR/params.json, then execute the /SHAPR/shapr/run_train_script.py
You can also print all the parameters and their values using `print()` function:

> print(settings)
------ settings parameters ------
path: "path value"
result_path: "result_path value"
pretrained_weights_path: "pretrained_weights_path value"
random_seed: 0
```

## Running functions:
You can run the training and evaluating on the test sample by calling the `run_train()` and `run_evaluation()` functions respectively.
```console
> from shapr import run_train
> run_train()
```

## Folder structure 
SHAPR expects the data in the following folder structure (see sample). With corresponding files having the same name. 2D microscopy images (64x64px) should be contained in the images folder, 2D segmentations (64x64px) in the mask folder and the 3D segmentation (64x64x64px) in the obj folder. 
```bash
path
├── image                 
│   ├── 000003-num1.png
│   │── 000004-num9.png
│   │── 000006-num1.png
│   │── .
│   │── .
│   │── .
│   │── 059994-num1.png     
│
└── mask               
│   ├── 000003-num1.png
│   │── 000004-num9.png
│   │── 000006-num1.png
│   │── .
│   │── .
│   │── .
│   │── 059994-num1.png    
│
└── obj     
│   ├── 000003-num1.png
│   │── 000004-num9.png
│   │── 000006-num1.png
│   │── .
│   │── .
│   │── .
│   │── 059994-num1.png    

```


## Contributing

We are happy about any contributions. For any suggested changes, please send a pull request to the *develop* branch.

## Citation

If you use SHAPR, please cite this paper: https://www.biorxiv.org/content/10.1101/2021.09.29.462353v1 and ToDo

