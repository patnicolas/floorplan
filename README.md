### Patrick Nicolas - Last update 06.28.2023

![Topology Graph Neural Network for floor plans](images/background.png)




The objective is this repository is to evaluate various techniques to extract and organize information from a floor plan

## References 
- [Room Classification on Floor Plan Graphs using Graph Neural Networks.pdf](https://arxiv.org/pdf/2108.05947.pdf).  
- [Parsing Line Segments of Floor Plan Images Using Graph Neural Networks](https://arxiv.org/pdf/2303.03851.pdf).  
- [Extracting real estate values of rental apartment floor plans using graph convolutional networks](https://arxiv.org/pdf/2303.13568.pdf).   
- [Room semantics inference using random forest and relational graph convolutional networks](https://onlinelibrary.wiley.com/doi/epdf/10.1111/tgis.12664).  




## Environment
| Package      | Version |
|:-------------|:--------|
| python       | 3.9.16  |
| torch        | 2.0.1   |
| openai       | 0.27.1  |
| matplotlib   | 3.7.1   |
| scikit-learn | 1.2.2   |
| numpy        | 1.24.3  |
| pandas       | 2.0.2   |
| langchain    | 0.0.2   |
| polars       | 0.17.0  |
| fastapi      | 0.97.0  |
| uvicorn      | 0.22.0  |
| requests     | 2.31.0  |
| pydantic     | 1.10.9  |
| jinja2       | 3.1.2.  |


## Versions
| Date       | Version |
|:-----------|:--------|
| 06.27.2023 | 0.1     |


## Deployment
```
pip install -r requirements

pandas~=2.0.2
boto3~=1.26.149
requests~=2.31.0
urllib3~=1.26.16
polars~=0.18.2
cryptography~=41.0.1
fastapi~=0.96.0
pydantic~=1.10.9
jinja2~=3.1.2
uvicorn~=0.22.0 

```
_Cost estimate_:     
- AWS ~15/20cents hour with a or t4 instances (~$110/mo).   
- GoDaddy  Dedicated server ($145/mo).     



## Todo list
- Generate and test requirements.txt file.    
- Specify copyright.     
- Encryption of SMTP user name and password or env. Variables
- Fix issue with drag-drop file with UploadFile.   
- Select a target email.   
- Define landing page (menus, ..).   
- Rename pdf file to be rename (MIME).    
- Define command line arguments. argparse.ArgumentParser.     
- Investigate ChatGPT-based PDF parsing https://github.com/brandonrobertz/chatgpt-document-extraction/tree/main.    
- Investigate detection and extraction of key widgets/components.       




