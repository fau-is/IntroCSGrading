# psgrade
Psgrade is a tool to evaluate the submissions of all 
students to a certain problem set in IntroCS.

## Optional Installing the tool as command-line tool
Run the following command to install the tool as a commandline tool (Recommended to do so in a virtualenv)
```bash
python setup.py install
```

## Usage
To use the program, you need to prepare some files and install requirements.

### Preliminaries

#### CS50-csvs
The cs50 csvs contain all information about students' submissions. 
Did they pass enough checks? Did style50 yield a score above 0.8?
Where is their code located at? 


1. Visit the [submit50](https://submit.cs50.io)-Website.
2. Go to courses and submissions to the course
3. Find the slugs, that you are interested in and filter them for the final date of submission.
4. Export the files as csv AND do not rename them.
5. Place them in any folder where psgrade can access them.

#### Grade Table
Psgrade will amend a grade table in csv format with an additional column called Pset(#).
This column indicates whether a student earned a bonus point or not.

The grade table must at least have the column Git_username. 

### Running the tool
#### Command Line Arguments
The minimum requirement to execute the program are the following.
1. --inputcsv \[CSV files ...]
   * After inputcsv add the paths to the submit50csv, so to their names and where you stored them.
2. --gradetable /path/to/gradetable.csv 
   * Grade Table that will be amended
3. --psetId # 
   * where # is the number of the week. Used to construct the column in the gradetable

Additional parameters refer to results creation
1. --tasks \[TASKS ...]
   * list all tasks which are part of a problem set
   * **IMPORTANT**: For tasks like mario, where there is less and more in the problem set name, you must only specify less and more. Since slugs are split by '/' and only the last word is used for distinguishing tasks. Therefore, _cs50/problems/x/mario/less_ is cropped to only _less_.
   * Example (Pset1): --tasks less more cash credit
2. --choices [CHOICES ...]
   * If a problem set contains choices like: "You can submit taskA or taskB"
   * Otherwise, you can fully ignore the command line argument.
   * If a problem set contains a choice, tasks which are not part of a choice still need to be listed in choices.
   * _Format_: taskA-taskB taskC-taskD taskE ...
   *. Example (Pset1 considering hello): --tasks hello less more cash credit --choices less-more cash-credit hello
4. --sentimental
   * Does a problem set contain a sentimental task. If there is set it, otherwise ignore it

Lastly there are some parameters regarding plagiarism checks. 
1. --plag 
   * Activates checking plagiarism
2. --archive
   * Should the program look for archive solutions.
   * Archive solutions must be in same/similar srtructure as submissions after their download. 
3. --distribution_code \[distribution.download.com ...]
   * URLs of the distribution zips. 
   * Will be downloaded and unzipped automatically

### Example
To run the program for Pset1. 
```bash
psgrade --inputcsv cs50_problems_2022_x_mario_less.csv cs50_problems_2022_x_mario_more.csv cs50_problems_2022_x_cash cs50_problems_2022_x_credit --gradetable gradetable.csv --psetId 1
```
If the program is not installed in your venv...
```bash
python psgrade-runner.py ...
```
... will do the job.

## License
Initial Author Sebastian Dunzer.
[MIT](https://choosealicense.com/licenses/mit/)