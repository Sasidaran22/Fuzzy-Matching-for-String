# -*- coding: utf-8 -*-
"""
@author: Sasidaran s
Data set files should be imported to the same directory of the python compiler
"""

import pandas as pd
import recordlinkage

hospital_accounts = pd.read_excel('hospital_account_info.xlsx', index_col='Account_Num')
hospital_reimbursement = pd.read_excel('hospital_reimbursement.xlsx', index_col='Provider_Num')
indexer = recordlinkage.Index()
indexer.full()
# First hundred records are taken into consideration for shorter time execution 
hospital_accounts=hospital_accounts[1:100]
hospital_reimbursement=hospital_reimbursement[1:100]

# Hospital accounts file gives the data collected at hospital and hospital reimbursemnts file gives the data collected at insurance section for reimbursemnets
candidates = indexer.index(hospital_accounts, hospital_reimbursement)
print(len(candidates))
compare = recordlinkage.Compare()

# Records are matched with exact matching in city name attribute
compare.exact('City', 'Provider City', label='City')

# Records are shown only when the quantative measure of the attributes of the data reaches the threshold of 0.85
compare.string('Facility Name',
            'Provider Name',
            threshold=0.85,
            label='Hosp_Name')
compare.string('Address',
            'Provider Street Address',
            method='jarowinkler',
            threshold=0.85,
            label='Hosp_Address')

# Comparison logic is defined using compute function in compare object 
features = compare.compute(candidates, hospital_accounts,
                        hospital_reimbursement)

# One key concept is that we can use blocking to limit the number of comparisons. For instance, we know that it is very likely that we only want to compare hospitals that are in the same state. We can use this knowledge to setup a block on the state columns:
indexer = recordlinkage.Index()
indexer.block(left_on='State', right_on='Provider State')
candidates = indexer.index(hospital_accounts, hospital_reimbursement)
print("Records after using blocking to reduce the number of comaprison "+str(len(candidates)))
indexer = recordlinkage.Index()
indexer.sortedneighbourhood(left_on='State', right_on='Provider State')
candidates = indexer.index(hospital_accounts, hospital_reimbursement)
print("Records that has the same pronounciation but misspelled "+str(len(candidates)))

print("Compared data attributes"+'\n'+str(features))
print(features.sum(axis=1).value_counts().sort_index(ascending=False))
potential_matches = features[features.sum(axis=1) > 1].reset_index()
potential_matches['Score'] = potential_matches.loc[:, 'City':'Hosp_Address'].sum(axis=1)
print(potential_matches)
print("The first record in hospital_reimbursement file with the best match to the first reccord in the hospital_accounts file:")
print("The record from the hospital_accounts file:"+'\n'+str(hospital_accounts.loc[potential_matches['Account_Num'][0]]))
print('\n'+"The record from the hospital_reimbursement file:"+'\n'+str(hospital_reimbursement.loc[potential_matches['Provider_Num'][0]]))

# concatenated all the attributes for each of these source DataFrame as Acct_Name_lookup and Reimbursement_Name_lookup
hospital_accounts['Acct_Name_Lookup'] = hospital_accounts[[
    'Facility Name', 'Address', 'City', 'State'
]].apply(lambda x: '_'.join(x), axis=1)

hospital_reimbursement['Reimbursement_Name_Lookup'] = hospital_reimbursement[[
    'Provider Name', 'Provider Street Address', 'Provider City',
    'Provider State'
]].apply(lambda x: '_'.join(x), axis=1)
account_lookup = hospital_accounts[['Acct_Name_Lookup']].reset_index()

# Merge in with the account data and reimbursement data
reimbursement_lookup = hospital_reimbursement[['Reimbursement_Name_Lookup']].reset_index()
account_merge = potential_matches.merge(account_lookup, how='left')
final_merge = account_merge.merge(reimbursement_lookup, how='left')
cols = ['Account_Num', 'Provider_Num', 'Score',
        'Acct_Name_Lookup', 'Reimbursement_Name_Lookup']
print(final_merge[cols].sort_values(by=['Account_Num', 'Score'], ascending=False))

#The matched records are exported to an Excel file in the same directory
mergelist=final_merge.sort_values(by=['Account_Num', 'Score'],
                    ascending=False)
mergelist.to_excel('merge_list.xlsx',index=False)

print(mergelist)
