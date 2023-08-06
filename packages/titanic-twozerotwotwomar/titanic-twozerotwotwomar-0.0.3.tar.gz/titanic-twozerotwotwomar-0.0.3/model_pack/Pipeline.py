import Features as Fea
from Config.config_validations import Config
from feature_engine.encoding import OneHotEncoder, RareLabelEncoder
from feature_engine.imputation import (
    AddMissingIndicator,
    CategoricalImputer,
    MeanMedianImputer,
)
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# import yaml


# with open('config.yaml','r') as file:
#    y=yaml.safe_load(file)


def titanic_pipe() -> Pipeline:

    # set up the pipeline
    pipeline = Pipeline(
        [
            ("Replacing_?_with_nan", Fea.ReplacingWithNan()),
            (
                "Converting_the_numerical_to_float",
                Fea.CovertingToFloat(variables=Config.pipe_params.NUMERICAL_VARIABLES),
            ),
            (
                "salutation_extraction",
                Fea.SalutationExtraction(variables=Config.pipe_params.SALUTATION),
            ),
            (
                "dropping_features",
                Fea.FeatureDropping(variables=Config.pipe_params.DROP),
            ),
            # ===== IMPUTATION =====
            # impute categorical variables with string 'missing'
            (
                "categorical_imputation",
                CategoricalImputer(variables=Config.pipe_params.CATEGORICAL_VARIABLES),
            ),
            # add missing indicator to numerical variables
            (
                "missing_indicator",
                AddMissingIndicator(variables=Config.pipe_params.NUMERICAL_VARIABLES),
            ),
            # impute numerical variables with the median
            (
                "median_imputation",
                MeanMedianImputer(variables=Config.pipe_params.NUMERICAL_VARIABLES),
            ),
            # Extract first letter from cabin
            (
                "extract_letter",
                Fea.ExtractLetterTransformer(variables=Config.pipe_params.CABIN),
            ),
            # == CATEGORICAL ENCODING ======
            # remove categories present in less than 5% of the observations (0.05)
            # group them in one category called 'Rare'
            (
                "rare_label_encoder",
                RareLabelEncoder(variables=Config.pipe_params.CATEGORICAL_VARIABLES),
            ),
            # encode categorical variables using one hot encoding into k-1 variables
            (
                "categorical_encoder",
                OneHotEncoder(
                    drop_last=True, variables=Config.pipe_params.CATEGORICAL_VARIABLES
                ),
            ),
            # scale using standardization
            ("scaler", StandardScaler()),
            # logistic regression (use C=0.0005 and random_state=0)
            (
                "Logit",
                LogisticRegression(
                    C=Config.model_params.C,
                    random_state=Config.model_params.Model_random_State,
                ),
            ),
        ]
    )

    return pipeline


if __name__ == "__main__":
    # pass
    print(Config.pipe_params.CATEGORICAL_VARIABLES)


# python Pipeline.py
