from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from cassandra.data.trasformations.trasformations import create_model
from cassandra.model.modelEvaluation.evaluation import show_nrmse, show_mape


def linear(df, X, y, target, name_model, medias = [], organic = [], metric = ['accuracy', 'nrmse', 'mape'], return_metric = False):
    metrics_values = {}

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    if medias or organic:
        model = create_model(medias, organic, LinearRegression())
    else:
        model = LinearRegression()

    model.fit(X_train, y_train)

    # Ask the model to predict on X_test without having Y_test
    # This will give you exact predicted values

    # Score returns the accuracy of the above prediction or R^2
    if 'accuracy' in metric:
        accuracy = model.score(X_test, y_test)
        if return_metric:
            metrics_values[name_model + '_accuracy'] = accuracy
        print(name_model, 'Accuracy: ', accuracy)

    # We can use our NRMSE and MAPE functions as well

    # Create new DF not to edit the original one
    result = df

    # Create a new column with predicted values
    if medias or organic:
        result['prediction'] = model.predict(result)
    else:
        result['prediction'] = model.predict(X)


    # Get the NRMSE & MAPE values
    if 'nrmse' in metric:
        nrmse_val = show_nrmse(result[target], result['prediction'])
        if return_metric:
            metrics_values[name_model + '_nrmse'] = nrmse_val
        print(name_model, 'NRMSE: ', nrmse_val)

    if 'mape' in metric:
        mape_val = show_mape(result[target], result['prediction'])
        if return_metric:
            metrics_values[name_model + '_mape'] = mape_val
        print(name_model, 'MAPE: ', mape_val)

    if metrics_values:
        return result, model, metrics_values
    else:
        return result, model