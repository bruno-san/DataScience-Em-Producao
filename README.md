# Data Science in Production
This Repository contains the scripts and files related to the course Data Science in Production ("Data Science em Produção") from [Meigarom Lopes](https://github.com/Meigarom), who is a well-known Data Scientist with several years of experience and practical applied know-how.

---

## Table of Contents
- [Introduction](#introduction)
- [Version 02 Improvements](#version-02-improvements)
- [Module 01. The Business Problem](#module-01-the-business-problem)
- [Module 02. Data Description](#module-02-data-description)
- [Module 03. Feature Engineering](#module-03-feature-engineering)

---

## Introduction
The Data Science in Production course is an online course that teaches how to design and implement a data science, machine learning project with Python, from the dataset until the model deployment. The course covers also the creation of a Telegram bot, as well as the creation of a Cloud-based API and Story-Telling techniques.

Unlike other online courses, this one is particularly special because it has a business-driven approach to solve a real business problem, so that the student can really think and understand the underlying logic behind the problem request, hence one can develop a sophisticated solution that meets the business-team expectation and bring value to it.

For more details, please visit the [Data Science in Production website.](https://sejaumdatascientist.com/como-ser-um-data-scientist/)

The detailed description, step-by-step solution is described below.
Please feel free to leave a comment with improvement suggestions: it will be highly appreciated!

---

## Version 02 Improvements
The process described below refers to the version 02 of the CRISP cycle with improvements regarding to the first version. The main improvement is the use of forecasted customers’ number in the sales prediction. For that, it was made a new, specific project so that the customers’ number for the next 6 weeks could be predicted and then applied to the version 02 of the sales prediction model. This script is also available in this repository.

Furthermore, other improvements were made such as outliers’ removal and additional feature scaling regarding the first version. All of this is described below in details.

The improvements were made mainly due to the points below:
- Practice and reinforce the course learned content – python code and the CRISP Cycle;
- Improve the model predictions and results;
- Better understand the business and get new insights;
- To serve as a Coursework Completion.

---

## Module 01. The Business Problem
### 1. The Problem: the business team requested a 6-weeks sales forecast.

**Key points to understand a data science problem:**
- What is the motivation? What is the context behind?
- What is the root cause? Why does the business team need a forecast?
- Who is the Stakeholder?
- What is the expected solution format?

In this case, the key point of the problem are:
- **Request:** the CFO requested this solution to the business team in a management meeting;
- **The root cause:** the CFO aims to reform the stores. However, it is extremely hard to determine the reform budget for each store;
- **The Stakeholder:** The CFO is the Stakeholder;
- **Solution Format:**
    - **Granularity:** Daily sales forecast (in R$) per store for the next 6 weeks;
    - **Problem Type:** Sales forecast;
    - **Potential Methods:** Time Series, Regression, Neural Networks;
    - **Output Shape:** Sales forecast displayed in a smartphone.

The above-mentioned key points show that there is relevant content behind the 6 weeks sales forecast request: the final goal is to reform the stores. However, it is not possible to set a budget for that without knowing the revenue for the period: it is a risk, for example, if the reform budget exceeds the total amount of sales, that is, pratical there would not be enough money to finish the reform.

### 2. The Data
The Dataset applied to develop the solution is the [Rossmann Store Sales from Kaggle.](https://www.kaggle.com/c/rossmann-store-sales/data)

### 3. Solution approach: The CRISP-DS Cycle
To design, model and deploy the solution will be applied the CRISP-DS (Cross-Industry Standard Process - Data Science, a.k.a. CRISP-DM) project management method.
The CRISP is a cyclic, iterative development method that covers all the steps needed to solve a data science problem. The image below shows the CRISP cycle:
![](img/CRISP.jpg)

[back to top](#table-of-contents)

---

## Module 02. Data Description
Data description goal is to describe and understand the available dataset that will be used to train and validate the model. In other words: **one must know the data at hand** and then notice: how challenging is the problem?

There are several ways to make a first, general data analysis. In this case, the following steps will be taken:
- Data Dimensions;
- Data Types;
- Missing values (check and fillout);
- Descriptive Statistics.

The descriptive Statistics is particularly important for two main reasons:
1. Gain business know-how;
2. Check Failures.

Within the Descriptive Statistics there are two main metrics:
- Dispersion metrics (standard deviation, min, max, skew, kurtosis);
- Central Tendency metrics (for example mean and median).

**Data Dimension:**

- Number of Rows: 1017209

- Number of Cols: 18

**Date Range:**

- first     2013-01-01

- last      2015-07-31


**Summary Statistics:**
- Numerical attributes summary table:
![](img/numericalattributes.PNG)
  
  
- Categorical Attributes Boxplot:
![](img/boxplotcatattributes.PNG)

[back to top](#table-of-contents)

---

## Module 03. Feature Engineering
### 1. Mind Map Hypothesis
The Mind Map is created in order to understand and highlight the key points below:
1.	Phenomenon: What phenomenon is being modeled?
2.	What are the factors that influence the phenomenon?
3.	What are the factors’ attributes?
4.	Hypothesis List: Hypothesis to validate with the data.

The main goal of the mind map is to generate a hypothesis list, which will later derivate an Analysis to validate or reject them. As a result, this analysis will be the basis for business insights, which can be both new, unknown information obtained from the data analysis, as well as to oppose some biased belief.

The Mind Map below shows the key factors of daily store sales.
![](img/Mindmaphypothesis.png)

### 2. Hypothesis List
Based on the Mind Map, the Hypothesis List below was generated. It is important though to highlight that the hypothesis are not a cause-effect relation, but a correlation. For example, a big store should always sell more it is not always the truth in practice. The goal is to recognize and understand the tiny, little effects that contribute to increase or decrease the sales. Furthermore, for the final hypothesis list it is also taken into account the availability of information in the dataset, once the hypothesis will be later checked in the exploratory data analysis step.

![](img/m03_hypothesis_list.PNG)

### 3. Feature Engineering
The goal of the feature engineering is to derivate new features from the available ones, so that it can be used to train a predictive model. The reasons for that are:
1.	The model to be developed is as good as the data trained on it;
2.	Improve the model predictive power;
3.	It creates the possibility to use less complex models that are faster than the more complex ones;
4.	The new features can better represent the underlying problem, which will facilitate the machine learning process.

In this problem, the following steps were carried-out to perform feature engineering:
1.	Decomposing dates to year, month, day, week of year and year week – helps the model to better represent structures or seasonality;
2.	Combining  detached features such as competition open since year and competition open since month, once they are related to the same date information;
3.	Calculate date difference between the observation date and the event date, for example promo since and date to result in a new feature that shows how much time such store is in a promotion state.
4.	Replace letter by text in categorical features.

### 4. Special Feature: Customers
The customers feature deserves a specific explanation. In the first version of the CRISP cycle, that is, in the first developed model, this feature was removed in the variables filtering step (next step described below) due to a business restriction. It is so because in the 6-week sales prediction the customers’ information will not be available. In other words: it is unknown how much customers will visit the stores in the next 6 weeks. Although the customers feature is available in the training dataset, it cannot be used to train the model because it is not available in the test dataset. Hence, this feature must be removed from the training dataset.

To solve such problem and also to improve the model’s performance, in the version 02 of the CRISP cycle it was made a specific script and model (code available in this repository) to predict the number of customers for the next 6 weeks. This information was then added to the test dataset in order to allow the model to predict the sales with this information. That is only possible if the model is trained also with the customers’ feature, which is the reason it was kept in the variables filtering step in the version 02 of the CRISP Cycle.
To summarize: it can be affirmed that this version 02 is a sales prediction based on customers prediction.

### 5. Variables Filtering
The variable filtering is applied due to business restrictions. It is necessary to check, based on the data description step previously performed, if all data and features from the training dataset will be actually available in the test dataset. It is also very important to check, considering a business perspective, what are the business-team’s processes and what kind of restrictions they have to provide the data, otherwise the model will be trained with data that does not correspond to the test data, which will lead to predictions that do not accomplish the expected results.

For this problem the closed stores and stores with sales equal to zero were filtered, because they are not relevant for the sales prediction. Furthermore, the 0,1%of  highest sales values were filtered because they are outliers. Additionally, the column open was removed because only open stores are now taken into account. The column promo interval was also removed, because new features were generated from it in the previous step, therefore its information is already in the dataset.

After all of these steps the final features are described below:
![](img/m03_features.PNG)

[back to top](#table-of-contents)

---