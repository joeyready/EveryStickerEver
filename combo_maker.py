import csv
import os

#create a lite of all 50 states in the US

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

#creat dictionary of all states with their abbreviations for SKU production
state_abbr_dict = {'Alabama' : 'AL',
'Alaska' : 'AK',
'Arizona' : 'AZ', 'Arkansas' : 'AR', 'California' : 'CA', 'Colorado' : 'CO', 'Connecticut' : 'CT', 'Delaware' : 'DE', 'Florida' : 'FL', 'Georgia' : 'GA', 'Hawaii' : 'HI', 'Idaho' : 'ID', 'Illinois' : 'IL', 'Indiana' : 'IN', 'Iowa' : 'IA', 'Kansas' : 'KS', 'Kentucky' : 'KY', 'Louisiana' : 'LA', 'Maine' : 'ME', 'Maryland' : 'MD', 'Massachusetts' : 'MA', 'Michigan' : 'MI', 'Minnesota' : 'MN', 'Mississippi' : 'MS', 'Missouri' : 'MO', 'Montana' : 'MT', 'Nebraska' : 'NE', 'Nevada' : 'NV', 'New Hampshire' : 'NH', 'New Jersey' : 'NJ', 'New Mexico' : 'NM', 'New York' : 'NY', 'North Carolina' : 'NC', 'North Dakota' : 'ND', 'Ohio' : 'OH', 'Oklahoma' : 'OK', 'Oregon' : 'OR', 'Pennsylvania' : 'PA', 'Rhode Island' : 'RI', 'South Carolina' : 'SC', 'South Dakota' : 'SD', 'Tennessee' : 'TN', 'Texas' : 'TX', 'Utah' : 'UT', 'Vermont' : 'VT', 'Virginia' : 'VA', 'Washington' : 'WA', 'West Virginia' : 'WV', 'Wisconsin' : 'WI', 'Wyoming' : 'WY'}


# iterate over list to give every possible combination of 2 states

for state1 in states:
    for state2 in states:
        print(state1, state2)  #print the combination of states
#print number of combinations
print(len(states) * len(states))

# Updated function to include SKU in the combinations
def all_combinations_with_sku(states, state_abbr_dict):
    combinations_with_sku = []
    for state1 in states:
        for state2 in states:
            # Concatenate the abbreviations of state1 and state2 to form the SKU
            sku = "D-" + state_abbr_dict[state1] + "-M-" + state_abbr_dict[state2]
            combinations_with_sku.append((state1, state2, sku))
    return combinations_with_sku



# print(all_combinations(states))
# print(len(all_combinations(states)))  #print number of combinations

for state1, state2, sku in all_combinations_with_sku(states, state_abbr_dict):
    print(f"Don't {state1} My {state2} SKU: {sku}")  #print the combination of states

# #export the combinations to a csv file column 1 "Don't {State1}; column 2 "My {State2}"
# with open('state_combinations.csv', 'w') as file:
#     writer = csv.writer(file)
#     writer.writerow(['State1', 'State2'])
#     for state1, state2 in all_combinations(states):
#         writer.writerow(["Don't " + state1, "My " + state2])

# # Updated function to include SKU in the combinations
# def all_combinations_with_sku(states, state_abbr_dict):
#     combinations_with_sku = []
#     for state1 in states:
#         for state2 in states:
#             # Concatenate the abbreviations of state1 and state2 to form the SKU
#             sku = state_abbr_dict[state1] + state_abbr_dict[state2]
#             combinations_with_sku.append((state1, state2, sku))
#     return combinations_with_sku

# Export the combinations to a csv file with an additional 'SKU' column
with open('venv/state_combinations.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['State1', 'State2', 'SKU'])  # Include 'SKU' in the header
    for state1, state2, sku in all_combinations_with_sku(states, state_abbr_dict):
        writer.writerow(["Don't " + state1, "My " + state2, sku])

# with open('state_combinations.csv', 'w') as file:
#     writer = csv.writer(file)
#     writer.writerow(['State1', 'State2'])
#     for state1, state2 in all_combinations(states):
#         writer.writerow([state1, state2])

# #seperate state_combinations.csv to separate files with a maximum of 250 combinations pre csv file
# with open('state_combinations.csv', 'r') as file:
#     reader = csv.reader(file)
#     header = next(reader)
#     count = 0
#     file_number = 1
#     with open(f'state_combinations_{file_number}.csv', 'w') as file:
#         writer = csv.writer(file)
#         writer.writerow(header)
#         for row in reader:
#             writer.writerow(row)
#             count += 1
#             if count >= 250:
#                 count = 0
#                 file_number += 1
#                 file = open(f'state_combinations_{file_number}.csv', 'w')
#                 writer = csv.writer(file)
#                 writer.writerow(header)
#                 print(f"state_combinations_{file_number}.csv")
#                 print("New file created")

# create new folder for each of the csv files with the same name
with open('venv/state_combinations.csv', 'r') as file:
    reader = csv.reader(file)
    header = next(reader)
    count = 0
    file_number = 1
    os.mkdir(f'state_combinations_{file_number}')
    with open(f'state_combinations_{file_number}/state_combinations_{file_number}.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for row in reader:
            writer.writerow(row)
            count += 1
            if count >= 250:
                count = 0
                file_number += 1
                os.mkdir(f'state_combinations_{file_number}')
                file = open(f'state_combinations_{file_number}/state_combinations_{file_number}.csv', 'w')
                writer = csv.writer(file)
                writer.writerow(header)
                print(f"state_combinations_{file_number}.csv")
                print("New file created")

