ISOSIMpy (c) by the ISOSIMpy Team

ISOSIMpy is licensed under a
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.

You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by-nc-sa/4.0/>.

# Please note:

This code is still under development. None of the components have been finally tested.

If you have any questions, write an email to max_gustav.rudolph@tu-dresden.de

# MyBinder

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jvollhueter/ISOSIMpy/ISOSIMpy_FHDGGV)

A Binder is available in which you can run the example notebooks remotely. With that, you do not need to install a Python distribution but you are also limited in functionality and adaptability (you cannot adapt the notebooks manually).

# Installing and Using the Package

If you have experience with the `Python` programming language, just download the source code from this repository and move the `ISOSIMpy` package files (`Pre.py`, `Calculate.py`, `Multis.py`, `Post.py`, `main.py`) to a local directory from which you intend to work. Proceed with using the package as demonstrated in the examples / `Jupyter Notebooks`.

If you do not have experience with the `Python` programming language, please perform the following steps:

0. Download the source code in this repository
    1. [Here](https://github.com/jvollhueter/ISOSIMpy/tree/ISOSIMpy_FHDGGV), click on the green button labeled `Code` and select `download zip`
    2. After downloading, unpack the `zip`-archive into a target directory (name it, e.g., `ISOSIMpy`)
1. Download `Anaconda` (most popular and easy-to-use Python distribution) [here](https://www.anaconda.com/products/distribution)
2. Install `Anaconda`
    1. during the installation **DO NOT SET THE PATH VARIABLE** and **DO NOT SET AS DEFAULT PYTHON INSTALLATION**
3. Open the `Anaconda PowerShell Prompt`
    1. press your `[WINDOWS]` button
    2. in the menu, locate the folder named `Anaconda` (or similar)
    3. open `Anaconda PowerShell Prompt`
4. (still in the `PowerShell Prompt`) type `conda install -c conda-forge ipyfilechooser` and hit `[ENTER]`; if asked, type `y` and hit `[ENTER]` to proceed
5. (still in the `PowerShell Prompt`) type `jupyter lab` and hit `[ENTER]`; now a new tab with `JupyterLab` should open in your browser
    1. **Note**: `JupyterLab` may not work with the Microsoft Edge browser; use Chrome or Firefox instead (set Chrome or Firefox as default browser)
6. In the file manager of `JupyterLab`, navigate to the `ISOSIMpy` directory and open an available `Jupyter Notebook` (e.g., `Notebook_Tracer_simple.ipynb`)
