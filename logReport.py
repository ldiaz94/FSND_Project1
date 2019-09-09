#!/usr/bin/env python3

# UDACITY FULL STACK WEB DEVELOPER NANODEGREE
# PROJECT 1
# LOG ANALYSIS
# ==============================================
# Author: Luis Diaz
# Date: 07/09/2019
# Last Edited: 08/09/2019

import psycopg2
import datetime

print('''\nBEGINNING OF REPORT
      \nDate and Time: {:%A %d of %B, %Y - %H:%M:%S}
      \n========================'''
      .format(datetime.datetime.now()))

# Conenct to db and create cursor
conn = psycopg2.connect("dbname=news")
cursor = conn.cursor()


# Get the 3 most viewed articles from database using a view
# and 1 PostregSQL query.
#
# Create a view to simplify the query to the database.
# This view is later also used in solving problem 2.
# The view joins the articles and log tables using a left join
# such that even if an article hadn't been visited it would still
# appear. The count is implemented on the log.path entry such that
# if that were the case, the new article would show 0 visits.
#
# A wildcard is used before the article.slug entry to match the
# logs path (which is formatted as /article/{slug}). This makes the query
# less verbose. Only logs which report a successful (200 OK) HTTP status are
# counted as visited.
cursor.execute('''CREATE VIEW article_views AS
            SELECT articles.title, articles.author, count(log.path) as num
            FROM articles LEFT JOIN log
            ON log.path LIKE ('%' || articles.slug)
            WHERE log.status = '200 OK'
            GROUP BY articles.title, articles.author;''')

cursor.execute('''SELECT title, num
            FROM article_views
            ORDER BY num DESC
            LIMIT 3;''')

# Format and present the results
print('\nHere are the most popular articles:\n')

for article, views in cursor.fetchall():
    print("\"{}\" - {} views".format(article, views))

print('\n========================\n')


# Sort the list of authors by popularity in descending order.
#
# This query uses the view created in the previous step and
# left joins it with the authors table. This ensures that
# if a new author is added to the team, that person will still
# appear in the query even when they haven't created any articles
# yet.
cursor.execute('''SELECT authors.name, SUM(article_views.num) AS num
            FROM authors LEFT JOIN article_views
            ON authors.id = article_views.author
            GROUP BY authors.name
            ORDER BY num DESC;''')

# Format and present the results
print('Here is how the authors stand:\n')

for author, num in cursor.fetchall():
    print("{} - {} views".format(author, num))

print('\n========================\n')


# Find the days in which more than 1% of requests received
# an error status.
#
# In order to do this, it is necessary to create two new views.
# One view does a SELECT where the logs are grouped and counted
# by date regardless of there status. This represents total requests.
#
# The second view does something similar, but it uses WHERE to select
# only those logs that resulted in an error status.
#
# A SELECT is then ran using both views where only the rows in which
# the bad requests (as a float) * 100 / total requests is greater
# than 1 (that is 1%). The number is expressed as a numeric for
# formatting purposes.
cursor.execute('''CREATE VIEW requests AS
            SELECT time::TIMESTAMP::DATE AS date, COUNT(*) AS num
            FROM log
            GROUP BY date
            ORDER BY date;''')

cursor.execute('''CREATE VIEW bad_requests AS
            SELECT time::TIMESTAMP::DATE AS date, COUNT(*) AS num
            FROM log
            WHERE status != '200 OK'
            GROUP BY date
            ORDER BY date;''')

cursor.execute('''SELECT requests.date,
            (bad_requests.num::float*100/requests.num)::numeric(5,2) as pct
            FROM requests, bad_requests
            WHERE requests.date = bad_requests.date
            AND (bad_requests.num::float*100/requests.num) > 1''')

# Format and present the results
print('Here are the dates in which more than 1% of requests were bad:\n')

for date, pct in cursor.fetchall():
    print('{:%B, %d %Y} - {}% errors'.format(date, pct))

print('\nEND OF REPORT\n========================\n')

# Close connection
conn.close()
