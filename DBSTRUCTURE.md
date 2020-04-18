# Database Structure

This API uses MongoDB which is a NoSQL Database. In this section, we will discuss the collections in our votingdb and the document data within. The collections are:

## Bills Collection- alpha
The document data for this collection shall include:
- the output from the ausbills.Bill().data object  
- the ID of the results document in the results collection

## Issues Collection - alpha
The document data for this collection shall include:
- Issue details; Title, question, description, answers?
- the ID of the results document in the results collection

## Ballotspecs Collection - alpha
This data is what same across both bills and issues and will form the basis for the ballotspec.
The document data for this collection shall include:
- id
- short_title
- question
- description
- start_date
- chamber
- Sponsor
- ballotspec hash

## Votes Collection - alpha
The document data for this collection shall include:
- id
- vote: yes/no
- Users public key
- Time
- Constituency

## Results Collection
The document data for this collection shall include:
- id
- Constituency
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
