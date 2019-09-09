## Project: Log Analysis
###### Author: L. Diaz
###### Date submitted: 09/09/2019

#### Overview:
The code submitted in this assignment is meant to run alongside the  
newsdata.sql file. It utilizes only three PostregSQL queries to perform  
the following tasks:

1. Reports the most popular articles of all time
2. Reports the most popular article authors of all time
3. Report the days in which more than 1% of requests failed

The script used to analyze and report on the database can be found on  
the logReport.py file. It has been designed and tested with Python 3.  
All views are created within the script, so it is not necessary to create  
them within PSQL.

To get the results from the report, simply run:

> python3 logReport.py

The results are printed in plain text onto the terminal.

#### Code:

##### Problem 1:

The code to solve the first task uses 1 view and 1 SQL query.

The view is created within the script and it simplifies the query.  
That same view, called **_article_views_**, is also used in task 2.

This view combines the articles and log tables with a left join on those  
rows where the log.path contains the articles.slug within it.
> A left join is used such that if a new article was published but had no views, it would still appear within the report.

From those tables, the title, author and a count of the number of times  
they appear in the log are selected. The count is performed on the log  
table such that in the hypothetical case above, a new article will be shown  
with a count of 0.

Finally, a WHERE statement is used within the view to filter out any log  
which was not a succesful HTTP request (i.e. _200 OK_).

The query to finish task 1 then becomes quite simple, where it is only necessary to select the title and count number from the view, order by the count in descending order and limit the results to only the top 3.

##### Problem 2:

The same view created for problem 1 is used in this problem.

In this case, however, the table of authors is combined with the view using  
a left join for similar reasons to those outlined above.

Then similarly, the result is order by the count in descending order and  
grouped by the authors.

##### Problem 3:

Task no. 3 requires only one table. However, for this problem two new  
views are created.

The first view groups all of the requests from the log table by date, and  
casts the date column into a simplified DATETIME::DATE type. This view  
also counts all of the requests, such that its result would be all the  
requests that were made in any given day.

The second view does a similar thing, but in this case it only aggregates  
the bad requests using a WHERE statement.

Finally, the query then combines both views and calculates the ratio of  
bad requests to total requests for any given day. This gives the  
percentage of errors per day. It selects the date and percentage from  
those days in which this percentage surpassed 1%.
