we'd like to map the citations in the /Users/simonwang/Library/CloudStorage/OneDrive-HongKongBaptistUniversity/OneDriveCursor/vibeCoding101/vibeCoding101/PolyUGuestLecture10Oct/output/paperFull.md with the reference 

the citations are in-text citations 

e.g. whereas Lass1998 [[66](https://link.springer.com/article/10.1007/s11042-022-13428-4#ref-CR66 "Lass R (1998) Phonology: An Introduction to Basic Concepts. Cambridge, UK; New York; Melbourne, Australia: Cambridge University Press. p. 1. ISBN 978–0–521-23728-4. Retrieved 8 January 2011Paperback ISBN 0–521–28183-0")]wrote that phonology 

should be mapped to Lass R (1998) Phonology: An Introduction to Basic Concepts. Cambridge, UK; New York; Melbourne, Australia: Cambridge University Press. p. 1. ISBN 978–0–521-23728-4. Retrieved 8 January 2011Paperback ISBN 0–521–28183-0 

we need to write a python program that takes each item in References and locate the paragraphs each item has been cited- sometime more than once

we will then generate a CSV to list the items and the paragraphs where they are cited


**@mapCitations.md**  please document your efforts /Users/simonwang/Library/CloudStorage/OneDrive-HongKongBaptistUniversity/OneDriveCursor/vibeCoding101/vibeCoding101/PolyUGuestLecture10Oct/Plan&test/citeMappinglog.md and output the CSV here /Users/simonwang/Library/CloudStorage/OneDrive-HongKongBaptistUniversity/OneDriveCursor/vibeCoding101/vibeCoding101/PolyUGuestLecture10Oct/output

apparently the results are not very good 

can we just ask the agent to do it directly 



/Users/simonwang/Library/CloudStorage/OneDrive-HongKongBaptistUniversity/OneDriveCursor/vibeCoding101/vibeCoding101/PolyUGuestLecture10Oct/output/comprehensive_citations_20251004_145107.csv only find 60 references
there should be a total of 160

we should first list all the 160 items in a file and then search for in-text citations one by one
let's list the 160 using python and then use AI agent's file tool to locate the paragraphs where each study is cited
