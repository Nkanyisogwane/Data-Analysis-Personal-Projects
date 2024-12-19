# **Mental Health & Suicide Rates Dashboard**

## **Project Overview**

This project is part of my personal learning journey as I continue to refine my data analysis skills. The goal of this project was to visualize the relationship between suicide rates and mental health resources using a global dataset. By utilizing **Power BI**, I created a one-page dashboard to analyze and display key metrics related to **suicide rates**, **mental health professionals**, and **mental health facilities**.

The dashboard provides insights into how the availability of mental health resources correlates with suicide rates across different countries, offering a valuable perspective on mental health trends globally.

![Mental Health & Suicide Rates Dashboard](https://github.com/Nkanyisogwane/Data-Analysis-Personal-Projects/blob/main/Mental-Health-Suicide-Rate/Mental.png?raw=true)

## **Key Metrics and Visualizations**

The dashboard includes the following key metrics and visualizations:

1.  **Overall Age-Standardized Suicide Rate**: Displays the global age-standardized suicide rate.
2.  **Crude Suicide Rate**: Shows the raw suicide rate across countries.
3.  **Mental Health Workforce Distribution**: A pie chart illustrating the distribution of nurses, psychiatrists, psychologists, and social workers across countries.
4.  **Suicide Rate Distribution by Country**: A map showing the suicide rates of various countries around the world.
5.  **Mental Hospitals Distribution by Country**: A bar chart that compares the availability of mental health facilities in different countries.
6.  **Crude Suicide Rate by Country and Gender**: A line chart comparing suicide rates by gender across different countries.

## **Methodology**

- **Data Import & Cleaning**: I cleaned the dataset by handling missing values, correcting column names, and ensuring that the data types were appropriately formatted (e.g., converting text to decimal for financial data). I used **Power BI Power Query** for cleaning the data and performing the necessary transformations.
- **Data Modeling**: The relationships between the tables were automatically established, and no additional modifications were needed for data modeling.
- **KPIs and Measures**: Using Power BI’s DAX functionality, I created key performance indicators (KPIs) to calculate and visualize the suicide rates and mental health workforce metrics.

## **Challenges**

- **Data Cleaning**: The dataset had some inconsistencies, such as missing values and columns with text values instead of decimals. It was necessary to clean the data before creating visualizations.
- **Lack of Date Field**: The dataset didn’t have a date column, which meant I couldn't add time-based slicers. I chose to work with year-based data instead, which was sufficient for the analysis.
- **First Health-Related Dataset**: This was my first time working with a health-related dataset, and I used **ChatGPT** to help suggest KPIs and chart types, especially for this unfamiliar subject.

## **Key Insights**

- **Mental Health Resources**: Countries with higher numbers of mental health professionals (e.g., psychiatrists) tend to have lower suicide rates, suggesting a correlation between mental health resources and suicide prevention.
- **Geographic Disparities**: There are significant disparities in the availability of mental health facilities worldwide, with some regions showing very few resources despite high suicide rates.
- **Suicide Rate Trends**: Countries like Japan and South Korea show higher suicide rates compared to other regions, highlighting areas where mental health interventions may be most needed.

## **Technologies Used**

- **Power BI**: For data visualization and creating interactive dashboards.
- **DAX**: Used for creating calculated columns and measures in Power BI.
- **Excel**: For initial data cleaning and transformations.

## **How to Use**

1. Clone this repository or download the Power BI file ([Mental_Health_Suicide_Rates.pbix](https://github.com/Nkanyisogwane/Data-Analysis-Personal-Projects/blob/main/Mental-Health-Suicide-Rate/mentalHealthandSuicideRates.pbix)).
2. Open the Power BI file in **Power BI Desktop**.
3. Interact with the dashboard by using slicers for countries to explore the data.
4. Use the visualizations to analyze suicide rates and mental health resources across different countries.

## **Future Improvements**

While this project was a valuable learning experience, I don’t plan to revisit this specific dashboard. However, based on the knowledge gained from this project, I would like to incorporate similar analyses into future projects. Possible directions include:

- **Predictive Modeling**: In future projects, I’d like to apply machine learning models to predict suicide trends based on available data and emerging factors.
- **Expanded Datasets**: I will explore incorporating other datasets, such as socioeconomic factors, to provide deeper insights into the mental health landscape.
- **Enhanced Interactivity**: Future dashboards could include more advanced filtering options and drill-through capabilities to allow for detailed data exploration.

## **Conclusion**

This project was an excellent opportunity to apply Power BI in analyzing real-world data related to mental health. It helped me develop my data cleaning, visualization, and analytical skills while offering meaningful insights into a crucial social issue. I look forward to using these learnings in future projects and continuing to improve my data analysis capabilities.

## **Dataset Source**

The dataset used for this analysis can be accessed here: [https://www.kaggle.com/datasets/twinkle0705/mental-health-and-suicide-rates?select=Facilities.csv]
