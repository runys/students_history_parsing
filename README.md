Students Performance Study
==========================
That is an study on the performance of software engineering students around the use of teaching methodologies based on programming competitions and the use of online judges.

The Database
------------
The database was built using the students histories provided by the institution where the study was made.

The extraction of the data from those pdfs were made with the following steps:

1. Acquiring the pdfs
2. Converting the pdfs to txt using [Cloud Convert][1]
3. Erasing the names and all the personal information from the students histories.
4. Processing the data using python scripts and creating JSON files.

The data visualization
----------------------
To visualize the data using charts and other visual resources we are using [Chart.js][2] and [AngularJS][3]. Thanks to [MaterializeCSS][4], everything is beautiful.

To get everything running follow these steps:

1. Make sure you have **NodeJS** installed.
2. Open the terminal and run `npm install -g gulp bower` to install the global requirements.
3. Install the local requirements with `npm install`.
4. Install the required libs with `bower install`.
5. Run `gulp` and preview it through **http://localhost:9999**

[1]: https://cloudconvert.com/pdf-to-txt
[2]: http://www.chartjs.org
[3]: https://angularjs.org
[4]: http://materializecss.com
