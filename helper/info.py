stats_info={
    "Mode": "It is one/more most occuring data in the dataset feature",
    "Mean": "It is the average or most expected value",
    "Median": "It represents the middle most datapoint in a sorted feature",
    "Range": "Range of values over which data is spread",
    "Variance": "How spread out the values in a data set are from the mean (average)", 
    "Standard Deviation": "Square root of variance",
    "Maximum": "Maximum value of the feature",
    "Minimum": "Minimum value of the feature",
    "Skewness": "Skewness measures the asymmetry of a data distribution around its mean",
    "Kurtosis": "Kurtosis measures the 'tailedness' or the sharpness of the peak of a data",
    "Q1":"1st Quartile or 25th Percentile",
    "Q2":"2nd Quartile or 50th Percentile(Median)",
    "Q3":"3rd Quartile or 75th Percentile",
    "IQR":"Q3 - Q1"

}

image_path={
    "Skewness": "media/skewness.png",
}

formula={
    "Mean":"media/mean.png",
    "Variance":"media/variance.png"
}
stats_detailed_info={
    "Measures of Central Tendency":{
        "Mode": "Value(s) of feature with the highest frequency",
        "Mean": "It is the most representative value (or average) that tends to lie centrally within the feature set. It can be measured using AM, GM and HM. Being general, it doesn't provide correct overview when there is large gap between datapoints.",
        "Median": "It represents the middle most datapoint when feature is arranged(sorted) in some order of magnitude, dividing set into two approximate halves",
    },
    "Measures of Dispersion":{
        "Range": "Represents variability or spread of data. It may not be a proper indicator of extent of scatter of a distribution.",
        "Variance": "How spread out the values in a data set are from the mean (average). The square measure is taken to account for each variation, else negative variation may cancel out positive ones.", 
        "Standard Deviation": "Square root of variance. It is generally preferred over variance because it is expressed in the same units as the original data, making it directly interpretable",
        "Q1":"also known as the 1st Quartile or 25th Percentile implies 25% of data lie below the Q1 value",
        "Q2":"also known as the 2nd Quartile or 50th Percentile(Median) implies 50% of data lie below the Q2 value",
        "Q3":"also known as the 3rd Quartile or 75th Percentile implies 75% of data lie below the Q3 value",
        "IQR":"Interquartile range or midspread is Q3 - Q1, represent the middlemost 50% data points. Boxplots represent quartiles and is a way of determining outliers"
    },
    "Variability":{
        "Skewness": "It is the measure of symmetry, precisely the lack of symmetry about mean. The property is graphically determined by the extent of tapering of tails. Longer left tails -> -ve skew; Longer right tails -> +ve skew",
        "Kurtosis": "Kurtosis measures the degree of 'tailedness' or the sharpness of the peak. Fatter tails i.e. higher peaks represent Leptokurtic distributions(+ve kurtosis) and thinner tails i.e. lower peaks represent Platykurtic distributiond(-ve kurtosis)"
    },
}


def get_stats_info():
    return stats_info

def get_stats_detailed_info():
    return stats_detailed_info

def get_static_media():
    return image_path

def get_formula():
    return formula