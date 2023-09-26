# **************************
# Business Problem:
# "Facebook recently introduced a new bidding type named "average bidding" as an alternative to the existing "maximum bidding" method.
# One of our clients, bombabomba.com, decided to test this new feature and wants to conduct an A/B test to understand
# whether average bidding brings more conversions than maximum bidding. The A/B test has been ongoing for a month, and now bombabomba.com
# expects you to analyze the results of this test. For Bombabomba.com, the ultimate success metric is Purchase.
# Therefore, statistical tests should focus on the Purchase metric."
# **************************

# **************************
# Dataset Story:
# This dataset contains information about a company's website, including details like the number of ads users have seen and clicked on,
# as well as revenue generated from these actions. There are two separate datasets for the Control and Test groups.
# These datasets can be found on separate sheets of the 'ab_testing.xlsx' Excel file. The Control group was subjected to Maximum Bidding,
# while the Test group was introduced to Average Bidding
# **************************

# **************************
# VARIABLES
# Impression: Number of ad views
# Click: Number of clicks on the displayed ad
# Purchase: Number of products purchased after the ad clicks
# Earning: Revenue generated from the purchased products
# **************************

# **************************
# Project Tasks
# Task 1: Data Preparation and Analysis
# Task 2: Defining the Hypothesis of the A/B Test
# Task 3: Performing the Hypothesis Test
# Task 4: Analysis of the Results


import pandas as pd
import numpy as np
from scipy.stats import shapiro, levene, ttest_ind

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df_control_m = pd.read_excel('ab_testing.xlsx', sheet_name="Control Group")
df_test_m = pd.read_excel('ab_testing.xlsx', sheet_name="Test Group")

df_control = df_control_m.copy()
df_test = df_test_m.copy()


# ***************************************
# Task 1: Data Preparation and Analysis
# ***************************************

# A function is used for missing value analysis
def analyze_missing_values(df):
    na_cols = df.columns[df.isna().any()].tolist()
    total_missing = df[na_cols].isna().sum().sort_values(ascending=False)
    percentage_missing = ((df[na_cols].isna().sum() / df.shape[0]) * 100).sort_values(ascending=False)
    missing_data = pd.DataFrame({'Missing Count': total_missing, 'Percentage (%)': np.round(percentage_missing, 2)})
    return missing_data


# to get an initial understanding of the data's structure, its content, and if there are any missing values that need to be addressed.
def sum_df(dataframe, head=6):
    print("~~~~~~~~~~|-HEAD-|~~~~~~~~~~ ")
    print(dataframe.head(head))
    print("~~~~~~~~~~|-TAIL-|~~~~~~~~~~ ")
    print(dataframe.tail(head))
    print("~~~~~~~~~~|-TYPES-|~~~~~~~~~~ ")
    print(dataframe.dtypes)
    print("~~~~~~~~~~|-SHAPE-|~~~~~~~~~~ ")
    print(dataframe.shape)
    print("~~~~~~~~~~|-NUMBER OF UNIQUE-|~~~~~~~~~~ ")
    print(dataframe.nunique())
    print("~~~~~~~~~~|-NA-|~~~~~~~~~~ ")
    print(dataframe.isnull().sum())
    print("~~~~~~~~~~|-QUANTILES-|~~~~~~~~~~ ")
    print(dataframe.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T)
    print("~~~~~~~~~~|-NUMERIC COLUMNS-|~~~~~~~~~~ ")
    print([i for i in dataframe.columns if dataframe[i].dtype != "O"])
    print("~~~~~~~~~~|-MISSING VALUE ANALYSIS-|~~~~~~~~~~ ")
    print(analyze_missing_values(dataframe))


sum_df(df_control)
sum_df(df_test)

# Based on the output of the sum_df(df_control) and sum_df(df_test) function, there are no outlier values.

# concat method to merge the control and test group data
df_control["group"] = "control"
df_test["group"] = "test"

df = pd.concat([df_control, df_test], axis=0, ignore_index=True)

df.head(5)
df.tail(5)

# **************************************************
# Task 2: Defining the Hypothesis of the A/B Test
# **************************************************

# Step 1: Defining the hypothesis

# H0 : M1  = M2 (There is NO statistically significant difference between the purchase averages of the control group and the test group)
# H1 : M1 != M2 (There is a statistically significant difference between the purchase averages of the control group and the test group)

# Step 2: Analysis of the purchase averages of the control group and the test group.

df.groupby("group").agg({"Purchase": "mean"})

# ******************************************
# Task 3: Performing the Hypothesis Test
# ******************************************

# Before conducting the hypothesis test, perform assumption checks.
# These are the assumption of normality and the assumption of homogeneity of variances

# Test separately whether the control and test groups satisfy the assumption of normality based on the 'purchase' variable

# Assumption of normality:
# h0: The assumption of normal distribution is met.
# h1: The assumption of normal distribution is not met.
# p < 0.05 Reject H0
# p > 0.05 Cannot be rejected H0
# Based on the test result, is the assumption of normality met for both the control and test groups?"

# Assumption of normality:
test_stat, pvalue = shapiro(df.loc[df["group"] == "control", "Purchase"])
print('Test Stat = %.5f, p-value = %.5f' % (test_stat, pvalue))
# Test Stat = 0.97727, p-value = 0.58911

test_stat, pvalue = shapiro(df.loc[df["group"] == "test", "Purchase"])
print('Test Stat = %.5f, p-value = %.5f' % (test_stat, pvalue))
# Test Stat = 0.95895, p-value = 0.15413

# Conclusion:
# H0 cannot be rejected since p value > 0.05 in both groups.
# The assumption of normality is provided.


# Variance Homogenity:
# Variance is the average of the squared differences from the Mean. Standard deviation is the square root of the variance.
# h0: The assumption of Variance Homogenity is met.
# h1: The assumption of Variance Homogenity is not met.
# p < 0.05 Reject H0
# p > 0.05 Cannot be rejected H0

test_stat, pvalue = levene(df.loc[df["group"] == "control", "Purchase"],
                           df.loc[df["group"] == "test", "Purchase"])
print('Test Stat = %.5f, p-value = %.5f' % (test_stat, pvalue))
# Test Stat = 2.63927, p-value = 0.10829

# Conclusion:
# H0 cannot be rejected since p value > 0.05.
# The variances are homogenous.

# Implementation of Appropriate Hypothesis Testing

# The two independent sample T-tests that is parametric tests can be applied because the assumptions are provided.

test_stat, pvalue = ttest_ind(df.loc[df["group"] == "control", "Purchase"],
                              df.loc[df["group"] == "test", "Purchase"],
                              equal_var=True)
print('Test Stat = %.5f, p-value = %.5f' % (test_stat, pvalue))
# Test Stat = -0.94156, p-value = 0.34933

# Conclusion
# H0 hypothesis can not be rejected because p value > 0.05.
# With an accuracy rate of 95%, M1 = M2 .So we can state that there is no statistically significant difference
# between the purchase averages for the Control and Test Groups.(M1=M2)

# ***********************************
# Task 4: Analysis of the Results
# ***********************************

# Step 1: Which test did you use? Why?

# First of all, a normality test was applied to both groups. It was observed that both groups conformed to the normal distribution.
# Then, the homogeneity of variance was examined as the second assumption. Since variances were homogenous,
# the "Independent Two-Sample T-Test" was applied. The resulting p-value was observed to be greater than 0.05,
# and the H0 hypothesis could not be rejected.


# Step 2: Provide recommendations to the client based on the test results you obtained.

# While there isn't a significant
# difference in terms of purchasing, the client can choose either method. However, differences in other statistics are also crucial.
# Differences in Clicks, Interaction, Earnings, and conversion rates should be evaluated to determine which method is more profitable.
# Especially since one pays Facebook per click, it can be determined in which method the click rate is lower, and the CTR (click-through rate)
# can be checked.Both groups should continue to be monitored.
