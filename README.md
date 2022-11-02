ISOSIMpy (c) by the ISOSIMpy Team

ISOSIMpy is licensed under a
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.

You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by-nc-sa/4.0/>.

# Please note:

This code is still under development. None of the components have been finally tested.

If you have any questions, write an email to jonas.vollhueter@tu-dresden.de.

# Installing and Using the Package

If you have experience with the `Python` programming language, just download the source code from this repository and move the `ISOSIMpy` package files (`Pre.py`, `Calculate.py`, `Multis.py`, `Post.py`, `main.py`) to a local directory from which you intend to work. Proceed with using the package as demonstrated in the examples / `Jupyter Notebooks`.

If you do not have experience with the `Python` programming language, please perform the following steps:
0. Download the source code in this repository
    1. [Here](https://github.com/jvollhueter/ISOSIMpy/tree/ISOSIMpy_FHDGGV), click on the green button labeled `Code` and select `download zip`
    2. After downloading, unpack the `zip`-archive into a target directory (name it, e.g., `ISOSIMpy`)
1. Download `Anaconda` (most popular and easy-to-use Python distribution) [here](https://www.anaconda.com/products/distribution)
2. Install `Anaconda`
3. Open the Anaconda `PowerShell Prompt`
4. Type `conda list` and hit `[ENTER]`
5. Look through the list and check if `python`, `jupyterlab`, `numpy`, `pandas`, and `matplotlib` are available
    1. If one of the packages is not available:
    2. (still in the `PowerShell Prompt`) type `conda install [PACKAGENAME]` and hit `[ENTER]`, where you replace `[PACKAGENAME]` by the missing package (i.e., `numpy`, `pandas`, `matplotlib`, etc.); if asked, type `y` and hit `[ENTER]` to proceed
6. (still in the `PowerShell Prompt`) type `jupyter lab` and hit `[ENTER]`; now a new tab with `JupyterLab` should open in your browser
7. In the file manager of `JupyterLab`, navigate to the `ISOSIMpy` directory and open an available `Jupyter Notebook` (e.g., `Notebook_Tracer_simple.ipynb`)
