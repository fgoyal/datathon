***REMOVED***
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt


# Read in data and display first 5 rows
data = pd.read_csv('Data Given/MMM-edited.csv')
# Q1 2018 -- January 1, 2018 to March 31, 2018
# Q2 2018 -- April 1, 2018 to June 30, 2018
# Q3 2018 -- July 1, 2018 to September 30, 2018
# Q4 2018 -- October 1, 2018 to December 31, 2018
# # Get dates for each quarter
# Q1_start = datetime.strptime("1/1", '%m/%d/%Y')
def quarters(row):
    if 1 <= row['Month'] <= 3:
        val = 'Q1'
    elif 4 <= row['Month'] <= 6:
        val = 'Q2'
    elif 7 <= row['Month'] <= 9:
        val = 'Q3'
    else:
        val = 'Q4'
    return val

#setting index as date
# data['Year'] = data['Date'].apply(lambda x: int(str(x)[-4:]))
#data['Date'] = pd.to_datetime(data.Date, format='%m/%d/%y')
date = data['Date'].str.split('/', expand=True)
data['Month'] = date[0].astype(np.int64)
data['Day'] = date[1].astype(np.int64)
data['Year'] = date[2].astype(np.int64)
data['Quarter'] = data.apply(quarters, axis=1)



print(data)

# One-hot encode the data using pandas get_dummies


# Create numpy array of data without Close
labels = np.array(data['Close'])  # Labels are the values we want to predict
dates = np.array(data['Date'])
data = data.drop('Close', axis=1)
data = data.drop('Date', axis=1)
data = pd.get_dummies(data)
factors_list = list(data.columns)
print(factors_list)
data = np.array(data)

# Split the data into training and testing sets
train_data, test_data, train_labels, test_labels, train_date, test_date = train_test_split(data, labels, dates, test_size=0.0127, shuffle=False)

# Get baseline prediction
average_close = labels.mean()
baseline_errors = abs(average_close - test_labels)
average_baseline_error = round(np.mean(baseline_errors), 2)
print('Average baseline error: ', average_baseline_error)


# Instantiate and train model with 1000 decision trees
rf = RandomForestRegressor(n_estimators=1000, random_state=42)
rf.fit(train_data, train_labels);

# Use the forest's predict method on the test data
predictions = rf.predict(test_data)

# Calculate errors
errors = abs(predictions - test_labels)
print('Mean Absolute Error:', round(np.mean(errors), 2), 'degrees.')

# Calculate mean absolute percentage error (MAPE)
mape = 100 * (errors / test_labels)
# Calculate and display accuracy
accuracy = 100 - np.mean(mape)
print('Accuracy:', round(accuracy, 2), '%.')



r2 = r2_score(predictions, test_labels)
print('R^2: ', round(r2, 2), '%.')

# Get numerical feature importances
importances = list(rf.feature_importances_)
# List of tuples with variable and importance
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(factors_list, importances)]
# Sort the feature importances by most important first
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
# Print out the feature and importances
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances];


training = pd.DataFrame({'Date': train_date, 'Close': train_labels})
training.index = training['Date']
actual = pd.DataFrame({'Date': test_date, 'Close': test_labels})
actual.index = actual['Date']
predicted = pd.DataFrame({'Date': test_date, 'Close': predictions})
predicted.index = predicted['Date']

# #plot
plt.figure(figsize=(16, 8))
plt.plot(training['Close'])
plt.plot(actual['Close'])
plt.plot(predicted['Close'])
plt.show()