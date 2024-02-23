import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt


prefix = "https://content.codecademy.com/courses/beautifulsoup/"
webpage_response = requests.get('https://content.codecademy.com/courses/beautifulsoup/shellter.html')

webpage = webpage_response.content
soup = BeautifulSoup(webpage, "html.parser")

turtle_links = soup.find_all("a")
links = []
#go through all of the a tags and get the links associated with them"
for a in turtle_links:
  links.append(prefix+a["href"])
    
#Define turtle_data:
turtle_data = {}

#follow each link:
for link in links:
  webpage = requests.get(link)
  turtle = BeautifulSoup(webpage.content, "html.parser")
  turtle_name = turtle.select(".name")[0].get_text()
  
  stats = turtle.find("ul")
  stats_text = stats.get_text("|")
  turtle_data[turtle_name] = stats_text.split("|")

turtle_df = pd.DataFrame(turtle_data)

# Clean the data
# 1. Remove rows containing only '\n' values
turtle_df = turtle_df.replace('\n', pd.NA).dropna(how='all')

# 2. Transpose the DataFrame
turtle_df = turtle_df.T

# Reset index
turtle_df.reset_index(inplace=True)

# Assign the new column labels to the DataFrame
turtle_df.columns = [0, 1, 2, 3, 4, 5]

# 3. Extract numerical range from the second column
turtle_df[1] = turtle_df[1].str.extract(r'(\d+(?:\.\d+)?)').astype(float)

# 3. Extract numerical range from the second column
turtle_df[2] = turtle_df[2].str.extract(r'(\d+(?:\.\d+)?)').astype(float)

#4. Define a function to convert SEX column to boolean
def sex_to_boolean(sex):
  return 1 if "Male" in sex else 0

#4. Apply the function to the SEX column
turtle_df[3] = turtle_df[3].apply(sex_to_boolean)

#5. Remove the "BREED: " prefix from each entry in the column 4
turtle_df[4] = turtle_df[4].str.replace('BREED: ', '')

# Define a dictionary to map each breed to its numerical value
breed_mapping = {
    'African Aquatic Sideneck Turtle': 1,
    'Eastern Box Turtle': 2,
    'Greek Tortoise': 3
}

# Map the breeds to their numerical values
turtle_df[4] = turtle_df[4].map(breed_mapping)

#5. Remove the "SOURCE: " prefix from each entry in the column 5
turtle_df[5] = turtle_df[5].str.replace('SOURCE: ', '')

# Define a dictionary to map each source to its numerical value
source_mapping = {
    'found in Lake Erie': 1,
    'hatched in house': 2,
    'surrendered by owner': 3
}

# Map the breeds to their numerical values
turtle_df[5] = turtle_df[5].map(source_mapping)


# Assign the new column labels to the DataFrame
turtle_df.columns = ['Name', 'Age', 'Weight', 'Sex', 'Breed', 'Source']

# Set display options to show all rows and columns
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Print the DataFrame
print(turtle_df)


# Group by Male column and calculate average weight
average_weight = turtle_df.groupby('Sex')['Weight'].mean()

# Plot box chart
plt.figure(figsize=(8, 6))
turtle_df.boxplot(column='Weight', by='Sex', grid=False)
plt.title('Average Weight for Males and Females')
plt.xlabel('Sex')
plt.ylabel('Weight')
plt.xticks([1, 2], ['Female', 'Male'])
plt.show()