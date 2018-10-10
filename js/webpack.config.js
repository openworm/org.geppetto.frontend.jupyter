const path = require('path');

var rules = [
    { test: /\.less$/, use: [{loader: "style-loader"}, {loader: "css-loader" }, {loader: "less-loader" }]},
];
module.exports = [
    {// Notebook extension
        entry: './src/index.js',
        output: {
            filename: 'index.js',
            //Move to static folder
            path: path.resolve(__dirname, '../jupyter_geppetto'),
            libraryTarget: 'amd'
        },
        module: {
            rules: rules
        }
    }
];