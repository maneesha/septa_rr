This Django app works with data scraped from SEPTA's tranview json feed (http://www3.septa.org/hackathon/TrainView/).  A cronjob on a local server runs the scraper every minute and stores data in a local postgres database. The scraper script is included in the management/commands directory.

The web user interface allows users to search for trains by their source, destination, next stop, or minutes late.  Up to two search terms are allowed using the AND operator.

On the back end, future versions of this app will include:
*integration of GTFS data with this data 

Future versions of this app will include:
*ability to limit search to a date range
*aggregate search functions such as average, max, min late for a specific time period
*a prettier UI (although I consider myself more of a backend, not frontend, developer)

Suggestions for additional functionality are welcome!

DNM - PR test

