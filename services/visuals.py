from matplotlib import dates
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from PIL import Image
from helper.image_handler import encode_img2b64
from helper.categories import detect_categories, categorize
import json


class Visualization:

    def __init__(self, dataframe):
        self.df = dataframe
        self.features, self.df = detect_categories(self.df)
        self.categories = categorize(self.features)
        self.plots = {}
        self.num_cols = self.categories.get("numerical")
        self.cat_cols = self.categories.get("categorical")
        self.dt_cols = self.categories.get("datetime")

    def __str__(self):
        return json.dumps(self.features, indent=1)

    # NUMERICAL

    def generate_histograms(self):
        if not self.num_cols:
            return []
        self.plots["Distribution"] = []
        for col in self.num_cols:
            fig, ax = plt.subplots()
            sns.histplot(self.df[col], palette="inferno", kde=True)
            self.plots["Distribution"].append(encode_img2b64(fig))

    def generate_boxplots(self):
        if not self.num_cols:
            return []
        self.plots["Boxplot"] = []
        for col in self.num_cols:
            fig, ax = plt.subplots()
            sns.boxplot(self.df[col], palette="inferno")
            self.plots["Boxplot"].append(encode_img2b64(fig))

    def generate_heatmap(self):
        if not self.num_cols or len(self.num_cols) < 2:
            return []

        fig, ax = plt.subplots()
        corr_matrix = self.df[self.num_cols].corr()
        sns.heatmap(
            corr_matrix, annot=True, ax=ax, fmt=".2f", linewidths=0.5, cmap="inferno"
        )
        self.plots["Heatmap"] = [encode_img2b64(fig)]
        plt.close(fig)

    # CATEGORICAL

    def generate_countplots(self):
        if not self.cat_cols:
            return []

        self.plots["Countplots"] = []
        for col in self.cat_cols:
            fig, ax = plt.subplots()
            ax.set_title(col)
            sns.countplot(x=self.df[col], palette="inferno")
            self.plots["Countplots"].append(encode_img2b64(fig))

    def generate_piecharts(self):
        if not self.cat_cols:
            return []

        self.plots["Pieplots"] = []
        for col in self.cat_cols:
            fig, ax = plt.subplots()
            ax.set_title(col)
            plt.pie(
                self.df[col].value_counts(),
                labels=self.df[col].value_counts().index,
                autopct="%1.2f%%",
            )
            self.plots["Pieplots"].append(encode_img2b64(fig))

    # DATETIME

    def generate_datetime_plots(self):
        if not self.dt_cols:
            return []

        self.plots["Datetime Plots"] = []
        for col in self.dt_cols:
            for sub_col in self.num_cols:
                if "id" in sub_col.lower():
                    continue
                month_df = self.df.copy()
                month_df["month"] = month_df[col].dt.month
                month_grouped = month_df.groupby("month")[sub_col].mean().reset_index()

                fig, ax = plt.subplots()
                ax.set_title(f"{sub_col} over Months")
                sns.lineplot(data=month_grouped, x="month", y=sub_col, ax=ax)
                self.plots["Datetime Plots"].append(encode_img2b64(fig))
                plt.close(fig)

                # ---- YEAR PLOT ----
                year_df = self.df.copy()
                year_df["year"] = year_df[col].dt.year
                year_grouped = year_df.groupby("year")[sub_col].mean().reset_index()

                fig, ax = plt.subplots()
                ax.set_title(f"{sub_col} over Years")
                sns.lineplot(data=year_grouped, x="year", y=sub_col, ax=ax)
                self.plots["Datetime Plots"].append(encode_img2b64(fig))
                plt.close(fig)

    def get_all(self):
        self.generate_histograms()
        self.generate_boxplots()
        self.generate_heatmap()
        self.generate_countplots()
        self.generate_piecharts()
        self.generate_datetime_plots()
        return self.plots
