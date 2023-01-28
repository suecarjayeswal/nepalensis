# [**The BOLD Nepal** <i class="fa fa-github"></i>](https://github.com/suecarjayeswal/nepalensis.git)
>  It's an interactive website that presents nepali specimens that are present in BOLD (The Barcode of Life Data System) database. The data was obtained from [BOLD's website](https://boldsystems.org/). This was made by Team *nepalensis* for [Watson Crack the Code-Fest 2022 (Nepal's First Biohackathon)](https://kubicclub.ku.edu.np/) organized by Kathmandu University Biotechnology Creatives [(KUBiC)](https://kubicclub.ku.edu.np/biohackathon22/) on 4th and 5th sept , 2022.

## Team *nepalensis*:
- **Swikar Jaiswal** , 1st year , B.Sc. in Computational Mathematics
                          
- **Aahana Bhandari** , 3rd year , B.Tech. in Biotechnology


---
## Installation

To run the website, please go through following steps:
// Since there are certain dependencies required for this project, it is a must to install the environment packages

0) Open your terminal in the nepalensis folder then enter following commands
1) conda create --name myEnv --file environment.yml
    if you want to install packages in your personal conda environment, enter following instead of above one:
        conda install --name <urEnvName> --file environment.yml

2) conda activate myEnv
3) pip install -r requirements.txt

4) Now you may move to directory BOLDmapNepal using:
        cd BOLDmapNepal 

5) Finally, run the server using the command below:
        python manage.py runserver
        
### Usage:
The website itself has shown how you can you search bar to find specimens of your interest on the map. You can simply play with the search bar and map, exploring various informations present there.


![Preview]("https://github.com/suecarjayeswal/nepalensis/blob/master/BOLDmapNepal/TheBOLDNepal.gif"){:class="post-img"}














