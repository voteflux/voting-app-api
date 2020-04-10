# Database Structure

This API uses MongoDB which is a NoSQL Database. In this section, we will discuss the collections in our votingdb and the document data within. The collections are:

- BILLS - 'billscollection'
- ISSUES - 'issuescollection'
- RESULTS - 'resultscollection'
- USERS - 'userscollection'
- VOTES - 'votescollection'

## Bills Collection- alpha
The document data for this collection shall include:
- the output from the ausbills.Bill().data object  
- the hash from the ballotspec
- yes/no for the country
- the ID of the results document in the results collection

## Issues Collection - alpha
The document data for this collection shall include:
- Issue details; Title, question, description, answers?
- the hash from the ballotspec
- yes/no for the country
- the ID of the results document in the results collection

## Results Collection - beta
The document data for this collection shall include:
- Bills/Issue ID
- Constituent name
- Yes count
- No count


---

# Not Required

## User Collection - on client side
The document data for this collection shall include:

- Users password encrypted private key (For recovery)
- Users personal details
- AEC verification status
- AEC data: constituent etc

## Votes Collection - on blockchain
The document data for this collection shall include:
- Bill/Issue ID
- vote: yes/no
- Users (password encrypted) public key
- Time
- Constituent

Should we include age and sex for post analysis?
