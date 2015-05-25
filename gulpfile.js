// Gulp
var gulp = require('gulp');

// Plugins
var connect = require('gulp-connect');

// Connect the project
gulp.task('connect', function(){
    connect.server({
        root: '.',
        port: 9999
    }); 
});

gulp.task('default', ['connect']);